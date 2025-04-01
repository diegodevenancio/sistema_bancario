from datetime import datetime

menu = """

    [1] Depositar
    [2] Sacar
    [3] Extrato
    [0] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0:
            saldo += valor
            data = datetime.now().strftime("%d/%m/%y %H:%M:%S")
            extrato += f"{data} - Depósito: R${valor:.2f}\n"
            print("Depósito realizado com sucesso!")
        else:
            print("Valor inválido. Tente novamente.")
    
    elif opcao == "2":
        valor = float(input("Informe o valor do saque. "))
        if numero_saques >= LIMITE_SAQUES:
            print("Limite de saques diários atingido.")
        elif valor > limite:
            print("O valor do saque excede o limite permitido de R$500,00.")
        elif valor > saldo:
            print("Saldo insuficiente.")
        elif valor > 0:
            saldo -= valor
            data = datetime.now().strftime("%d/%m/%y %H:%M:%S")
            extrato += f"{data} - Saque: R${valor:.2f}\n"
            numero_saques += 1
            print("Saque realizado com sucesso!")
        else:
            print("Valor inválido. Tente novamente.")
    
    elif opcao == "3":
        print("==================== EXTRATO ====================")
        print(extrato if extrato else "Não foram realizadas movimentações.")
        data = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        print(f"\n{data} - Saldo atual: R${saldo:.2f}")
        print("=================================================")
            
    elif opcao == "0":
        print("Saindo... Obrigado por utilizar nosso sistema!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")