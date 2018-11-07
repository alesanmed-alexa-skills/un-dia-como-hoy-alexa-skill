# encoding: utf-8
from sys import path
import os
from os.path import dirname as dir

path.append(dir(path[0]))

from pymongo import MongoClient
import db_utils
from configurations import skill_config

def get_event_for_user(user_id, date):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    event = None

    if not user_exists(user_id, date):
        insert_new_user(user_id, date)
    
    if get_number_date_events(date) == get_number_already_fetched_events(user_id, date):
        reset_user_fetched_events(user_id, date)
        
    fetched_events = get_already_fetched_events(user_id, date)

    event = get_random_event_not_fetched(date, fetched_events)
    
    add_user_fetched_event(user_id, date, event['_id'])
    
    db_utils.close(client)

    return event

def add_user_fetched_event(user_id, date, event_id):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    db.users.find_one_and_update({
        'user_id': user_id,
        'date': date
    }, {
        '$push': {
            'fetched_events': event_id
        }
    })

    db_utils.close(client)


def get_random_event_not_fetched(date, already_fetched):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    events = db.ephemeris.aggregate([
        {
            '$match': {
                'date': date,
                '_id': {
                    '$nin': already_fetched
                }
            }
        },
        {
            '$sample': { 'size': 1 }
        }
    ])

    db_utils.close(client)

    return list(events)[0]

def reset_user_fetched_events(user_id, date):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    db.users.find_one_and_update({
        'user_id': user_id,
        'date': date
    }, {
        '$set': {
            'fetched_events': []
        }
    })

    db_utils.close(client)

def get_number_date_events(event_date):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    res = db.ephemeris.count_documents({
        'date': event_date
    })

    db_utils.close(client)

    return res

def get_number_already_fetched_events(user_id, date):
    return len(get_already_fetched_events(user_id, date))

def get_already_fetched_events(user_id, date):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    res = db.users.find_one({
        'user_id': user_id,
        'date': date
    })

    db_utils.close(client)

    return res['fetched_events']

def user_exists(user_id, date):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    res = db.users.count_documents({
        'user_id': user_id,
        'date': date
    })

    db_utils.close(client)

    return res == 1

def insert_new_user(user_id, date):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    db.users.insert_one({
        'user_id': user_id,
        'date': date,
        'fetched_events': []
    })

if __name__ == '__main__':
    print(get_event_for_user('1', '8/11'))