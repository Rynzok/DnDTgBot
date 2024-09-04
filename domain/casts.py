from random import randint


class Cast:

    def __init__(self, string):
        self.dict_values = {'count': 1, 'facets': 20, 'advantage': False, 'hindrance': False,  'mod': 0}
        self.command = string

    def create_from_string(self):
        # Символы, которые мы ищем в строке
        list_symbols = ['d', 'a', 'h', '+', '-']
        # Список символов, которые мы найдём
        # list_characters = []
        # Список колючей по символам, которые мы наёдём в строке
        list_key = ['count', 'facets']

        # Получаем список ключевых символов котороые есть в строке
        for i in list_symbols:
            if self.command.find(i) != -1:
                # list_characters.append(i)
                if i == 'a':
                    self.dict_values['advantage'] = True
                elif i == 'h':
                    self.dict_values['hindrance'] = True
                elif i == '+' or i == '-':
                    list_key.append('mod')




        # list_characters.append('z')
        string = self.command

        buff = ""
        j = 0
        for i in range(len(string)):
            buff += string[i]
            if buff[-1] == list_characters[j]:
                self.set_values(list_key[j], buff[:-1])
                j += 1
                buff = ""

    def create_from_db(self, list_tuple):
        keys = []
        for key in self.dict_values.keys():
            keys.append(key)

        for i in range(len(keys)):
            self.dict_values[keys[i]] = list_tuple[i + 2]

    # def set_values(self, key, value):
    #     if value != '':
    #         self.dict_values[key] = int(value)
    #     else:
    #         if key == 'count':
    #             self.dict_values[key] = 1
    #         elif key == 'facets':
    #             self.dict_values[key] = 20
    #         elif key == 'bomb':
    #             self.dict_values[key] = 1
    #         elif key == 'resist':
    #             self.dict_values[key] = 1
    #         elif key == 'multi':
    #             self.dict_values[key] = 1
    #         elif key == 'percent':
    #             self.dict_values[key] = 1
    #         else:
    #             self.dict_values[key] = 0

    def calculation(self):
        cubes = [0 for _ in range(self.dict_values['count'])]

        # if self.dict_values['percent'] == 1:
        #     self.set_values('facets', 100)

        for i in range(self.dict_values['count']):
            cubes[i] = randint(0, self.dict_values['facets'])
            if i < self.dict_values['bomb'] and cubes[i] == self.dict_values['facets']:
                cubes.append(randint(0, self.dict_values['facets']))

        result = (sum(cubes) + self.dict_values['mod']) * self.dict_values['multi']
        if self.dict_values['resist'] == 1:
            result = result / 2

        text_box = f"Бросок {self.command}: {result} ("
        if self.dict_values['resist'] == 1:
            text_box += "половина от "
        for i in cubes:
            text_box += str(i) + " + "
        if self.dict_values['mod'] != 0:
            text_box += str(self.dict_values['mod'])
        else:
            text_box = text_box[:-2]
        if self.dict_values['multi'] != 1:
            text_box += f" помноженное на {self.dict_values['multi']})"
        else:
            text_box += ")"

        return result, text_box
