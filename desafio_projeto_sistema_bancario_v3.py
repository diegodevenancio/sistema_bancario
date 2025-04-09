import datetime  # Importa o módulo datetime para lidar com datas e horários

# Constantes e estruturas iniciais
AGENCIA = "0001"  # Número fixo da agência bancária
usuarios = []     # Lista que armazena os usuários do sistema
contas = []       # Lista que armazena as contas bancárias

# Função para buscar um usuário na lista pelo CPF
def localizar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario  # Retorna o usuário se o CPF for encontrado
    return None  # Retorna None se não encontrar o CPF

# Função para criar um novo usuário e opcionalmente uma conta
def criar_usuario(usuarios, contas):
    cpf = input("Informe o CPF do novo usuário: ").strip()

    # Verifica se o CPF já está cadastrado
    if localizar_usuario(cpf, usuarios):
        print("⚠️  Usuário já cadastrado.")
        return

    # Coleta os dados do novo usuário
    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()

    # Cria o dicionário do usuário e adiciona à lista
    usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }

    usuarios.append(usuario)
    print("✅ Usuário criado com sucesso!")

    # Pergunta se o usuário deseja criar uma conta logo após o cadastro
    resposta = input("Deseja criar uma conta bancária para esse usuário agora? (s/n): ").lower()
    if resposta == 's':
        numero_conta = len(contas) + 1
        conta = {
            "agencia": AGENCIA,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "transacoes": [],
            "saldo": 0.0
        }
        contas.append(conta)
        print(f"✅ Conta criada com sucesso! Número da conta: {numero_conta}")

# Função para criar uma nova conta para um usuário já existente
def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = localizar_usuario(cpf, usuarios)

    if usuario:
        conta = {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "transacoes": [],
            "saldo": 0.0
        }
        contas.append(conta)
        print(f"✅ Conta criada com sucesso! Número da conta: {numero_conta}")
    else:
        print("❌ Usuário não encontrado. Conta não criada.")

# Função para listar todas as contas cadastradas
def listar_contas(contas):
    print("\n=========== CONTAS CADASTRADAS ===========\n")
    for conta in contas:
        print(f"""
        Agência:	{conta['agencia']}
        C/C:		{conta['numero_conta']}
        Titular:	{conta['usuario']['nome']}
        CPF:		{conta['usuario']['cpf']}
        """)
    print("========================================\n")

# Função para realizar depósito em uma conta
def depositar(contas):
    numero_conta = int(input("Informe o número da conta: "))
    conta = localizar_conta(numero_conta, contas)

    if conta:
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0:
            conta["saldo"] += valor
            conta["transacoes"].append((datetime.datetime.now(), "Depósito", valor))
            print("✅ Depósito realizado com sucesso!")
        else:
            print("❌ Valor inválido.")
    else:
        print("⚠️  Conta não encontrada.")

# Função para realizar saque de uma conta
def sacar(contas):
    numero_conta = int(input("Informe o número da conta: "))
    conta = localizar_conta(numero_conta, contas)

    if conta:
        valor = float(input("Informe o valor do saque: "))
        if 0 < valor <= conta["saldo"]:
            conta["saldo"] -= valor
            conta["transacoes"].append((datetime.datetime.now(), "Saque", valor))
            print("✅ Saque realizado com sucesso!")
        else:
            print("❌ Saque inválido ou saldo insuficiente.")
    else:
        print("⚠️  Conta não encontrada.")

# Função para exibir o extrato bancário da conta
def exibir_extrato(contas):
    numero_conta = int(input("Informe o número da conta: "))
    conta = localizar_conta(numero_conta, contas)

    if conta:
        print("\n================ EXTRATO ================")
        print(f"Agência:	{conta['agencia']}")
        print(f"C/C:		{conta['numero_conta']}")
        print(f"Titular:	{conta['usuario']['nome']}")
        print(f"CPF:		{conta['usuario']['cpf']}")
        print("------------------------------------------")
        for data, tipo, valor in conta["transacoes"]:
            print(f"[{data.strftime('%d/%m/%Y %H:%M:%S')}] {tipo:<10} R$ {valor:.2f}")
        print(f"\nSaldo atual:	R$ {conta['saldo']:.2f}")
        print("Data/hora:	" + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("==========================================\n")
    else:
        print("⚠️  Conta não encontrada.")

# Função auxiliar para localizar uma conta pelo número
def localizar_conta(numero_conta, contas):
    for conta in contas:
        if conta["numero_conta"] == numero_conta:
            return conta
    return None

# Função principal do programa
def main():
    print("🚀  Bem-vindo ao sistema bancário!")
    cpf_inicial = input("Por favor, informe seu CPF para acessar o sistema: ").strip()
    usuario = localizar_usuario(cpf_inicial, usuarios)

    # Se o CPF não estiver cadastrado, cria um novo usuário
    if not usuario:
        print("🔔  CPF não encontrado. Vamos criar um novo usuário.")
        criar_usuario(usuarios, contas)
    else:
        print(f"👤  Bem-vindo de volta, {usuario['nome']}!")

    # Loop principal do menu
    while True:
        print("""
================ MENU ================
[1]     Depositar
[2]     Sacar
[3]     Extrato
[4]     Nova conta
[5]     Listar contas
[6]     Novo usuário
[0]     Sair
=> """, end="")

        opcao = input().strip()

        if opcao == "1":
            depositar(contas)
        elif opcao == "2":
            sacar(contas)
        elif opcao == "3":
            exibir_extrato(contas)
        elif opcao == "4":
            numero_conta = len(contas) + 1
            criar_conta(AGENCIA, numero_conta, usuarios, contas)
        elif opcao == "5":
            listar_contas(contas)
        elif opcao == "6":
            criar_usuario(usuarios, contas)
        elif opcao == "0":
            print("👋 Encerrando o sistema. Até logo!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

# Garante que a função main() só será executada se o script for o principal
if __name__ == "__main__":
    main()
