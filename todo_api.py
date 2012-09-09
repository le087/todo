#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
import json
import socket

class todoserver:
    """создает сервер, который слушает по протоколу 
    подобному телнету пор и предоставляет информацию
    по спискам заданий для того или иного пользователя
    """
    
    def __init__(self, adress='192.168.0.2', port=12235):
        """ конструктор
        """
        self.ADRESS = adress
        self.PORT = port
        self.DATADIR = os.path.abspath(os.curdir) + '/user_data'
        self.MAINPAGE = """Выберите действие:
[1] Просмотреть записи
[2] Добваить запись
[3] Удалить запись
[4] Выход
==========================
"""

    def run(self):
        """ Метод открывает сокет и слушает его на
        указанном порту
        Arguments:
        - `self`:
        """
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind((self.ADRESS, self.PORT))
        server_sock.listen(5)
        
        while 1:
            conn, adr_user = server_sock.accept()
            conn.send('Добро пожаловать в Тудушечку!\n')
            conn.send('=============================\n')
            conn.send('Выберите пользователя:\n')
            string_list, dict_users = self.get_list_user()
            conn.send(string_list)
            user = dict_users[conn.recv(1024)[:1]]
            conn.send('Вы выбрали пользователя: ' + user + '\n')
            conn.send(self.MAINPAGE)
            while 1:
                self.commander(conn.recv(1024)[:1], conn, "/" + user)
            conn.close()

    def commander(self, command, conn, user):
        """ обрабатывает запросы пользователя
        
        Arguments:
        - `self`:
        - `command`: команда пользователя
        - `conn`: объект соединение
        - `user`: пользователь, для которого надо редактировать записи
        """
        try:
            dict_todo = json.load(open(self.DATADIR + user, 'r'))
        except:
            dict_todo = {}
            print "Ошибка при импорте данных пользователя"
        conn.send('=============================\n')
        dict_print = {}
        string = u''
        iteration = 1
        for i, p in dict_todo.items():
            dict_print[iteration]=(i, p)
            string += u'[' + str(iteration).decode('utf-8') + u'] ' + p + u'\n'
            iteration += 1
        if command == '1':
            conn.send(string.encode("utf-8"))
        elif command == '2':
            conn.send('Введите новую запись: ')
            dict_todo[str(uuid.uuid1()).encode("utf-8")] = conn.recv(1024)[:-2]
            json.dump(dict_todo, open(self.DATADIR + user, 'w')) 
        elif command == '3':
            conn.send('Введите номер записи, которую нужно удалить: ')
            test = int(conn.recv(1024)[:1])
            print dict_todo[dict_print[test][0]]
        conn.send(self.MAINPAGE)

    def get_list_user(self):
        """ возвращает список пользователей
        
        Arguments:
        - `self`:
        """
        dict_users = {}
        stroka = ""
        n = 1
        for i in os.listdir(self.DATADIR):
            dict_users[str(n)] = i
            stroka += "[" + str(n) + "]" + i + "\n"
            n += 1
        return stroka, dict_users
            
    def get_todo(self, user):
        """возвращает список todo из словаря
        который сохранен в базе для конкретного пользователя
        
        Arguments:
        - `self`:
        - `user`: пользователь, для которого необходим вывести инфу
        """
        list_user = os.listdir(self.DATADIR)
        if user in list_user:
            return 
        else:
            return False

    def write_todo(self, user, todo):
        """записывает новую запись в базу данных
        пользователя
        
        Arguments:
        - `self`:
        - `user`: пользоветель
        - `todo`: новая запись
        """
        data = json.load(open(self.DATADIR + user, 'r'))
        data[str(uuid.uuid1())] = todo
        list_user = os.listdir(self.DATADIR)
        if user in list_user:
            json.dump(data, open(self.DATADIR + user, 'wb'))
            return True
        else:
            return False
            
app = todoserver()

if __name__ == '__main__':
    app.run()
