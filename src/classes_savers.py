from abc import ABC, abstractmethod
import json


class SaverABC(ABC):

    @abstractmethod
    def __init__(self):
        pass


class SaverJSON(SaverABC):

    def __init__(self, filename):
        self.filename = filename

    def save(self, list_data, mode='w'):  # 'a' or 'w'

        if mode == 'a':
            old_set = set(self.load())
            for vacancy in list_data:
                old_set.add(vacancy)
            new_list = list(old_set)
            list_data = new_list

        dict_data = [item.convert_to_dict() for item in list_data]

        with open(self.filename, 'w', encoding="UTF-8") as f:
            json.dump(dict_data, f, indent=2, ensure_ascii=False)

    def load(self):
        with open(self.filename, encoding="UTF-8") as f:
            new_data = json.load(f)

        return new_data

    def __del__(self):
        with open(self.filename, 'w', encoding="UTF-8") as f:
            f.write('')


class SaverTXT(SaverABC):

    def __init__(self):
        pass

