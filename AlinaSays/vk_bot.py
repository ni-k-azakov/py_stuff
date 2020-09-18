from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pytz


class VkBot:
    def __init__(self):
        print("Alina was born")
        self._commands = ["!алина", "!алина завтра", "!алина сегодня", "!команды", "!обновление", "понимаю",
                          "!обновления"]
        request = requests.get('https://itmo.ru/ru/schedule/0/M3206/raspisanie_zanyatiy_M3206.htm')
        self._itmo_schedule = BeautifulSoup(request.text, 'lxml')
        request = requests.get("http://www.xn--80aajbde2dgyi4m.xn--p1ai/")
        parsed_text = BeautifulSoup(request.text, 'lxml')
        day = parsed_text.find("p", id="day").text
        self._prev_day = day

    @staticmethod
    def _get_time():
        tz = pytz.timezone('Europe/Moscow')
        time = datetime.now(tz=tz).strftime('%H:%M:%S')
        time = time[:-1]
        time = time[:-1]
        return time[:-1]

    def _get_day(self):
        request = requests.get("http://www.xn--80aajbde2dgyi4m.xn--p1ai/")
        parsed_text = BeautifulSoup(request.text, 'lxml')
        day = parsed_text.find("p", id="day").text
        return day

    def _get_info(self):
        if self._itmo_schedule.find("strong").text == 'нечетная':
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
        temp_day = parsed_text.find("table", id=switch.get(self._get_day()))
        if temp_day is not None:
            for tag in temp_day.find("tbody").find_all("tr"):
                temp_time = tag.select_one(".time")
                if temp_time is not None:
                    time = temp_time.find("span").text.split('-')
                    lesson_block = tag.select_one(".lesson").find("dd").text
                    if time[0] >= self._get_time() and not more_lessons:
                        more_lessons = True
                        temp_lesson = lesson_block
                    if time[0] <= self._get_time() <= time[1]:
                        lesson = lesson_block
                        teacher = tag.select_one(".lesson").find("b").text.replace('\n', "").replace(" ", "")
                        if teacher == "":
                            return "Выпиваю с незнакомцем, ведущим " + lesson + " (" + time[0] + "-" + time[1] + ")"
                        output_teacher = ""
                        for letter in teacher:
                            if letter.lower() != letter:
                                output_teacher += ' '
                            output_teacher += letter
                        return "Закрепляю пивом " + lesson + " (" + time[0] + "-" + time[1] + ")" + output_teacher
                if more_lessons:
                    time = temp_time.find("span").text.split('-')
                    return "Попиваю пивко в ожидании пары (" + temp_lesson + ")\nНачало в " + time[0]
        return "Сейчас отдыхаю. Пивко попиваю. Тейлор снимаю"

    def _day_info(self, which_day):
        switch = {
            0: '1day',
            1: '2day',
            2: '3day',
            3: '4day',
            4: '5day',
            5: '6day',
            6: '7day',
        }
        switch2 = {
            'Понедельник': 0,
            'Вторник': 1,
            'Среда': 2,
            'Четверг': 3,
            'Пятница': 4,
            'Суббота': 5,
            'Воскресенье': 6,
        }
        if switch.get(self._get_day()) != 'Воскресенье':
            if self._itmo_schedule.find("strong").text == 'нечетная':
                request = requests.get('https://itmo.ru/ru/schedule/0/M3206/2/raspisanie_zanyatiy_M3206.htm')
            else:
                request = requests.get('https://itmo.ru/ru/schedule/0/M3206/1/raspisanie_zanyatiy_M3206.htm')
        else:
            if self._itmo_schedule.find("strong").text == 'нечетная':
                request = requests.get('https://itmo.ru/ru/schedule/0/M3206/1/raspisanie_zanyatiy_M3206.htm')
            else:
                request = requests.get('https://itmo.ru/ru/schedule/0/M3206/2/raspisanie_zanyatiy_M3206.htm')
        parsed_text = BeautifulSoup(request.text, 'html5lib')
        temp_day = parsed_text.find("table", id=switch.get(switch2.get(self._get_day()) + which_day))
        table = ""
        if which_day == 0:
            table = "Сегодня пью на:\n"
        elif which_day == 1:
            table = "Завтра буду пить на:\n"
        if temp_day is not None:
            for tag in temp_day.find("tbody").find_all("tr"):
                temp_time = tag.select_one(".time")
                if temp_time is not None:
                    time = temp_time.find("span").text.split('-')
                    lesson_block = tag.select_one(".lesson").find("dd").text
                    teacher = tag.select_one(".lesson").find("b").text.replace('\n', "").replace(" ", "")
                    table += lesson_block + " (" + time[0] + "-" + time[1] + ")"
                    output_teacher = ""
                    if teacher != "":
                        for letter in teacher:
                            if letter.lower() != letter:
                                output_teacher += ' '
                            output_teacher += letter
                    table += output_teacher + '\n----\n'
            return table
        return "Сегодня отдыхаю. Пивко попиваю. Тейлор снимаю"

    def _command_info(self):
        return "Список команд:\n1) !алина - ближайшая пара на сегодня\n2) !алина сегодня - расписание на сегодня\n3) " \
               "!алина завтра - расписание на завтра\n4) !обновление - новости о последнем обновлении"

    def _update(self):
        return "Update:\n1) Команда `алина говорит` изменена на !алина\n2) Новая команда: !алина сегодня\n3) Новая " \
               "команда: !алина завтра\n4) Новая команда: !команды"

    def new_message(self, message):
        switch_time = {
            'Понедельник': 0,
            'Вторник': 1,
            'Среда': 2,
            'Четверг': 3,
            'Пятница': 4,
            'Суббота': 5,
            'Воскресенье': 6,
        }
        if switch_time.get(self._prev_day) > switch_time.get(self._get_day()):
            self._prev_day = self._get_day()
            request = requests.get('https://itmo.ru/ru/schedule/0/M3206/raspisanie_zanyatiy_M3206.htm')
            self._itmo_schedule = BeautifulSoup(request.text, 'lxml')
        if message.lower() == self._commands[0]:
            return self._get_info()
        if message.lower() == self._commands[1]:
            return self._day_info(1)
        if message.lower() == self._commands[2]:
            return self._day_info(0)
        if message.lower() == self._commands[3]:
            return self._command_info()
        if message.lower() == self._commands[4] or message.lower() == self._commands[6]:
            return self._update()
        if message.lower() == self._commands[5]:
            return "Спасибо за понимание"
        return "no"
