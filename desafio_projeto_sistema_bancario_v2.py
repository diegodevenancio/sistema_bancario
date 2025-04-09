import textwrap
from datetime import datetime

def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDepositar 
    [2]\tSacar 
    [3]\tExtrato 
    [4]\tNova conta 
    [5]\tListar contas 
    [6]\tNovo usuário 
    [0]\tSair 
    => """
    return input(textwrap.dedent(menu))

def filtrar_usuario(cpf, usuarios):
    return next((u for u in usuarios if u["cpf"] == cpf), None)

def criar_usuario_interativo(cpf, usuarios):
    print("🔔  CPF não encontrado. Vamos criar um novo usuário.")
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco,
        "conta": {
            "agencia": "0001",
            "numero_conta": len(usuarios) + 1,
            "saldo": 0,
            "extrato": "",
            "numero_saques": 0
        }
    }
    usuarios.append(novo_usuario)
    print("✅  Usuário criado com sucesso!")
    return novo_usuario

def depositar(usuario):
    valor = float(input("Informe o valor do depósito: "))
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if valor > 0:
        usuario["conta"]["saldo"] += valor
        usuario["conta"]["extrato"] += f"[{data}] {'Depósito'.ljust(10)} R$ {valor:.2f}\n"
        print("\n✅  Depósito realizado com sucesso!")
    else:
        print("\n⚠️  Operação falhou! O valor informado é inválido.")

def sacar(usuario, limite=500, limite_saques=3):
    valor = float(input("Informe o valor do saque: "))
    conta = usuario["conta"]
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if valor <= 0:
        print("\n⚠️  Operação falhou! Valor inválido.")
    elif valor > conta["saldo"]:
        print("\n⚠️  Operação falhou! Saldo insuficiente.")
    elif valor > limite:
        print("\n⚠️  Operação falhou! Valor excede o limite por saque.")
    elif conta["numero_saques"] >= limite_saques:
        print("\n⚠️  Operação falhou! Número máximo de saques excedido.")
    else:
        conta["saldo"] -= valor
        conta["extrato"] += f"[{data}] {'Saque'.ljust(10)} R$ {valor:.2f}\n"
        conta["numero_saques"] += 1
        print("\n✅  Saque realizado com sucesso!")

def exibir_extrato(usuario):
    conta = usuario["conta"]
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    print("\n================ EXTRATO ================")
    print(f"Agência:\t{conta['agencia']}")
    print(f"C/C:\t\t{conta['numero_conta']}")
    print(f"Titular:\t{usuario['nome']}")
    print(f"CPF:\t\t{usuario['cpf']}")
    print("------------------------------------------")
    print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
    print(f"\nSaldo atual:\tR$ {conta['saldo']:.2f}")
    print(f"Data/hora:\t{data_atual}")
    print("==========================================")

def listar_contas(usuarios):
    print("\n=========== CONTAS CADASTRADAS ===========")
    for usuario in usuarios:
        conta = usuario["conta"]
        print(f"""
        Agência:\t{conta['agencia']}
        C/C:\t\t{conta['numero_conta']}
        Titular:\t{usuario['nome']}
        CPF:\t\t{usuario['cpf']}
        """)
        print("=" * 40)

def main():
    usuarios = []

    print("🚀  Bem-vindo ao sistema bancário!")
    cpf_cliente = input("Por favor, informe seu CPF para acessar o sistema: ")
    cliente = filtrar_usuario(cpf_cliente, usuarios)

    if not cliente:
        cliente = criar_usuario_interativo(cpf_cliente, usuarios)

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(cliente)

        elif opcao == "2":
            sacar(cliente)

        elif opcao == "3":
            exibir_extrato(cliente)

        elif opcao == "4":
            print("\n⚠️  Você já possui uma conta ativa!")

        elif opcao == "5":
            listar_contas(usuarios)

        elif opcao == "6":
            cpf_novo = input("Informe o CPF do novo usuário: ")
            if filtrar_usuario(cpf_novo, usuarios):
                print("⚠️  Usuário já cadastrado.")
            else:
                criar_usuario_interativo(cpf_novo, usuarios)

        elif opcao == "0":
            print("👋  Saindo do sistema. Até logo!")
            break

        else:
            print("⚠️  Opção inválida! Tente novamente.")

# Início do programa
main()
