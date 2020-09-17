from bs4 import BeautifulSoup
import requests


class VkBot:
    def __init__(self):
        print("Alina was born")
        self._commands = ["алина говорит..."]

    @staticmethod
    def _get_user_name(user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        parsed_text = BeautifulSoup(request.text, 'lxml')
        user_name = parsed_text.find_all("title")[0].text
        return user_name.split()[0]

    @staticmethod
    def _get_time():
        request = requests.get("https://my-calend.ru/date-and-time-today")
        parsed_text = BeautifulSoup(request.text, 'lxml')
        time = parsed_text.select(".page")[0].findAll("h2")[1].text.split()[1]
        time = time[:-1]
        time = time[:-1]
        return time[:-1]

    @staticmethod
    def _get_day():
        request = requests.get("http://www.xn--80aajbde2dgyi4m.xn--p1ai/")
        parsed_text = BeautifulSoup(request.text, 'lxml')
        day = parsed_text.find("p", id="day").text
        return day

    def _get_info(self):
        request = requests.get('https://itmo.ru/ru/schedule/0/M3206/raspisanie_zanyatiy_M3206.htm')
        parsed_text = BeautifulSoup(request.text, 'html5lib')
        if parsed_text.find("strong").text == 'нечетная':
            request = requests.get('https://itmo.ru/ru/schedule/0/M3206/2/raspisanie_zanyatiy_M3206.htm')
        else:
            request = requests.get('https://itmo.ru/ru/schedule/0/M3206/1/raspisanie_zanyatiy_M3206.htm')
        parsed_text = BeautifulSoup(request.text, 'html5lib')
        switch = {
            'Понедельник': '1day',
            'Вторник': '2day',
            'Среда': '3day',
            'Четверг': '4day',
            'Пятница': '5day',
            'Суббота': '6day',
            'Воскресенье': '7day',
        }
        more_lessons = False
        temp_lesson = ""
        if parsed_text.find("table", id=switch.get(self._get_day())) is not None:
            temp_day = parsed_text.find("table", id=switch.get(self._get_day()))
            for tag in temp_day.find("tbody").find_all("tr"):
                if tag.select_one(".time") is not None:
                    time = tag.select_one(".time").find("span").text.split('-')
                    if time[0] >= self._get_time() and not more_lessons:
                        more_lessons = True
                        temp_lesson = tag.select_one(".lesson").find("dd").text
                    if time[0] <= self._get_time() <= time[1]:
                        lesson = tag.select_one(".lesson").find("dd").text
                        teacher = tag.select_one(".lesson").find("b").text.replace('\n', "").replace(" ", "")
                        if teacher == "":
                            return "Выпиваем с таинственным незнакомцем"
                        return lesson
            if more_lessons:
                return "Попиваем пивко в ожидании пары (" + temp_lesson + ")"
        return "Сегодня отдыхаем. Пивко попиваем. С бюджета слетаем"

    def new_message(self, message):
        if message.lower() == self._commands[0]:
            return self._get_info()
        return "no"