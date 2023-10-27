import requests


class BaseWorker:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.endpoints = {
            'login': server_url + '/login',
            'register': server_url + '/register',
            'create_employee': server_url + '/employee_create',
        }

    def login(self, email: str, password: str) -> dict:
        json_data = {
            'email': email, 
            'password': password
        }
        response = requests.post(self.endpoints['login'], json=json_data)
        return response.json()

    def register(self, email: str, password: str) -> dict:
        json_data = {
            'email': email,
            'password': password
        }
        response = requests.post(self.endpoints['register'], json=json_data)
        return response.json()

    def create_employee(
        self,
        position: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str
    ) -> dict:
        json_data = {
            'user_in': {
                'email': email, 
                'password': password
            },
            'employee_in': {
                'position': position,
                'first_name': first_name,
                'last_name': last_name
            }
        }
        response = requests.post(self.endpoints['create_employee'], json=json_data)
        return response.json()


base_worker = BaseWorker('http://127.0.0.1:8000')
