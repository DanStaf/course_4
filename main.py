from src.classes_API import HHAPI
from src.classes_aux import UserParameters
from src.classes_savers import SaverJSON
from src.classes_vacancy import Vacancy

"""
# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()

# Получение вакансий с hh.ru в формате JSON
hh_vacancies = hh_api.get_vacancies("Python")

# Преобразование набора данных из JSON в список объектов
vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

# Пример работы контструктора класса с одной вакансией
vacancy = Vacancy("Python Developer", "", "100 000-150 000 руб.", "Требования: опыт работы от 3 лет...")

# Сохранение информации о вакансиях в файл
json_saver = JSONSaver()
json_saver.add_vacancy(vacancy)
json_saver.delete_vacancy(vacancy)

# Функция для взаимодействия с пользователем

def user_interaction():
    platforms = ["HeadHunter"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)
"""


def collect_user_parameters():
    vacancy_name = input('____\nВведите поисковый запрос для запроса вакансий: ')
    vacancy_amount = input('Введите количество вакансий для вывода в топ N: ')
    vacancy_keywords = input('Введите опыт работы (количество лет >= 0): ')
    vacancy_salary = input('Введите уровень зарплаты: ')

    return UserParameters([vacancy_name, vacancy_amount, vacancy_keywords, vacancy_salary])


def temp_parameters_for_API():
    return UserParameters(['Python', '8', '', '100000'])


def temp_parameters_for_saver():
    return UserParameters(['Senior', '', '', '200000'])


def hh_ru_user_interface():

    print('Программа для поиска и обработки вакансий')
    saver = SaverJSON("data/response_result.json")

    while True:

        platform_no = int(input('____\nВыберите платформу: 1="hh", 2="Из файла JSON": '))

        if platform_no == 1:
            #user_parameters = collect_user_parameters()
            user_parameters = temp_parameters_for_API()

            hh_api = HHAPI(user_parameters)
            result = hh_api.get_vacancies()
            [print(item) for item in result]

            how_to_save = input('Добавить новые вакансии в файл (a), перезаписать файл (w) или пропустить (n)?')
            if how_to_save == 'a':
                saver.save(result, 'a')
            elif how_to_save == 'w':
                saver.save(result, 'w')
            else:
                pass

        elif platform_no == 2:
            #user_parameters = collect_user_parameters()
            user_parameters = temp_parameters_for_saver()

            vacancies = saver.load()

            result = Vacancy.init_from_json(vacancies)
            filtered = Vacancy.filter_vacancies(result, user_parameters)

            [print(item) for item in filtered]

        else:
            print("Некорректный ввод")

        if input('Хотите запустить новый поиск? y/n: ') != 'y':
            break


hh_ru_user_interface()

