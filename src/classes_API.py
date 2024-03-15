from abc import ABC, abstractmethod
import requests
import json
from src.classes_vacancy import Vacancy
from src.classes_aux import UserParameters


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

        self.text = user_parameters.text
        self.per_page = user_parameters.per_page
        self.experience = user_parameters.experience
        self.salary = user_parameters.salary

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

        parameters = {'text': self.text,
                      'currency': 'RUR',
                      'order_by': 'salary_desc'
                      }

        if self.per_page:
            parameters['per_page'] = self.per_page
        if self.experience:
            parameters['experience'] = self.experience
        if self.salary:
            parameters['salary'] = self.salary

        print(parameters)

        url_get = 'https://api.hh.ru/vacancies'

        response = requests.get(url_get, params=parameters, headers=headers)

        if response.status_code == 200:
            vacancies = response.json()['items']

            return Vacancy.init_from_json(vacancies)

        else:
            result = response.json()['errors']
            print('Ошибка получения вакансий от HH.RU.', response.status_code, result)
            return None






"""
"vacancy_search_order": [
{
"id": "publication_time",
"name": "по дате"
},
{
"id": "salary_desc",
"name": "по убыванию дохода"
},
{
"id": "salary_asc",
"name": "по возрастанию дохода"
},
{
"id": "relevance",
"name": "по соответствию"
},
{
"id": "distance",
"name": "по удалённости"
}
],

"experience": [
{
"id": "noExperience",
"name": "Нет опыта"
},
{
"id": "between1And3",
"name": "От 1 года до 3 лет"
},
{
"id": "between3And6",
"name": "От 3 до 6 лет"
},
{
"id": "moreThan6",
"name": "Более 6 лет"
}
],
"""
        ######################
