from abc import ABC, abstractmethod

class Customer(ABC):     
    def __init__(self, policy_number, branch_number, name_katakana, name_kanji, 
                 phone_number1, address_kanji, policy_term_effective_date, policy_term_end_date):
        self.policy_number = policy_number
        self.branch_number = branch_number
        self.name_katakana = name_katakana
        self.name_kanji = name_kanji
        self.address_kanji = address_kanji
        self.phone_number1 = phone_number1
        self.policy_term_effective_date = policy_term_effective_date
        self.policy_term_end_date = policy_term_end_date

    def set_customer(self, customer):
        self.policy_number = customer.policy_number
        self.branch_number = customer.branch_number
        self.name_katakana = customer.name_katakana
        self.name_kanji = customer.name_kanji
        self.address_kanji = customer.address_kanji
        self.phone_number1 =customer.phone_number1
        self.policy_term_effective_date = customer.policy_term_effective_date
        self.policy_term_end_date = customer.policy_term_end_date
