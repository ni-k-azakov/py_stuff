# import requests
from datetime import datetime
import pytz
from deadline_container import DeadlineContainer


class VkBot:
    def __init__(self):
        print("Deadliner was born")
        self._commands = ["!создать", "!дедлайны", "!load", "!save"]
        self._phase = 0
        self._temp_deadline = ""
        self._temp_deadline_date = ""
        self._deadlines = {}

    @staticmethod
    def date_format(date) -> bool:
        parsed_date = date.split(".")
        if len(parsed_date) != 3:
            return False
        for token in parsed_date:
            try:
                int(token)
            except ValueError:
                return False
        return True

    @staticmethod
    def time_format(time) -> bool:
        parsed_time = time.split(":")
        if len(parsed_time) != 2:
            return False
        for token in parsed_time:
            try:
                int(token)
            except ValueError:
                return False
        return True

    @staticmethod
    def get_time() -> str:
        tz = pytz.timezone('Europe/Moscow')
        time = datetime.now(tz=tz).strftime('%H:%M:%S')
        time = time[:-1]
        time = time[:-1]
        return time[:-1]

    @staticmethod
    def command_info() -> str:
        return "Команды:\n1) !создать - создать новый дедлайн\n2) !дедлайны `дата` - дедлайны на этот день\n" \
               "3) !load - загрузить состояние предыдущее бота\n4) !save - сохранить текущее состояние бота"

    def _set_deadline(self, message) -> str:
        if self._phase == 0:
            self._phase = 1
            return "1) Выберите дату (Формат: 01.01.01)"
        if self._phase == 1:
            if not self.date_format(message):
                return "Введен неверный формат даты.\nВведите еще раз (Формат: 01.01.01)"
            self._phase = 2
            self._temp_deadline_date = message
            return "2) Выберите время (Формат: 00:00)"
        if self._phase == 2:
            if not self.time_format(message):
                return "Введен неверный формат времени.\nВведите еще раз (Формат: 00:00)"
            self._phase = 3
            self._temp_deadline += message + " "
            return "3) Напишите описание"
        if self._phase == 3:
            self._phase = 0
            self._temp_deadline += message
            if self._deadlines.get(self._temp_deadline_date) is None:
                self._deadlines[self._temp_deadline_date] = DeadlineContainer()
            self._deadlines[self._temp_deadline_date].set_deadline(self._temp_deadline)
            self._temp_deadline = ""
            return "Дедлайн сохранен"
        return "Error"

    def _get_deadline(self, date) -> str:
        if self._deadlines.get(date) is None:
            return "На " + date + " дедлайнов нет"
        return self._deadlines[date].get_deadlines()

    def _save_state(self) -> str:
        file = open('deadlines.txt', 'w')
        for key, value in self._deadlines.items():
            file.write('index: ' + str(key) + '\n')
            file.write(self._deadlines[key].get_deadlines())
        file.close()
        return "State saved"

    def _load_state(self) -> str:
        file = open('deadlines.txt', 'r')
        temp_date = ''
        for line in file:
            if line == '':
                continue
            if line.split()[0] == 'index:':
                temp_date = line.split()[1]
                self._deadlines[temp_date] = DeadlineContainer()
                continue
            temp_deadline = line[:-1]
            self._deadlines[temp_date].set_deadline(temp_deadline)
        file.close()
        return "Previous state loaded"

    def new_message(self, message) -> str:
        if message.lower() == self._commands[0] or self._phase != 0:
            return self._set_deadline(message)
        if message.lower().split()[0] == self._commands[1]:
            if len(message.split()) < 2:
                return "Введите команду в формате: `!дедлайны дата`"
            return self._get_deadline(message.split()[1])
        if message.lower() == self._commands[2]:
            return self._load_state()
        if message.lower() == self._commands[3]:
            return self._save_state()
        return "no"
