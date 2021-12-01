from data_access_layer.implementation_classes.account_dao_implementation import AccountDAOImp
from entities.accounts import Account

account_dao = AccountDAOImp()
test_account = Account(0, 500, 0)
test_account_two = Account(5, 3000, 0)


def test_create_account_success():
    created_account = account_dao.create_account(test_account)
    assert created_account.account_id != 0


def test_get_account_by_id_success():
    selected_account = account_dao.get_account_by_id(1)
    assert selected_account.account_id == 1


def test_deposit_into_account_by_id_success():
    depositing_account = account_dao.deposit_into_account_by_id(2, 400)
    assert depositing_account.amount_in_account == 600


def test_withdraw_from_account_by_id_success():
    withdraw_account = account_dao.withdraw_from_account_by_id(3, 1)
    assert withdraw_account.amount_in_account == 49


def test_transfer_money_between_accounts_by_their_ids_success():
    transfer_account = account_dao.transfer_money_between_accounts_by_their_ids(4, 50)
    assert transfer_account.amount_in_account == 150


def test_delete_account_by_id_success():
    result = account_dao.delete_account_by_id(3)
    assert result
