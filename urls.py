import requests

BASE_URL = 'https://qa-scooter.praktikum-services.ru'
COURIER_CREATION_URL = f'{BASE_URL}/api/v1/courier'
COURIER_LOGIN_URL = f'{BASE_URL}/api/v1/courier/login'
ORDER_CREATION_URL = f'{BASE_URL}/api/v1/orders'
ORDER_LIST_URL = f'{BASE_URL}/api/v1/orders'

class CourierRequest:

    def create_courier(payload):
        return requests.post(COURIER_CREATION_URL, json=payload)
    
    def login_courier(payload):
        return requests.post(COURIER_LOGIN_URL, json=payload)
    
class OrderRequest:

    def get_order_list():
        return requests.get(ORDER_LIST_URL)
    
    def create_order(order_data):
        return requests.post(ORDER_CREATION_URL, json = order_data)