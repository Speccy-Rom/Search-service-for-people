#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import vk_api
import getpass


# APP_ID = 7136810
APP_ID = 6222115
SCOPE = 394462


def two_factor_auth():
    key = getpass.getpass('Введите код двухфакторной авторизации: ')
    remember_device = True
    return key, remember_device


def captcha_handler(captcha):
    """ https://vk-api.readthedocs.io/en/latest/exceptions.html#vk_api.exceptions.Captcha
    """
    key = input("Введите код капчи {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


def vk_login(login, password, two_factor=False):
    if two_factor:
        vk_session = vk_api.VkApi(login, password, app_id=APP_ID, scope=SCOPE,
                                  auth_handler=two_factor_auth())
    else:
        vk_session = vk_api.VkApi(login, password, app_id=APP_ID, scope=SCOPE)
    try:
        vk_session.auth(token_only=True)
    except vk_api.Captcha as err:
        print('Необходима проверка капчи')
        vk_session = vk_api.VkApi(login, password, app_id=APP_ID, scope=SCOPE,
                                  captcha_handler=captcha_handler)
    except vk_api.AuthError as err:
        print(err)
    else:
        return vk_session
