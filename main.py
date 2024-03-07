from src.classes_API import HHAPI

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
    input('____\nВведите поисковый запрос для запроса вакансий: ')
    input('Введите количество вакансий для вывода в топ N: ')
    input('Введите ключевые слова для поиска в описании: ')
    input('Введите диапазон зарплат: ')

    pass


def hh_ru_user_interface():

    print('Программа для поиска и обработки вакансий')

    while True:

        platform_no = int(input('____\nВыберите платформу: 1="hh", 2="Из файла JSON"'))

        if platform_no == 1:
            collect_user_parameters()

            hh_api = HHAPI()
            result = hh_api.get_vacancies()
            print(result)

        elif platform_no == 2:
            pass
            collect_user_parameters()

        else:
            print("Некорректный ввод")

        if input('Хотите запустить новый поиск? y/n: ') != 'y':
            break


hh_ru_user_interface()

