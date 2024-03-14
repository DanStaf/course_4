from datetime import datetime


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
        return f"Vacancy: {self.name} / {self.published_at}"

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

##################
