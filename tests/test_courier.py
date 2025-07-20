import pytest
import requests
import allure

from urls import *

class TestCourier:

    class TestCreateCourier:
        
        @allure.title('Проверка успешного создания курьера')
        @pytest.mark.usefixtures("delete_courier")
        def test_create_courier_success(self, courier_data):

            login, password, first_name = courier_data
            payload = {
            "login": login,
            "password": password,
            "firstName": first_name
            }
            
            response = requests.post(COURIER_CREATION_URL, json=payload)
            
            assert response.status_code == 201
            assert response.json() == {'ok': True}

        @allure.title('Проверка ответа при попытке создать существующего курьера')
        @pytest.mark.usefixtures("delete_courier")
        def test_create_courier_duplicate(self, courier_data):
            
            login, password, first_name = courier_data
            payload = {
            "login": login,
            "password": password,
            "firstName": first_name
            }

            response1 = requests.post(COURIER_CREATION_URL, json=payload)
            assert response1.status_code == 201

            response2 = requests.post(COURIER_CREATION_URL, json=payload)
            assert response2.status_code == 409

        @allure.title('Проверка ответа при попытке создать курьера без указания обязательного поля')
        @pytest.mark.usefixtures("delete_courier")
        @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
        def test_create_courier_missing_field(self, courier_data, missing_field):
                
                login, password, first_name = courier_data
                payload = {
                    "login": login,
                    "password": password,
                    "firstName": first_name
                }
                
                del payload[missing_field]
                
                response = requests.post(COURIER_CREATION_URL, json=payload)
                assert response.status_code == 400
                assert "message" in response.json()

    class TestLoginCourier:

        @allure.title('Проверка успешного входа систему курьером') 
        @pytest.mark.usefixtures("delete_courier")
        def test_login_courier_success(self, courier_data):
             
            login, password, first_name = courier_data
            payload = {
                "login": login,
                "password": password
            } 

            response = requests.post(COURIER_LOGIN_URL, json=payload)
            assert response.status_code == 200
            assert "id" in response.json()

        @allure.title('Проверка ответа при входе в систему курьера без указания обязательного поля')
        @pytest.mark.usefixtures("delete_courier")
        @pytest.mark.parametrize("missing_field", ["login", "password"])
        def test_login_courier_missing_field(self, courier_data, missing_field):
             
            login, password, first_name = courier_data
            payload = {
                "login": login,
                "password": password
            }

            del payload[missing_field] 

            response = requests.post(COURIER_LOGIN_URL, json=payload)
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для входа"

        @allure.title('Проверка ответа при входе в систему курьера с неправильной парой логин/пароль')
        def test_login_courier_wrong_creds(self):
             
            payload = {
                "login": "nonexistent_user",
                "password": "wrong_password"
            }
    
            response = requests.post(COURIER_LOGIN_URL, json=payload)
    
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена"

        @allure.title('Проверка ответа при входе в систему курьера с неправильным логином')
        @pytest.mark.usefixtures("delete_courier")
        def test_login_courier_wrong_login(self, courier_data):

            login, password, first_name = courier_data 
            payload = {
                "login": "nonexistent_user",
                "password": password
            }
    
            response = requests.post(COURIER_LOGIN_URL, json=payload)
    
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена"

        @allure.title('Проверка ответа при входе в систему курьера с неправильным паролем')
        @pytest.mark.usefixtures("delete_courier")
        def test_login_courier_wrong_password(self, courier_data):

            login, password, first_name = courier_data 
            payload = {
                "login": login,
                "password": "wrong_password"
            }
    
            response = requests.post(COURIER_LOGIN_URL, json=payload)
    
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена"