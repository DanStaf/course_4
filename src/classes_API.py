from abc import ABC, abstractmethod
import requests


class AbcAPI(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HHAPI(AbcAPI):

    def __init__(self):
        pass

    def get_vacancies(self):
        pass


def get_hh_token():
    url_post = "https://api.hh.ru/token"  # используемый адрес для отправки запроса

    response = requests.post(url_post)  # отправка POST-запроса

    print(response)  # вывод объекта класса Response
    print(response.status_code)  # вывод статуса запроса, 200 означает, что всё хорошо
    print(response.text)  # печать ответа в виде текста того, что вернул нам внешний сервис
    print(response.json())  # печать ответа в виде json объекта того, что нам вернул внешний сервис


get_hh_token()
