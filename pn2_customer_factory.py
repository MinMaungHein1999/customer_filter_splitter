from customer_factory import CustomerFactory
from pn2_customer_dao import Pn2CustomerDao

class Pn2CustomerFactory(CustomerFactory):

    def __init__(self, table_name, region_name, customer_array, bucket, file_name):
        self.pn2_customer_dao = Pn2CustomerDao(table_name, region_name, customer_array, bucket, file_name)

    def create_customer(self):
        self.pn2_customer_dao.save_customer_to_dynamodb()