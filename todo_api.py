#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
import json
import socket

class TodoServer:
    """создает сервер, который слушает по протоколу 
    подобному телнету пор и предоставляет информацию
    по спискам заданий для того или иного пользователя
    """
    
    def __init__(self, adress='192.168.0.2', port=12235):
        """ конструктор
        """
        self.ADRESS = adress
        self.PORT = port
        self.DATADIR = os.path.abspath(os.curdir) + '/user_data/'
        self.MAINPAGE = """Выберите действие:
[1] Просмотреть записи
[2] Добваить запись
[3] Удалить запись
[4] Изменить запись
[5] Очистить поврежденный файл
[6] Создать нового пользователя
[7] Выход
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
            if dict_users == {}:
                tempf = open(self.DATADIR + 'temp_user', 'w')
                tempf.write('{}')
                tempf.close()
                string_list, dict_users = self.get_list_user()
            conn.send(string_list)
            user = dict_users[conn.recv(1024)[:1]]
            conn.send('Вы выбрали пользователя: ' + user + '\n')
            conn.send('=============================\n')
            conn.send(self.MAINPAGE)
            p = True
            while p:
                p = self.commander(conn.recv(1024)[:1], conn, user)
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
        conn.send('=============================\n')
        dict_print = {}
        string = u''
        iteration = 1
        for i, p in dict_todo.items():
            dict_print[iteration]=(i, p)
            string += u'[' + str(iteration).decode('utf-8') + u'] ' + p + u'\n'
            iteration += 1
        # [1] Просмотреть записи
        if command == '1':
            conn.send(string.encode("utf-8"))
            conn.send(self.MAINPAGE)
            return True
        # [2] Добваить запись
        elif command == '2':
            conn.send('Введите новую запись: ')
            note = conn.recv(1000000)
            dict_todo[str(uuid.uuid1()).encode("utf-8")] = note[:-2]
            json.dump(dict_todo, open(self.DATADIR + user, 'w')) 
            conn.send(self.MAINPAGE)
            return True
        # [3] Удалить запись
        elif command == '3':
            conn.send('Введите номер записи, которую нужно удалить: ')
            note = int(conn.recv(1024)[:1])
            del dict_todo[dict_print[note][0]]
            json.dump(dict_todo, open(self.DATADIR + user, 'w')) 
            conn.send(self.MAINPAGE)
            return True
        # [4] Изменить запись
        elif command == '4':
            conn.send('Введите номер записи, которую нужно изменить: ')
            note = int(conn.recv(1024)[:1])
            conn.send('Введите новое значение записи: ')
            dict_todo[dict_print[note][0]] = conn.recv(1024)[:-2]
            json.dump(dict_todo, open(self.DATADIR + user, 'w')) 
            conn.send(self.MAINPAGE)
            return True
        # [5] Очистить поврежденный файл
        elif command == '5':
            json.dump({}, open(self.DATADIR + user, 'w')) 
            conn.send(self.MAINPAGE)
            return True
        # [6] Создать нового пользователя
        elif command == '6':
            conn.send('Введите имя нового пользователя: ')
            new_user = conn.recv(1000000).decode('utf-8')
            tempf = open(self.DATADIR + new_user[:-2], 'w')
            tempf.write('{}')
            tempf.close()
            conn.send(self.MAINPAGE)
            return True
        # [7] Выход
        elif command == '7':
            conn.send(self.MAINPAGE)
            return False
        else:
            conn.send(self.MAINPAGE)
            return True

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
            
app = TodoServer()

if __name__ == '__main__':
    app.run()
