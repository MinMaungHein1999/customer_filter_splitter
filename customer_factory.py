from abc import ABC, abstractmethod
from customer import Customer
from typing import List

class CustomerFactory(ABC):
    @abstractmethod
    def create_customer(self) -> Customer:
        pass
