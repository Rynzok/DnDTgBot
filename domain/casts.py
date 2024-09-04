from random import randint


class Cast:

    def __init__(self, string):
        self.dict_values = {'count': 1, 'facets': 20, 'advantage': False, 'hindrance': False,  'mod': 0}
        self.command = string

    def create_from_string(self):
        # Елси это просто d
        if self.command == 'd':
            return

        list_symbols = ['a', 'h', '+', '-']
        # Список символов, которые мы найдём
        # list_characters = []
        # Список колючей по символам, которые мы наёдём в строке
        # list_key = ['count', 'facets']

        # Находим количество бросаемых кубов
        if self.command.find('d') != 0:
            i = 0
            d = ''
            while i < self.command.find('d'):
                d += ''.join(self.command[i])
                i += 1

            self.dict_values['count'] = int(d)


        # Находим количество граней кубов
        i = self.command.find('d') + 1
        if i < len(self.command):
            f = ''
            while self.command[i] not in list_symbols:
                f += ''.join(self.command[i])
                i += 1
                if i == len(self.command):
                    break

            if f != '':
                self.dict_values['facets'] = int(f)


        # Поиск ключевых сиволов и добавление их значений
        for i in list_symbols:
            if self.command.find(i) != -1:
                # list_characters.append(i)
                if i == 'a':
                    self.dict_values['advantage'] = True
                elif i == 'h':
                    self.dict_values['hindrance'] = True

                elif i == '+':
                    x = self.command.find(i) + 1
                    y = ''
                    for j in range( x ,len(self.command)):
                        y += ''.join(self.command[j])
                    self.dict_values['mod'] = int(y)

                elif i == '-':
                    x = self.command.find(i) + 1
                    y = ''
                    for j in range( x ,len(self.command)):
                        y += ''.join(self.command[j])
                    self.dict_values['mod'] = -int(y)


    def create_from_db(self, list_tuple):
        keys = []
        for key in self.dict_values.keys():
            keys.append(key)

        for i in range(len(keys)):
            self.dict_values[keys[i]] = list_tuple[i + 2]


    def calculation(self):
        cubes = [0 for _ in range(self.dict_values['count'])]

        for i in range(self.dict_values['count']):
            if self.dict_values['advantage']:
                cubes[i] = max(randint(1, self.dict_values['facets']), randint(1, self.dict_values['facets']))
            elif self.dict_values['hindrance']:
                cubes[i] = min(randint(1, self.dict_values['facets']), randint(1, self.dict_values['facets']))
            else:
                cubes[i] = randint(1, self.dict_values['facets'])

        result = (sum(cubes) + self.dict_values['mod'])

        text_box = f"Бросок {self.command}: {result} ("
        for i in cubes:
            text_box += str(i) + " + "
        if self.dict_values['mod'] != 0:
            text_box += str(self.dict_values['mod'])
        else:
            text_box = text_box[:-3]
        text_box += ")"

        return result, text_box
