#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
import json
import socket

#configuration
DATADIR = os.path.abspath('.') + '/user_data'

class todoserver:
    """создает сервер, который слушает по протоколу 
    подобному телнету пор и предоставляет информацию
    по спискам заданий для того или иного пользователя
    """
    
    def __init__(self):
        """ конструктор
        """
        self.adress = '0.0.0.0'
        self.port = 12235
        
    def run(self, adress, port):
        """ Метод открывает сокет и слушает его на
        указанном порту
        Arguments:
        - `self`:
        """
        while 1:
            pass

    def get_list_user(self):
        """ возвращает список пользователей
        
        Arguments:
        - `self`:
        """
        pass
    
    def get_todo(self, user):
        """возвращает список todo из словаря
        который сохранен в базе для конкретного пользователя
        
        Arguments:
        - `self`:
        - `user`: пользователь, для которого необходим вывести инфу
        """
        list_user = os.listdir(DATADIR)
        if user in list_user:
            data = json.load(open(DATADIR + user, 'r'))
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
        list_user = os.listdir(DATADIR)
        if user in list_user:
            data = json.dump(open(DATADIR + user, 'r'))
            return [(k, v) for k, v in data.items()]
        else:
            return False
        

            


if __name__ == '__main__':
    app.run()
