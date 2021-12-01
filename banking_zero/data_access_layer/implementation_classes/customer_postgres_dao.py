from data_access_layer.abstract_classes.customer_dao import CustomerDataAccessObject
from entities.customers import Customer
from util.database_connection import connection


class CustomerPostgresDAO(CustomerDataAccessObject):

    def create_customer_entry(self, customer: Customer) -> Customer:
        sql = """INSERT INTO customer VALUES(%s, %s, %s, default, %s)
        returning customer_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (customer.first_name, customer.last_name, customer.date_of_birth, customer.account_id))
        connection.commit()
        customer_id = cursor.fetchone()[0]
        customer.customer_id = customer_id
        return customer

    def get_customer_by_id(self, customer_id: int) -> Customer:
        sql = "select * from customer where customer_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id])
        customer_record = cursor.fetchone()
        customer = Customer(*customer_record)
        return customer

    def update_customer_by_id(self, customer_id: int) -> Customer:
        pass

    def delete_customer_by_id(self, customer_id: int) -> bool:
        pass
