from datetime import date, timedelta

import pandas as pd
from bs4 import BeautifulSoup
from requests import get

from web_scrapper import Web_Scrapper, Web_Scrapper_Factory


# ConcreteProduct
class Scrapper_Floods(Web_Scrapper):

    def config(self, data_inf: str, data_sup: str) -> None:
        self.data_inf=data_inf
        self.data_sup=data_sup

    # -------------GET ALL DAYS DATES BETWEEN TWO DATES-------------
    def getAlldays(self):

        data_inferior = self.data_inf.split("/")

        data_superior = self.data_sup.split("/")

        data_inicio = date(
            int(data_inferior[2]), int(data_inferior[1]), int(data_inferior[0])
        )
        data_fim = date(
            int(data_superior[2]), int(data_superior[1]), int(data_superior[0])
        )

        delta = data_fim - data_inicio
        dias = []
        for i in range(delta.days + 1):
            day = data_inicio + timedelta(days=i)
            dias.append(day)

        return dias

    def captar(self) -> None:
        try:
            # --------create dataframe--------
            colunas = [
                "data",
                "periodo",
                "endereco",
                "sentido",
                "referencia",
                "status",
                "url_base",
                "string",
            ]
            df = pd.DataFrame(columns=colunas)

            print(self.getAlldays())

            for i in self.getAlldays():
                print(i)

                # --------create url_base CGE--------
                data = str(i).split("-")

                dia = data[2]
                mes = data[1]
                ano = data[0]

                url_base = (
                    "https://www.cgesp.org/v3/alagamentos.jsp?dataBusca="
                    + dia
                    + "/"
                    + mes
                    + "/"
                    + ano
                    + "+&enviaBusca=Buscar"
                )

                response = get(url_base)
                soup = BeautifulSoup(response.text, "html.parser")

                lista_alagamentos = soup.find_all(
                    class_="tb-pontos-de-alagamentos"
                )

                if len(lista_alagamentos) == 0:
                    print("Não há alagamentos neste dia!")

                else:
                    # -------find flood list-------
                    for j in lista_alagamentos:
                        pontos_alagamentos = j.find_all(
                            class_="ponto-de-alagamento"
                        )

                        # -------find flood point-------
                        for k in pontos_alagamentos:
                            # -------find status-------
                            if (k.find(class_="ativo-transitavel")) or (
                                k.find(class_="inativo-transitavel")
                            ):
                                status = "transitavel"
                            elif (k.find(class_="ativo-intransitavel")) or (
                                k.find(class_="inativo-intransitavel")
                            ):
                                status = "intransitavel"

                            # -------find addres and reference-------
                            end_ref = k.find_all(class_="arial-descr-alag")

                            cont_end_ref = 0
                            for l in end_ref:
                                features = l.find_all(text=True)

                                cont_features = 0
                                for m in features:
                                    if cont_end_ref == 0 and cont_features == 0:
                                        periodo = m
                                    elif cont_end_ref == 1 and cont_features == 0:
                                        endereco = m
                                    elif cont_end_ref == 0 and cont_features == 1:
                                        sentido = m
                                    elif cont_end_ref == 1 and cont_features == 1:
                                        referencia = m

                                    cont_features += 1
                                cont_end_ref += 1

                            # --------------------Save into DF--------------------
                            tam = len(df) + 1

                            df.loc[tam, "data"] = i
                            df.loc[tam, "periodo"] = periodo
                            df.loc[tam, "endereco"] = endereco
                            df.loc[tam, "sentido"] = sentido
                            df.loc[tam, "referencia"] = referencia
                            df.loc[tam, "status"] = status
                            df.loc[tam, "url_base"] = url_base
                            df.loc[tam, "string"] = end_ref

                            print(tam)
                            print("--------------------------")
                            print("data: ", i)
                            print("periodo: ", periodo)
                            print("endereco: ", endereco)
                            print("sentido: ", sentido)
                            print("referencia: ", referencia)
                            print("status: ", status)
                            print("url_base: ", url_base)
                            print("string: ", end_ref)
                            print("--------------------------")

            self.df = df

        except Exception as e:
            pass

    def persistir(self) -> None:
        try:
            self.df.to_csv("dados_geograficos.csv")

        except Exception as e:
            print(e)
            pass


# ConcreteCreator
class Floods_Scrapper_Factory(Web_Scrapper_Factory):
    def createScrapper(self) -> Web_Scrapper:
        return Scrapper_Floods()


if __name__ == "__main__":

    floods_scrapper_factory = Floods_Scrapper_Factory()
    scrapper_floods = floods_scrapper_factory.createScrapper()
    scrapper_floods.config(data_inf = "01/10/2019", data_sup = "31/10/2019")
    scrapper_floods.scrapping()
