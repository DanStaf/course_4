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
        self.published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S+%f")
        self.employer = employer
        self.address = address

    def __repr__(self):
        return f"Vacancy: {self.name} / {self.published_at}"
