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
                pass
            conn.close()

    def commander(self, command, conn):
        """ обрабатывает запросы пользователя
        
        Arguments:
        - `self`:
        - `command`:
        """
        if command == '1':
            pass

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
            data = json.load(open(self.DATADIR + user, 'r'))
            return [(k, v) for k, v in data.items()]
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
