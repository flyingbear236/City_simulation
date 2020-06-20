#!/usr/bin/env python
# coding: utf-8

# In[20]:


import random as rnd


# In[9]:


def get_list(var):
    """По условному названию списка
    возвращает список либо словарь, из
    которого выбирается имя, фамилия, улицы, прочее"""
    path = choose_path(var)
    file = open(path, 'r').readlines()
    if len(file) == 1:
        file = open(path, 'r').read()
        return [i for i in file.split(',')]
    else:
        return get_dict(path)


def get_dict(path):
    """Вызывается внутри get_list()
    если структура документа предполагает
    создание словаря, а не списка
    возвращает словарь"""
    file = open(path, 'r')
    elem_mixed = file.read().split('\n')
    elem_types = elem_mixed[::2]
    del elem_mixed[::2]
    elem_pure = [i.split(',') for i in elem_mixed]
    elem_dict = {elem_types[n]: elem_pure[n] for n in range(len(elem_pure))}
    return (elem_dict)


def choose_path(var):
    """Выбирает путь к файлу
    по кодовому слову"""
    if Loc.locs.get(var):
        return Loc.locs[var]


# In[85]:


def get(ID):
    """Возвращает объект City, Street или House по ID
    если нашлось несколько подходящих, возвращает список ID
    и печатает сообщение"""
    if get_city(ID):
        if type(get_city(ID)) == list:
            print('{} cities found. Search full ID:'.format(len(get_city(ID))))
        return get_city(ID)
    elif get_street(ID):
        if type(get_street(ID)) == list:
            print('{} streets found. Search full ID:'.format(len(get_street(ID))))
        return get_street(ID)
    elif get_house(ID):
        if type(get_house(ID)) == list:
            print('{} houses found. Search full ID:'.format(len(get_house(ID))))
        return get_house(ID)
    else:
        print("Error! Nothing found")


# In[74]:


def get_city(ID):
    """Возвращает объект City по ID или его части
    если нашел несколько, возвращает
    список возможных ID. Не нашел ничего — None"""
    out = []
    for key in City.full_list.keys():
        if key.find(ID) != -1:
            out.append(City.full_list.get(key))
    if len(out) == 1:
        return out[0]
    elif out == []:  # как это сделать умнее? хотел через for ... else, не вышло
        return None
    else:
        ID_list = list()
        for elem in out:
            ID_list.append(elem.ID)
        return ID_list


# In[73]:


def get_street(ID):
    """Возвращает объект Street по ID или его части
    если нашел несколько, возвращает
    список возможных ID. Не нашел ничего — None"""
    out = []
    for key in Street.full_list.keys():
        if key.find(ID) != -1:
            out.append(Street.full_list.get(key))
    if len(out) == 1:
        return out[0]
    elif out == []:  # как это сделать умнее? хотел через for ... else, не вышло
        return None
    else:
        ID_list = list()
        for elem in out:
            ID_list.append(elem.ID)
        return ID_list


# In[76]:


def get_house(ID):
    """Возвращает объект House по ID или его части
    если нашел несколько, возвращает
    список возможных ID. Не нашел ничего — None"""
    out = []
    for key in House.full_list.keys():
        if key.find(ID) != -1:
            out.append(House.full_list.get(key))
    if len(out) == 1:
        return out[0]
    elif out == []:  # как это сделать умнее? хотел через for ... else, не вышло
        return None
    else:
        ID_list = list()
        for elem in out:
            ID_list.append(elem.ID)
        return ID_list


# In[14]:


class Loc:
    """Класс, сотоящий из словаря, где хранятся пути к csv-спискам имён"""
    locs = {'streets': 'csv/streets.csv',
            'jobs': 'csv/jobs.csv',
            'male': 'csv/boys.csv',
            'female': 'csv/girls.csv',
            'surnames': 'csv/surnames.csv',
            'cities': 'csv/cities.csv'}


# In[136]:


class City:
    """Город. Класс хранит словарь городов, список возможных названий улиц, работ,
    названий городов"""
    full_list = {}
    all_streets = get_list('streets')
    all_jobs = get_list('jobs')
    all_city_names = get_list('cities')

    def __init__(self):
        """Атрибуты объекта город: имя, ID, число улиц, список названий улиц,
        вспомогательный список названий улиц, словарь объектов-улиц
        :rtype: City"""
        self.name = rnd.choice(City.all_city_names)
        City.all_city_names.remove(self.name)
        self.ID = self.name
        self.population = []
        self.streets_number = rnd.randint(5, 10)
        self.streets_names = self.choose_names()
        self.streets_names_copy = self.streets_names[:]
        self.streets_list = {}
        for i in range(self.streets_number):
            new = Street(self)

        City.full_list.update({self.ID: self})

    def __str__(self):
        return ((self.name) + ': ' + str(self.streets_number) + ' streets')

    def choose_names(self):
        """Выбирает из списка всех возможных названий улиц
        N названий, где N= число улиц в городе"""
        i = 1
        availible_street = set()
        while i <= self.streets_number:
            x = rnd.choice(City.all_streets)
            if not (x in availible_street):
                availible_street.add(x)
                i += 1
        return list(availible_street)

    def print_map(self):
        """Возвращает строку:
        название города, к-во улиц
        список улиц с адресами и типами домов"""
        out = ''
        out += str(self) + '\n\n==========+==========\n\n'
        for key in self.streets_list.keys():
            street = self.streets_list.get(key)
            out += street.print_map() + '\n'
        return out

    def detailed_map(self):
        """Возвращает строку:
        название города, к-во улиц
        список улиц с адресами и типами домов, их помещениями"""
        out = ''
        out += str(self) + '\n\n==========+==========\n\n'
        for key in self.streets_list.keys():
            street = self.streets_list.get(key)
            out += street.detailed_map() + '\n'
        return out


# In[17]:


class Street:
    """Улица. Класс хранит словарь всех улиц"""
    count = 0
    full_list = {}

    def __init__(self, city):
        """Атрибуты объекта улица: объект-город, название улицы
        словарь объектов-домов, ID"""
        self.city = city
        self.name = rnd.choice(self.city.streets_names_copy)
        self.city.streets_names_copy.remove(self.name)
        self.houses_number = rnd.randint(1, 5)
        self.houses_list = {}
        self.make_houses()

        self.ID = self.city.name + ', ' + self.name
        Street.full_list.update({self.ID: self})
        self.city.streets_list.update({self.ID: self})
        Street.count += 1

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        self.max = len(self.houses_list) - 1
        if self.i <= self.max:
            result = str(self.houses_list[self.i])
            self.i += 1
            return result
        else:
            raise StopIteration

    def print_map(self):
        """Возвращает строку:
        название улицы, к-во домов
        адрес каждого дома, его тип """
        out = ''
        out += str(self) + '\n===============\n'
        for key in self.houses_list.keys():
            house = self.houses_list.get(key)
            out += (str(house)) + '\n'
        return out

    def detailed_map(self):
        """Возвращает строку:
        название улицы, к-во домов
        адрес каждого дома, его тип и помещения """
        out = ''
        out += str(self) + '\n===============\n'
        for key in self.houses_list.keys():
            house = self.houses_list.get(key)
            out += (house.detailed()) + '\n'
        return out

    def __str__(self):
        return (self.name + ', ' + str(self.houses_number) + ' buildings:')

    def make_houses(self):
        """Добавить в словарь домов объекты-дома"""
        for number in range(1, self.houses_number + 1):
            new = House(self, number)


# In[18]:


class House:
    """Класс Дом. Хранит счетчик домов, словарь всех домов"""
    count = 0
    full_list = {}

    def __init__(self, street, number):
        """Атрибуты объекта Дом: объект-улица
        тип, номер, адрес (строка-название улицы и номер), к-во жилых и рабочих помещений, ID"""
        self.street = street
        self.type = rnd.choice(('office', 'house'))
        self.number = number
        self.address = self.street.name + ', ' + str(self.number)
        if self.type == 'house':
            self.living_space = rnd.randint(5, 20)
            self.working_space = None
        else:
            self.living_space = None
            self.working_space = rnd.randint(5, 20)
        self.ID = self.street.city.name + ', ' + self.address
        House.full_list.update({self.ID: self})
        self.street.houses_list.update({self.ID: self})
        House.count += 1

    def __str__(self):
        out = ''
        out += (self.street.city.name + ', ' + self.address + ' — ' + self.type)
        return out

    def detailed(self):
        out = ''
        if self.living_space is None:
            out += (self.street.city.name + ', ' + self.address + ' — ' + self.type + '\nI hold ' +
                    str(self.working_space) + ' offices')
        else:
            out += (self.street.city.name + ', ' + self.address + ' — ' + self.type + '\nI hold ' +
                    str(self.living_space) + ' apartments')
        return out


# In[148]:


class Human:
    surnames = get_list('surnames')

    def __init__(self, city):
        self.city = city
        self.age = rnd.randint(18, 20)
        self.gender = rnd.choice(('male', 'female'))
        self.name = rnd.choice(get_list(self.gender))  # неправильно, список имен сохранить в атрибуты класса
        self.surname = rnd.choice(Human.surnames)
        self.home_street = get(self.make_street_ID())
        self.work_street = get(self.make_street_ID())
        self.job_domain = rnd.choice(list(City.all_jobs.keys()))
        self.job = rnd.choice(City.all_jobs[self.job_domain])
        self.money = None
        self.wants_marriage = bool(rnd.randint(0, 1))
        self.is_married = False

        # length between home address and work address becomes time to commute

    def __str__(self):
        return ('Hi! My name is ' + self.name + ' ' + self.surname +
                '\nmy age is ' + str(self.age) + ' my gender is ' + self.gender +
                '\nI live in ' + self.home_street.name + ' in ' + self.city.name +
                '\nI work in ' + self.job_domain + ' as a ' + self.job +
                '\nat ' + self.work_street.name +
                '\nDo I want to marry? — ' + str(self.wants_marriage))

    # пока не сделал, чтобы человек заселялся в дом и устривался на работу.
    # думаю сделать классы Apartment, Office, внутри - рабочие и жилые места. Или не надо

    def make_street_ID(self):
        return self.city.name + ', ' + rnd.choice(self.city.streets_names)

    def act(self):
        pass

    def work(self):
        pass

    def commute(self):
        pass

    def sleep(self):
        pass

    def eat(self):
        pass

    def relax(self):
        pass

    def fall_ill(self):
        pass

    def die(self):
        pass

    def cure(self):
        pass


city1 = City()
print(city1)
# In[ ]:


# примеры вызовов


# In[137]:


# максимально можно создать до 50 городов, пока не кончатся имена
# здесь - 10 напихивается в список k

# k = []
# i = 0
# while i <= 9:
#     k.append(City())
#     i += 1


# In[138]:


# словарь городов вида {имя_города:объект}

# (City.full_list)


# In[143]:


# примеры вызовов

# for i in City.full_list.values():
#     print (i)

# попробуй также (получится большой вывод на консоль)

# .print_map()
# метод City

# for i in City.full_list.values():
#     print(i.print_map())


# In[147]:


# названия улиц

# for city in k:
#     print (city.streets_names)

# названия городов

# for city in k:
#     print (city.name)


# попробуй функцию get('Любое из названий')
# попробуй также print(get('Любое из названий'))

# в get можно вводить имя города, улицы или адрес дома по типу Golden Lane, 1

# когда ты get-вызвал объект Улица, попробуй .detailed_map()
# когда ты get-вызвал объект Дом, попробуй .detailed()


# In[93]:


# счетчик домов
# print(House.count)


# In[149]:


# city1 = City()
# print(city1.detailed_map())


# In[150]:


# print(city1.print_map())


# In[154]:


# man1 = Human(city1)
# print (man1)


# имплементировать заселение. метод populate() класса City. Смотрим, сколько есть рабочих и жилых мест в городе и
# заселяем народ. При инициализации объекта Человек — человек заселяется в дом, занимает там одну ячейку,
# на работе тоже. Как-то надо это тоже сделать.
