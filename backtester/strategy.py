from abc import ABC, abstractmethod

class Strategy(ABC): 
    @abstractmethod
    def generate_signal(self,data_so_far): 
        """
        """
        ...