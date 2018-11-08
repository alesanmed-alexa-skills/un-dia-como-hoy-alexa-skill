# encoding: utf-8
from sys import path
import os
from os.path import dirname as dir

path.append(dir(path[0]))

from pymongo import MongoClient
from configurations import skill_config
import urllib

def connect():
    username = urllib.parse.quote_plus(skill_config.DB_USER)
    password = urllib.parse.quote_plus(skill_config.DB_PASS)
    db_ip = urllib.parse.quote_plus(skill_config.DB_IP)
    db_port = urllib.parse.quote_plus(skill_config.DB_PORT)
    db_name = urllib.parse.quote_plus(skill_config.DB_NAME)

    client = MongoClient('mongodb://%s:%s@%s:%s/%s' % 
                        (username, password, db_ip, db_port, db_name))

    return client

def close(client):
    client.close()