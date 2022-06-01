import sys
sys.path.append("")

from SF_mod_19.Test_PetFriends.api_pf import PetFriends
from SF_mod_19.Test_PetFriends.pf_settings import valid_email, valid_password, invalid_email, invalid_password, invalid_email_2, invalid_password_2

import os

pf = PetFriends()


def test_1_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    print()
    print ('status= ', status)
    assert 'key' in result


def test_2_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    # неверный email
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

def test_3_get_api_key_for_invalid_user(email=valid_email, password=invalid_password_2):
    # неверный email
    status, result = pf.get_api_key(email, password)
    print()
    print ('status 403, key not in result')
    assert status == 403
    assert 'key' not in result

def test_4_get_api_key_for_invalid_user(email=invalid_email_2, password=valid_password):
    # пустой  email
    status, result = pf.get_api_key(email, password)
    assert status == 403
    print()
    print('status 403, key not in result')
    assert 'key' not in result

def test_5_get_api_key_for_valid_user(email=valid_email, password=invalid_password):
    # пустой  password
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in  result

def test_6_get_all_pets_with_valid_key(filter='my_pets'):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    print()
    print('auth_key=',auth_key, 'status =',status, )
    print (result['pets'])
    assert status == 200
    assert len(result['pets']) > 0

def test_7_add_new_pet_with_valid_data(name='Stuart', animal_type='терьер',
                                     age='22', pet_photo='images/animal_jp.jpg'):
    """Проверяем что можно добавить питомца с корректными данными.   """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    print()
    print('result=',result)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200



def test_8_add_new_pet_with_wrong_data(name='Stuart'*100, animal_type='терьер'*100,
                                     age='-444444', pet_photo='images/sf_metro.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    print()
    print('result [name]=', result['name'])

def test_9_add_new_pet_with_valid_data(name='Stuart', animal_type='терьер',
                                     age='44', pet_photo='images/P1040103.jpg'):
    """Проверяем что можно добавить питомца с большим фото.
     но у меня плохой интернет"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    print()
    print('result [name]=',result['name'])

def test_10_add_new_pet_with_wrong_data(name='Stuart', animal_type='терьер',
                                     age='14', pet_photo='images/animal.bmp'):
    """Проверяем что можно добавить питомца с некорректными расширением фото.
     В ответе, что фото с таким расширением не принимается сервером"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 500
    assert result['name'] == name
    print()
    print('result [name]=', result['name'])

def test_11_add_new_pet_with_None(name=None, animal_type='терьер',
                                     age=None, pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с None .
     Ответ не понял. Прошёл тест или нет. на странице ошибки нет"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    print()
    print('result [name]=', result['name'])

def test_12_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key,  "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    print()
    print ('pet_id=', pet_id)
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_13_successful_update_self_pet_info(name='Мрзк', animal_type='Cat', age= 5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
        print()
        print('result [name]=', result['name'])
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# мои записи
def test_14_add_new_pet_simple_with_valid_data(name='Тигрик', animal_type='КОТОтище',
                                                age='19'):
        """Проверяем что можно добавить питомца с корректными данными без фото"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        print()
        assert status == 200
        print ('status simple ADD name =', status)
        assert result['name'] == name
        print ('result [name]=', result['name'])
        assert result['age'] == age
        print ('result [age]=', result['age'])
        assert result['animal_type'] == animal_type
        print ('result [animal_type]=', result['animal_type'])
        print()





def test_15_add_photo_pet(pet_photo='images/animal_jp.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    print()
    print('Обновление фото для pet_id=', pet_id)

    status, result = pf.add_photo_pet(auth_key, pet_id,  pet_photo)

    assert status == 200
    print ('status=',status)
