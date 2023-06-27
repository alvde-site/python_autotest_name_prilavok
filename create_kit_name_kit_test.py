import data
import sender_stand_request


def get_kit_body(name):
    current_body = data.kit_body.copy()
    current_body["name"] = name
    return current_body


def create_user():
    user_response = sender_stand_request.post_new_user(data.user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""
    user_token = sender_stand_request.get_new_user_token()
    current_token = data.auth_token.copy()
    current_token["Authorization"] = "Bearer " + user_token
    return current_token


def positive_assert(name):
    # получаем токен пользователя для header
    auth_token = create_user()
    kit_body = get_kit_body(name)
    user_kit_response = sender_stand_request.post_new_client_kit(kit_body, auth_token)
    assert user_kit_response.status_code == 201
    assert user_kit_response.json()["name"] == name


def negative_assert_code_400(name):
    # получаем токен пользователя для header
    auth_token = create_user()
    kit_body = get_kit_body(name)
    user_kit_response = sender_stand_request.post_new_client_kit(kit_body, auth_token)
    assert user_kit_response.status_code == 400


# Тест 1. Допустимое количество символов (1):
def test_create_user_kit_1_letter_in_name_get_success_response():
    positive_assert("a")


# Тест 2. Допустимое количество символов (511):
def test_create_user_kit_511_letter_in_name_get_success_response():
    positive_assert(
        "Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabc" \
        + "dabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
        + "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcda" \
        + "bcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdab" \
        + "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabc" \
        + "dabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
        + "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcda" \
        + "bcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")


# Тест 3. Количество символов меньше допустимого (0):
def test_create_user_kit_0_letter_in_name_get_error_response():
    negative_assert_code_400("")


# Тест 4. Количество символов больше допустимого (512):
def test_create_user_kit_512_letter_in_name_get_error_response():
    negative_assert_code_400("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
                             + "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabc" \
                             + "dabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
                             + "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcda" \
                             + "bcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
                             + "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabc" \
                             + "dabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
                             + "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcda" \
                             + "bcdabcD")


# Тест 5. Разрешены английские буквы:
def test_create_user_kit_english_letter_in_name_get_success_response():
    positive_assert("QWErty")


# Тест 6. Разрешены русские буквы:
def test_create_user_kit_russian_letter_in_name_get_success_response():
    positive_assert("Мария")


# Тест 7. Разрешены спецсимволы:
def test_create_user_kit_has_special_symbol_in_name_get_success_response():
    positive_assert("\"№%@\",")


# Тест 8. Разрешены пробелы:
def test_create_user_kit_has_space_in_name_get_success_response():
    positive_assert(" Человек и КО ")


# Тест 9. Разрешены цифры:
def test_create_user_kit_has_number_in_name_get_success_response():
    positive_assert("123")


# Тест 10. Параметр не передан в запросе:
def test_create_user_kit_no_name_get_error_response():
    auth_token = create_user()
    kit_body = data.kit_body.copy()
    kit_body.pop("name")
    user_kit_response = sender_stand_request.post_new_client_kit(kit_body, auth_token)
    assert user_kit_response.status_code == 400


# Тест 11. Передан другой тип параметра (число):
def test_create_user_kit_user_number_type_name_get_error_response():
    negative_assert_code_400(123)
