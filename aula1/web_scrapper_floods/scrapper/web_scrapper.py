from abc import ABC, abstractmethod
from singleton import Singleton

# Product
class Web_Scrapper(Singleton):

    @abstractmethod
    def config(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def captar(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def persistir(self) -> None:
        raise NotImplementedError

    def scrapping(self) -> None:
        self.captar()
        self.persistir()


# Creator
class Web_Scrapper_Factory(Singleton):
    
    @abstractmethod
    def createScrapper(self) -> Web_Scrapper:
        raise NotImplementedError
