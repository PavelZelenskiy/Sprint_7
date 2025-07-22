import pytest
import requests

from helper.creat_new_courier import CreateNewCourier
from urls import *

@pytest.fixture
def courier_data():
    courier_data = CreateNewCourier.register_new_courier_and_return_login_password()
    return courier_data

@pytest.fixture
def delete_courier(courier_data):
    yield
    requests.delete(f'{COURIER_CREATION_URL}/{courier_data[0]}')