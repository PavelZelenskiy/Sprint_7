import requests
import pytest
import allure

from urls import *
from data.order_data import *

class TestOrders:

    class TestGetOrdersList:

        @allure.title('Проверка ответа на запрос списка заказов без передачи courierId')
        def test_get_orders_list_no_courierId(self):
            
            response = requests.get(ORDER_LIST_URL)
            assert response.status_code == 200, f'Статус код ответа - {response.status_code}'

            orders_list = response.json()
            assert 'orders' in orders_list, 'В ответе отсутсвует ключ "orders"'
            assert isinstance(orders_list['orders'], list), 'Ключ "orders" не является списком'

            assert len(orders_list['orders']) > 0, 'Список заказов пуст'

            for order in orders_list['orders']:
                for field in order_required_fields:
                    assert field in order, f'У заказа {order.get('id', 'без ID')} отсутствует обязательное поле "{field}"'

    class TestCreateOrder:
        
        @allure.title(f'Проверка создания заказа при передаче различных сочетаний цветов - {order_data_colors}')
        @pytest.mark.parametrize('color', order_data_colors)
        def test_create_order_different_colors(self, color):

            order_data["color"] = color
            response = requests.post(ORDER_CREATION_URL, json = order_data)

            assert response.status_code == 201, f'Статус код ответа - {response.status_code}'

            response_body = response.json()
            assert "track" in response_body, 'В ответе отсутствует поле "track"'
            assert isinstance(response_body["track"], int), 'Поле "track" не является числом'
        


