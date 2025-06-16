def start_interface():
    import sys
    from agents.csv_agent import CSVAgent

    agent = CSVAgent()
    agent.load_data()

    print("Bem-vindo ao sistema de perguntas sobre arquivos CSV!")
    files = agent.list_files()
    if not files:
        print("Nenhum arquivo CSV encontrado em src/data.")
        sys.exit()

    print("Arquivos disponíveis:")
    for idx, fname in enumerate(files):
        print(f"{idx+1}: {fname}")

    while True:
        file_idx = input("Escolha o número do arquivo para consultar (ou 'sair'): ")
        if file_idx.lower() == 'sair':
            print("Encerrando a interface. Até logo!")
            sys.exit()
        if not file_idx.isdigit() or int(file_idx) < 1 or int(file_idx) > len(files):
            print("Escolha inválida.")
            continue
        filename = files[int(file_idx)-1]
        print(f"Você selecionou: {filename}")

        while True:
            question = input("Digite sua pergunta ('voltar' para escolher outro arquivo, 'sair' para encerrar): ")
            if question.lower() == 'sair':
                print("Encerrando a interface. Até logo!")
                sys.exit()
            if question.lower() == 'voltar':
                break
            answer = agent.query_data(filename, question)
            print("Resposta:", answer)