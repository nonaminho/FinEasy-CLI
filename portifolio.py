from brapi import Brapi
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

client = Brapi(
    api_key = os.environ.get("BRAPI_API_KEY"),
)

class Portifolio:
    def __init__(self, investimento):
        self.investimento = investimento
        self.__dados = pd.read_csv("portifolio.csv")
        self.getPortifolio()

    #retorna o Portifolio
    def getPortifolio(self):
        precos = self.__pullBrapi(self.__dados["ticket"].tolist())
        self.__dados["preco"] = precos
        self.__dados["investido"] = self.__dados["tenho"] * self.__dados["preco"]
    
    #Metodo interno para puxar os valors das açoes...     
    def __pullBrapi(self, ticker):
        papel=",".join(ticker)
        quote = client.quote.retrieve(tickers=papel)
        precos = []
        for stock in quote.results:
            precos.append(stock.regular_market_price)
        precos.append(1)
        return precos
    
    #Calcula o investimento necessario para balancear a carteira
    def CalcInvestimento(self):
        self.__dados["perc"] = self.__dados["nota"] / self.__dados["nota"].sum()
        total_inv = self.__dados["investido"].sum() + self.investimento
        self.__dados["diferenca"] = total_inv * self.__dados["perc"] - self.__dados["investido"]
        self.__dados["comprar"] = (self.__dados["diferenca"] / self.__dados["preco"]).round()

    def dados(self):
        return self.__dados 
    
    def confInvest(self):
        df = self.__dados.copy()
        df["tenho"] += df["comprar"]
        df.drop(["preco","investido","perc","diferenca","comprar"], axis=1, inplace=True)
        df.to_csv("portifolio.csv")