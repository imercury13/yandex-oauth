"""Модуль функций библиотеки"""

import pickle, datetime
from . import __version__
from jreq.jreq import safe_request

def get_token_by_code(code, client_id, client_secret):
    """Функция получения токена по коду авторизации

    :param code: код подтверждения
    :type code: str
    :param client_id: id приложения
    :type client_id: str
    :param client_secret: пароль приложения
    :type client_secret: str
    :return: Словарь токенов
    :rtype: dict
	"""

    token = dict()
    url = 'https://oauth.yandex.ru/token'
    headers={'Host': 'oauth.yandex.ru', 'Content-type': 'application/x-www-form-urlencoded'}
    body = 'grant_type=authorization_code&code='+str(code)+'&client_id='+str(client_id)+'&client_secret='+str(client_secret)
    token.update({'client_id':client_id, 'client_secret':client_secret})
    token.update(safe_request('post', url, headers, body))
    token.update({'expires_in':datetime.datetime.today()+datetime.delta(seconds=token['expires_in'])})
    
    return token

def refresh_token(token):
    """Функция обновления токена
    
    :param token: Словарь токенов
    :type token: dict
    :return: Обновленный словарь токенов
    :rtype: dict
    """
    url = 'https://oauth.yandex.ru/token'
    headers={'Host': 'oauth.yandex.ru', 'Content-type': 'application/x-www-form-urlencoded'}
    body = 'grant_type=refresh_token&refresh_token='+token['refresh_token']+'&client_id='+token['client_id']+'&client_secret='+token['client_secret']
    token.update(safe_request('post', url, headers, body))
    token.update({'expires_in':datetime.datetime.today()+datetime.delta(seconds=token['expires_in'])})
    
    return token

def check_expire_token(token, delta):
    """Функция проверки на истечение времени жизни токена

    :param token: Словарь токенов
    :type token: dict
    :param delta: Временной интервал, если разница между датой истечения и текущей меньше этого значения, функция вернет True
    :type delta: datetime.delta
    :return: True или False
    :rtype: bool
    """
    if token['expires_in'] - datetime.datetime.today() < delta:
        return True
    else:
        return False 

def save_token(path, token):
    """Функция сохранения токенов в pickle хранилище
    
    :param path: путь для сохранения хранилища
    :type path: str
    :param token: словарь токенов
    :type token: dict
    :return: True или False
    :rtype: bool
    """
    try:
        with open(path+'/token.pickle','wb') as f:
            pickle.dump(token, f)
    except:
        return False
    
    return True

def load_token(path):
    """Функция загрузки токенов из хранилища
    
    :param path: путь к хранилищу
    :type path: str
    :return: Словарь токенов или False, если нет хранилища
    """
    try:
        with open(path+'/token.pickle','rb') as f:
            token = pickle.load(f)
    except:
        return False
    else:
	    return token