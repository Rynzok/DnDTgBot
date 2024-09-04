from domain.casts import Cast
from infrastructure.work_with_db import write_to_db, casts_read_from_db, alias_all_read_db


class Alias:

    def __init__(self):
        self.id = None
        self.name = None
        self.string = None
        self.list_cast = []

    def create_from_string(self, list_string):
        self.string = " ".join(list_string)
        for string in list_string:
            command = Cast(string)
            command.create_from_string()
            self.list_cast.append(command)

    def create_from_db(self, name):
        list_string, string = casts_read_from_db(name)
        self.string = string
        for string in list_string:
            command = Cast(string[1])
            command.create_from_db(string)
            self.list_cast.append(command)

    def create_name(self, name):
        self.name = name

    def sum(self):
        result = 0
        some_text = ""
        for cast in self.list_cast:
            res, text_box = cast.calculation()
            result += res
            some_text += text_box + f"\n"

        text = f"Суммарный результат: {result} \n" + some_text

        return text, result

    def write_to_db(self, group_url):
        write_to_db(self.name, self.string, self.list_cast, group_url)


def calculation_dice(string):
    command = Alias()
    command.create_from_string(string.split())
    text_box, res = command.sum()
    return text_box, res


def alias_release(string):
    list_string = string.split()
    command = Alias()
    command.create_from_db(list_string[1])
    text, res = command.sum()
    text_box = f"Алиас: {list_string[1]} ({command.string}) \n" + text
    return text_box, res

def create_alias(string, group_url):
    # Разделяем строку
    list_string = string.split()
    # Убираем ключевое слово al
    list_string.pop(0)
    # Получаем название алиаса
    title = list_string[0]
    # Удаляемназвание алиаса из списка casts
    list_string.pop(0)
    command = Alias()
    command.create_name(title)
    command.create_from_string(list_string)
    command.write_to_db(group_url)
    text_box, res = command.sum()
    return text_box, res

def alias_read_db():
    list_alias = alias_all_read_db()
    text_box = []
    for i in list_alias:
        text_box.append(f"{i[0]}: {i[1]}")
    some_text = " Список Алиасов: \n"
    for i in text_box:
        some_text += str(i) + "\n"
    return some_text
