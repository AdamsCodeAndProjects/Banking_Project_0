# API folder
"""
As a customer, I can create a new bank account with a starting balance. (create_account)
As a customer, I can view the balance of a specific account. (get_account_by_id)
As a customer, I can make a withdrawal or deposit to a specific account.
(deposit_into_account_by_id, withdraw_from_account_by_id)
As a customer, I can transfer money between accounts (transfer_money_between_accounts_by_their_ids)
As a customer, I can update my personal information (update_customer_by_id)
As a customer, I can view my personal information (get_customer_by_id)
As a customer, I can close any of my bank accounts (delete_account_by_id)
As a customer, I can end my business relationship with the bank (delete_customer_by_id)
As the system, I reject invalid transactions.
Ex:
A withdrawal that would result in a negative balance.
A deposit or withdrawal of negative money.
"""
from flask import Flask, request, jsonify

from custom_exceptions.duplicate_exceptions import DuplicateAccountIDException, DuplicateCustomerIDException
from data_access_layer.implementation_classes.account_dao_implementation import AccountDAOImp
from data_access_layer.implementation_classes.customer_dao_implementation import CustomerDAOImp
from entities.accounts import Account
from entities.customers import Customer
from service_layer.implementation_services.account_service_imp import AccountServiceImp
from service_layer.implementation_services.customer_service_imp import CustomerServiceImp

app = Flask(__name__)

customer_dao = CustomerDAOImp()
customer_service = CustomerServiceImp(customer_dao)
account_dao = AccountDAOImp()
account_service = AccountServiceImp(account_dao)


@app.route("/customer", methods=["post"])
def create_customer_entry():
    try:
        customer_data = request.get_json()
        new_customer = Customer(
            customer_data["firstName"],
            customer_data["lastName"],
            customer_data["dateOfBirth"],
            customer_data["customerId"],
            customer_data["accountId"]
        )
        customer_to_return = customer_service.service_create_customer_entry(new_customer)
        customer_as_dictionary = customer_to_return.make_customer_dictionary()
        customer_as_json = jsonify(customer_as_dictionary)
        return customer_as_json

    except DuplicateAccountIDException as e:

        # can either pass a str or a json
        exception_dictionary = {"message": str(e)}
        exception_json = jsonify(exception_dictionary)
        return exception_json

    # get customer info


@app.get("/customer/<customer_id>")
def get_customer_by_id(customer_id: str):
    result = customer_service.service_get_customer_by_id(int(customer_id))
    result_as_dictionary = result.make_customer_dictionary()
    result_as_json = jsonify(result_as_dictionary)
    return result_as_json


# def get_all_customers_information():
#     pass
#
#     # update info

@app.patch("/customer/<customer_id>")
def update_customer_by_id(customer_id: str):
    try:
        customer_data = request.get_json()
        new_customer = Customer(
            customer_data["firstName"],
            customer_data["lastName"],
            customer_data["dateOfBirth"],
            int("customerId"),
            customer_data["accountId"]
        )
        updated_customer = customer_service.service_update_customer_by_id(new_customer)
        return "Customer updated successfully.  The customer info is now " + str(updated_customer)
    except DuplicateCustomerIDException as e:
        return str(e)


@app.delete("/customer/<customer_id>")
def delete_customer_by_id(customer_id: str):
    result = customer_service.service_delete_customer_by_id(int(customer_id))
    if result:
        return "Customer with ID of {} was deleted successfully".format(customer_id)
    else:
        return "Something went wrong.  Customer with ID of {} was not deleted".format(customer_id)


@app.post("/account")
def create_account():
    try:
        body = request.get_json()
        new_account = Account(
            body["accountId"],
            body["amountInAccount"],
            body["amountInSecondAccount"]
        )
        newly_created_account = account_service.service_create_account(new_account)
        created_account_as_dictionary = newly_created_account.make_account_dictionary()
        return jsonify(created_account_as_dictionary), 201

    except DuplicateAccountIDException as e:

        error_message = {"errorMessage": str(e)}
        return jsonify(error_message), 400


@app.get("/account/<account_id>")
def get_account_by_id(account_id: str):
    account = account_service.service_get_account_by_id(int(account_id))
    account_as_dictionary = account.make_account_dictionary()
    return jsonify(account_as_dictionary), 200


@app.patch("/account/<account_id>")
def deposit_into_account_by_id(account_id: str):
    try:
        account_data = request.get_json()
        new_update = Account(
            account_data["accountId"],
            account_data["amountInAccount"],
            account_data["amountInSecondAccount"]
        )
        updated_account = account_service.service_deposit_into_account_by_id(account_id)
        return "Account updated successfully.  The account info is now " + str(new_update)
    except DuplicateAccountIDException as e:
        return str(e)


@app.patch("/account/<account_id>")
def withdraw_from_account_by_id(account_id: str):
    try:
        account_data = request.get_json()
        new_update = Account(
            account_data["accountId"],
            account_data["amountInAccount"],
            account_data["amountInSecondAccount"]
        )
        updated_account = account_service.service_withdraw_from_account_by_id(account_id)
        return "Account updated successfully.  The account info is now " + str(new_update)
    except DuplicateAccountIDException as e:
        return str(e)


@app.patch("/account/<account_id>")
def transfer_money_between_accounts_by_their_ids(account_id: str, transfer_amount: str):
    try:
        account_data = request.get_json()
        new_update = Account(
            account_data["accountId"],
            account_data["amountInAccount"],
            account_data["amountInSecondAccount"]
        )
        updated_account = account_service.service_transfer_money_between_accounts_by_their_ids(account_id)
        return "Account updated successfully.  The account info is now " + str(new_update)
    except DuplicateAccountIDException as e:
        return str(e)


@app.delete("/account/<account_id>")
def delete_account_by_id(account_id: str):
    result = account_service.service_delete_account_by_id(int(account_id))
    if result:
        return "Account ID of {} has been deleted".format(account_id)
    else:
        return "Something went wrong:  Account ID of {} was not deleted".format(account_id)


app.run()
