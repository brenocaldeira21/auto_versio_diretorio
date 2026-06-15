import os
import json
from datetime import datetime

# Constantes para evitar digitar os mesmos nomes (Boa prática)
DIRETORIO_RAIZ = "." 
PASTA_LOGS = "logs"
NOME_ARQUIVO_LOG = "log.json"
NOME_GITKEEP = ".gitkeep"

def processar_diretorios(raiz: str) -> dict:
    """
    Percorre os diretórios aplicando as regras do .gitkeep.
    Retorna um dicionário com os registros de criação e remoção.
    """
    registros = {
        "criados": [],
        "removidos": [],
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # os.walk percorre toda a árvore de diretórios
    for diretorio_atual, sub_diretorios, arquivos in os.walk(raiz):
        
        # 1. Restrição Importante: Ignorar a pasta logs
        if PASTA_LOGS in diretorio_atual.split(os.sep):
            continue
            
        # O os.walk passará primeiro na raiz ".". 
        # Ignoramos a raiz se não quisermos criar/apagar .gitkeep nela própria.
        if diretorio_atual == raiz:
             continue

        caminho_gitkeep = os.path.join(diretorio_atual, NOME_GITKEEP)

        # 2. Diretórios Vazios: Se não há subdiretórios e não há arquivos
        if not sub_diretorios and not arquivos:
            # Cria o arquivo .gitkeep
            with open(caminho_gitkeep, 'w') as f:
                pass # Cria o arquivo vazio
            registros["criados"].append(caminho_gitkeep)
            print(f"Criado: {caminho_gitkeep}")

        # 3. Diretórios Não Vazios: Se há subdiretórios ou arquivos (além do próprio .gitkeep)
        else:
            # Verifica se apenas o .gitkeep existe lá dentro (neste caso, a pasta conta como vazia para nós)
            if len(arquivos) == 1 and arquivos[0] == NOME_GITKEEP and not sub_diretorios:
                continue # Deixa ele lá, a pasta está virtualmente vazia
            
            # Se a pasta realmente tem conteúdo útil e possui um .gitkeep, devemos removê-lo
            if NOME_GITKEEP in arquivos:
                os.remove(caminho_gitkeep)
                registros["removidos"].append(caminho_gitkeep)
                print(f"Removido: {caminho_gitkeep}")

    return registros

def registrar_logs(novos_registros: dict):
    """
    Cria a pasta logs se não existir e anexa o novo registro no arquivo log.json.
    """
    # Cria diretório de logs se não existir
    if not os.path.exists(PASTA_LOGS):
        os.makedirs(PASTA_LOGS)

    caminho_log = os.path.join(PASTA_LOGS, NOME_ARQUIVO_LOG)
    historico_logs = []

    # Se o arquivo já existe, lê o histórico antigo primeiro
    if os.path.exists(caminho_log):
        try:
            with open(caminho_log, 'r', encoding='utf-8') as f:
                historico_logs = json.load(f)
        except json.JSONDecodeError:
            # Caso o arquivo exista mas esteja corrompido ou vazio
            historico_logs = []

    # Adiciona o novo registro à lista
    historico_logs.append(novos_registros)

    # Escreve a lista completa atualizada de volta no arquivo
    with open(caminho_log, 'w', encoding='utf-8') as f:
        # Usa o json.dump com indent=4 para ficar bonitinho e fácil de ler
        json.dump(historico_logs, f, indent=4, ensure_ascii=False)
    
    print(f"\nLog atualizado com sucesso em: {caminho_log}")

def main():
    print("--- Iniciando verificação de diretórios ---")
    registros_da_execucao = processar_diretorios(DIRETORIO_RAIZ)
    registrar_logs(registros_da_execucao)
    print("--- Verificação finalizada ---")

if __name__ == "__main__":
    main()