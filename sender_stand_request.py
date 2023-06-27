import configuration
import requests
import data


def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)


def get_new_user_token():
    return post_new_user(data.user_body).json()["authToken"]


def post_new_client_kit(body, token):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_KITS,
                         json=body,
                         headers=token)
