import pandas as pd
from bs4 import BeautifulSoup
from requests import get

from web_scrapper import Web_Scrapper, Web_Scrapper_Factory


# ConcreteProduct
class ITI_Scrapper_Cursos(Web_Scrapper):
    
    def config(self):
        
        url_base = "https://iti.ufscar.mba/"

        response = get(url_base)

        response.encoding = "UTF-8"

        self.soup = BeautifulSoup(response.text,  "html.parser")
    
    def captar(self) -> None:
        try:
            url_base = "https://iti.ufscar.mba/"

            response = get(url_base)

            response.encoding = "UTF-8"

            soup = BeautifulSoup(response.text,  "html.parser")

            nossos_cursos = soup.find(id="nossos-cursos")

            container_default = nossos_cursos.find(class_="container-default")
            
            vector = []
            cursos_disponiveis = container_default.find_all(class_ = "box-curso")
            for i in cursos_disponiveis:
                if "ocultar" not in i["class"]:
                    vector.append(i.find(class_ = "h2-nome-do-curso").text)
            
            self.df = pd.DataFrame(columns = ["cursos"])
            self.df["cursos"] = vector

        except Exception as e:
            pass

    def persistir(self) -> None:
        try:
            self.df.to_csv("dados_iti_cursos.csv")

        except Exception as e:
            print(e)
            pass

# ConcreteProduct
class ITI_Scrapper_Professores(Web_Scrapper):
    
    def config(self):
        
        url_base = "https://iti.ufscar.mba/"

        response = get(url_base)

        response.encoding = "UTF-8"

        self.soup = BeautifulSoup(response.text,  "html.parser")
    

    def captar(self) -> None:
        try:

            nosso_time = self.soup.find(id="nosso-time")

            coluna_docentes = nosso_time.find(class_="fundo-coluna-docentes")

            #-----Professores da Academia-----

            professores_academia = coluna_docentes.find_all(class_ = "card-profs-home")

            vector_professores_academia = []
            vector_org_academia = []

            for i in professores_academia:
                professor = i.find(class_ = "h4-nome-professor").text
                org = i.find(class_ = "h5-org-prof").text

                vector_professores_academia.append(professor)
                vector_org_academia.append(org)

            #-----Professores do Mercado de Trabalho-----

            coluna_representantes = nosso_time.find(class_="fundo-coluna-representantes")


            professores_industria = coluna_representantes.find_all(class_ = "card-profs-home")

            vector_professores_industria = []
            vector_org_industria = []

            for i in professores_industria:
                professor = i.find(class_ = "h4-nome-professor").text
                org = i.find(class_ = "h5-org-prof").text

                vector_professores_industria.append(professor)
                vector_org_industria.append(org)


            self.df = pd.DataFrame(columns = ["professores", "instituicao"])

            vector_professores = vector_professores_academia + vector_professores_industria
            vector_org = vector_org_academia + vector_org_industria

            self.df["professores"] = vector_professores
            self.df["instituicao"] = vector_org

        except Exception as e:
            pass

    def persistir(self) -> None:
        try:
            self.df.to_csv("dados_iti_professores.csv")

        except Exception as e:
            print(e)
            pass

# ConcreteCreator
class ITI_Scrapper_Factory(Web_Scrapper_Factory):
    def createScrapper(self,tipo) -> Web_Scrapper:
        if tipo == "cursos":
            return ITI_Scrapper_Cursos()
        elif tipo == "professores":
            return ITI_Scrapper_Professores()
        else:
            raise ValueError
    

if __name__ == "__main__":

    iti_scrapper_factory = ITI_Scrapper_Factory()
    
    iti_scrapper_cursos = iti_scrapper_factory.createScrapper("cursos")
    iti_scrapper_cursos.config()
    iti_scrapper_cursos.scrapping()

    iti_scrapper_professores = iti_scrapper_factory.createScrapper("professores")
    iti_scrapper_professores.config()
    iti_scrapper_professores.scrapping()
