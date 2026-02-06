from portifolio import Portifolio
import sys

def main():
    if len(sys.argv) != 2:
        print("uso main.py investimento")
        return 1


    investir =float(sys.argv[1])
    port = Portifolio(investir)
    port.CalcInvestimento()
    tabela = port.dados()
    print(tabela)
    total = sum(tabela["preco"] * tabela["comprar"])

    print(f"Total = {total}")

    print()
    print()
    port.confInvest()


main()