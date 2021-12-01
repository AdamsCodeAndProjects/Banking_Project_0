from abc import ABC

from data_access_layer.implementation_classes.customer_postgres_dao import CustomerPostgresDAO
from entities.customers import Customer
from service_layer.abstract_services.customer_service import CustomerService


class CustomerPostgresImp(CustomerService, ABC):
    def __init__(self, customer_dao: CustomerPostgresDAO):
        self.customer_dao = customer_dao

    def service_create_customer_entry(self, customer: Customer) -> Customer:
        customers = self.customer_dao
        return customers

    def service_update_customer_by_id(self, customer_id: int) -> Customer:
        customers = self.customer_dao
        return customers