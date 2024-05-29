import json
from customer import Customer
class Pn2Customer(Customer):
    def __init__(self, policy_number=None, branch_number=None, name_katakana=None, name_kanji=None, phone_number1=None, 
                 address_kanji=None, policy_term_effective_date=None,  policy_term_end_date=None,
                 vehicle_info=None):
        
        super().__init__(policy_number, branch_number, name_katakana, name_kanji, phone_number1, 
                        address_kanji, policy_term_effective_date, policy_term_end_date)
        
        self.vehicle_info = vehicle_info

    def set_pn2_customer(self, customer, vehicle_info):
        self.set_customer(customer)
        self.vehicle_info = vehicle_info
        return self

    def to_dict(self):
        policy_number_trimmed = self.policy_number.rstrip()
        branch_number_trimmed = self.branch_number.rstrip()
        policy_number_and_branch = f"{policy_number_trimmed}#{branch_number_trimmed}".replace(" ", "")

        return {
            'Customer': 'Customer',
            'PolicyNumberAndBranchNumber': policy_number_and_branch,
            'PolicyNumber': self.policy_number,
            'BranchNumber': self.branch_number,
            'NameKatakana': self.name_katakana,
            'NameKanji': self.name_kanji,
            'Address': self.address_kanji,
            'PhoneNumber1': self.phone_number1,
            'PolicyTermEffectiveDate': self.policy_term_effective_date,
            'PolicyTermEndDate': self.policy_term_end_date,
            'NumberPlate1': self.vehicle_info.number_plate1,
            'NumberPlate2': self.vehicle_info.number_plate2,
            'NumberPlate3': self.vehicle_info.number_plate3,
            'NumberPlate4': self.vehicle_info.number_plate4,
            'NumberPlate5': self.vehicle_info.number_plate5,
            'NumberPlate6': self.vehicle_info.number_plate6,
            'VehicleName': self.vehicle_info.vehicle_name
        }
