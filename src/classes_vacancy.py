from datetime import datetime
from src.classes_aux import UserParameters

CURRENCY_RATES = {
    'RUR': 1,
    'USD': 91.87,
    'EUR': 99.97
}


class Vacancy:

    def __init__(self, name, requirement, responsibility,
                 salary, experience, employment,
                 url, published_at, employer, address):
        """
            "published_at": "2024-03-07T13:59:59+0300",
            "snippet": {
                "requirement": "",
                "responsibility": ""
            },
        """

        self.name = name
        self.requirement = requirement
        self.responsibility = responsibility

        self.salary = salary
        self.experience = experience
        self.employment = employment

        self.url = url
        self.published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S%z")
        self.employer = employer
        self.address = address

    def __repr__(self):
        return f"Vacancy: {self.name} / {self.get_salary()['text']} / {self.published_at.strftime("%Y-%m-%d %H:%M")}"

    def get_salary(self):
        compare = []
        if self.salary['from'] is not None:
            compare.append(self.salary['from'])
        if self.salary['to'] is not None:
            compare.append(self.salary['to'])
        if compare:
            value = max(compare)
            text = (str(value) + ' ' + self.salary['currency'] + ' ' +
                    ('gross' if self.salary['gross'] else 'net')
                    )
            value_rur = value*CURRENCY_RATES[self.salary['currency']]
        else:
            value = 0
            value_rur = 0
            text = 'Зарплата не задана'

        return {'value': value, 'text': text, 'value_rur': value_rur}

    def convert_to_dict(self):

        return {
            'name': self.name,
            'snippet': {
                'requirement': self.requirement,
                'responsibility': self.responsibility
            },
            'salary': self.salary,
            'experience': self.experience,
            'employment': self.employment,
            'url': self.url,
            'published_at': self.published_at.strftime("%Y-%m-%dT%H:%M:%S%z"),
            'employer': self.employer,
            'address': self.address
        }

    @classmethod
    def init_from_json(cls, vacancies_json):

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
                        ) for item in vacancies_json]

    @classmethod
    def filter_vacancies(cls, vacancies, user_parameters: UserParameters):

        filtered = []

        for vacancy in vacancies:

            if ((user_parameters.text in vacancy.name) or
                    (user_parameters.text in vacancy.requirement) or
                    (user_parameters.text in vacancy.responsibility)):
                if user_parameters.salary <= vacancy.get_salary()['value_rur']:
                    if user_parameters.experience is None:
                        filtered.append(vacancy)
                    else:
                        if user_parameters.experience == vacancy.experience['id']:
                            filtered.append(vacancy)

        filtered.sort(key=lambda s: s.get_salary()['value_rur'])

        return filtered[:user_parameters.per_page]

    def __gt__(self, other):
        a = self.get_salary()['value_rur']
        b = other.get_salary()['value_rur']

        return True if a > b else False

    def __lt__(self, other):
        a = self.get_salary()['value_rur']
        b = other.get_salary()['value_rur']

        return True if a < b else False

##################
