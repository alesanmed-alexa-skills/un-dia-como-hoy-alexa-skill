# encoding: utf-8
from sys import path
import os
from os.path import dirname as dir

path.append(dir(path[0]))

from pymongo import MongoClient
from configurations import skill_config
import urllib
from pathlib import Path

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

def load_data():
    client = connect()

    db = client[skill_config.DB_NAME]
    
    pathlist = Path('files').glob('**/*.txt')

    for path in pathlist:
        path = str(path)
        date = path.replace('files{}'.format(os.sep), '').replace('{}list.txt'.format(os.sep), '').split(os.sep)
        
        day = date[-1]
        month = date[0]

        print(date)
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                db.ephemeris.insert_one({
                    'date': '{}/{}'.format(day, month),
                    'event': line.strip()
                })
    
    close(client)

if __name__ == '__main__':
    load_data()