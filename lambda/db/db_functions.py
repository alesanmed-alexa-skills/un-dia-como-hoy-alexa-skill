# encoding: utf-8
from sys import path
import os
from os.path import dirname as dir

path.append(dir(path[0]))

from pymongo import MongoClient
import db_utils
from configurations import skill_config

import datetime

def retrieve_random_event(handler_input):
    req_envelope = handler_input.request_envelope

    user_id = req_envelope.context.System.user.userId

    date = datetime.datetime.now()

    date = '{}/{}'.format(str(date.day), str(date.month))

    random_event = __get_event_for_user(user_id, date)['event']

    return random_event

def __get_event_for_user(user_id, date):
    event = None

    if not __user_exists(user_id, date):
        __insert_new_user(user_id, date)
    
    if __get_number_date_events(date) == __get_number_already_fetched_events(user_id, date):
        __reset_user_fetched_events(user_id, date)
        
    fetched_events = __get_already_fetched_events(user_id, date)

    event = __get_random_event_not_fetched(date, fetched_events)
    
    __add_user_fetched_event(user_id, date, event['_id'])

    return event

def __add_user_fetched_event(user_id, date, event_id):
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


def __get_random_event_not_fetched(date, already_fetched):
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

def __reset_user_fetched_events(user_id, date):
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

def __get_number_date_events(event_date):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    res = db.ephemeris.count_documents({
        'date': event_date
    })

    db_utils.close(client)

    return res

def __get_number_already_fetched_events(user_id, date):
    return len(__get_already_fetched_events(user_id, date))

def __get_already_fetched_events(user_id, date):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    res = db.users.find_one({
        'user_id': user_id,
        'date': date
    })

    db_utils.close(client)

    return res['fetched_events']

def __user_exists(user_id, date):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    res = db.users.count_documents({
        'user_id': user_id,
        'date': date
    })

    db_utils.close(client)

    return res == 1

def __insert_new_user(user_id, date):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    db.users.insert_one({
        'user_id': user_id,
        'date': date,
        'fetched_events': []
    })