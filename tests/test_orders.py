import requests
import pytest
import allure

from urls import *
from data.order_data import *
from helper.order_fields_validation import OrderValidation



class TestGetOrdersList:

    @allure.title('Проверка ответа на запрос списка заказов без передачи courierId')
    def test_get_orders_list_no_courierId(self):
        
        response = OrderRequest.get_order_list()
        assert response.status_code == 200, f'Статус код ответа - {response.status_code}'

        orders_list = response.json()
        assert 'orders' in orders_list, 'В ответе отсутсвует ключ "orders"'
        assert isinstance(orders_list['orders'], list), 'Ключ "orders" не является списком'

        assert len(orders_list['orders']) > 0, 'Список заказов пуст'

        field, order = OrderValidation.field_in_order_validation(orders_list['orders'], order_required_fields)
        assert field in order, f'У заказа {order.get('id', 'без ID')} отсутствует обязательное поле "{field}"'

class TestCreateOrder:
    
    @allure.title(f'Проверка создания заказа при передаче различных сочетаний цветов - {order_data_colors}')
    @pytest.mark.parametrize('color', order_data_colors)
    def test_create_order_different_colors(self, color):

        order_data["color"] = color
        response = OrderRequest.create_order(order_data)

        assert response.status_code == 201, f'Статус код ответа - {response.status_code}'

        response_body = response.json()
        assert "track" in response_body, 'В ответе отсутствует поле "track"'
        assert isinstance(response_body["track"], int), 'Поле "track" не является числом'
        


