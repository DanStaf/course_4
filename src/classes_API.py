from abc import ABC, abstractmethod
import requests
import json
from src.classes_vacancy import Vacancy

class AbcAPI(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HHAPI(AbcAPI):

    def __init__(self, user_parameters, is_token_needed=False, token_force_update=False):
        self.token = self.receive_token(is_token_needed, token_force_update)
        self.parameters = user_parameters

    @staticmethod
    def receive_token(is_token_needed: bool, token_force_update: bool):
        """
        Данный access_token имеет неограниченный срок жизни.
        При повторном запросе ранее выданный токен отзывается и выдается новый.
        Запрашивать access_token можно не чаще, чем один раз в 5 минут
        """

        if is_token_needed:
            with open('../data/API_token.json') as f:
                data = json.loads(f.read())

            if ('HH_API_TOKEN' in data) and not token_force_update:
                token = data['HH_API_TOKEN']
            else:
                if ('HH_CLIENT_ID' in data) and ('HH_CLIENT_SECRET' in data):
                    client_id = data['HH_CLIENT_ID']
                    client_secret = data['HH_CLIENT_SECRET']

                    grant_type = 'client_credentials'
                    parameters = f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}"
                    url_post = "https://api.hh.ru/token"  # используемый адрес для отправки запроса

                    response = requests.post(url_post, params=parameters)  # отправка POST-запроса

                    if response.status_code == 200:
                        token = response.json()['access_token']
                    else:
                        print('Токен не получен от HH.RU. Продолжим без токена')
                        token = None
                else:
                    print('Приложение не зарегистрировано на HH.RU. Продолжим без токена')
                    token = None
        else:
            token = None

        return token

    def get_vacancies(self):

        if self.token is not None:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'HH-User-Agent': 'Vacancies Manager (danstaf@mail.ru)'
            }
        else:
            headers = {}

        parameters = {'text': 'python'}

        url_get = 'https://api.hh.ru/vacancies'

        response = requests.get(url_get, params=parameters, headers=headers)

        if response.status_code == 200:
            vacancies = response.json()['items']

            with open("data/response_result.json", 'w', encoding="UTF-8") as f:
                json.dump(vacancies, f, indent=2, ensure_ascii=False)

            return [Vacancy(item['name'],
                            item['snippet']['requirement'],
                            item['snippet']['responsibility'],
                            item['salary'],
                            item['experience'],
                            item['employment'],
                            item['url'],
                            item['published_at'],
                            item['employer'],
                            item['address']
                            ) for item in vacancies]

        else:
            print('Ошибка получения вакансий от HH.RU.')
            return None

######################
