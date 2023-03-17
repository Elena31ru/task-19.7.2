from api import PetFriends
from pytest import mark
from settings import valid_email, valid_password, invalid_password, invalid_email
import os


class TestApi:
    def setup(self):
        self.pf = PetFriends()

    def test_get_api_key_for_invalid_email(self):
        """Проверяем, что запрос api ключа с неверным email возвращает код 403"""
        status, result = self.pf.get_api_key(invalid_email, invalid_password)
        assert status == 403
        assert 'This user wasn&#x27;t found in database' in result

    def test_get_api_key_for_valid_email_and_invalid_password(self):
        """Проверяем, что запрос api ключа с верным email и неверным password возвращает код 403"""
        status, result = self.pf.get_api_key(valid_email, invalid_password)
        assert status == 403
        assert 'This user wasn&#x27;t found in database' in result
    
    def test_get_all_pets_with_invalid_key(self):
        """Проверяем, что запрос всех питомцев с неверным api ключом возвращает код 403"""
        # Задаем неверный ключ api и сохраняем в переменную auth_key
        auth_key = {'key': '123'}
        status, result = self.pf.get_list_of_pets(auth_key, '')
        assert status == 403
    
    @mark.parametrize('name', ('Вася', 'Петя'))
    @mark.parametrize('animal_type', ('кот', 'пёс'))
    @mark.parametrize('age', ('1', '15'))
    def test_create_pet_simple_with_valid_data(self, name, animal_type, age):
        """Проверяем, что можно упрощенно добавить питомца с корректными данными"""
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.create_pet_simple(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name

    @mark.parametrize('name', ('Вася', 'Петя'))
    @mark.parametrize('animal_type', ('кот', 'пёс'))
    @mark.parametrize('age', ('1', '15'))
    def test_create_pet_simple_with_invalid_key(self, name, animal_type, age):
        """Проверяем, что запрос на упрощенное добавление питомца с неверным api ключом возвращает код 403"""
        # Задаем неверный ключ api и сохраняем в переменную auth_key
        auth_key = {'key': '123'}
        status, result = self.pf.create_pet_simple(auth_key, name, animal_type, age)
        assert status == 403

    @mark.parametrize('name', ('Вася', 'Петя'))
    @mark.parametrize('animal_type', ('кот', 'пёс'))
    @mark.parametrize('age', ('1', '15'))
    def test_add_new_pet_with_invalid_data(self, name, animal_type, age):
        """Проверяем что можно добавить питомца с некорректными данными"""
        pet_photo = 'images/lol.txt'
    
        # Получаем путь изображения питомца и сохраняем в pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    
        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
    
        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)  # Добавляем питомца
        assert status == 400
    
    def test_successful_set_photo(self):
        """Проверяем возможность установки фото питомца"""
    
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)  # Получаем ключ auth_key
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")  # Запрашиваем список своих питомцев
    
        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), 'images/dog.jpg')
        if len(my_pets['pets']) > 0:
            status, result = self.pf.set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
            assert status == 200
        else:
            raise Exception("There is no my pets")

    @mark.parametrize('name', ('Вася', 'Петя'))
    @mark.parametrize('animal_type', (2, 10))
    @mark.parametrize('age', ('1', '15'))
    def test_create_pet_simple_with_invalid_animal_type(self, name, animal_type, age):
        """Проверяем, что запрос на упрощенное добавление питомца с неверным api ключом возвращает код 403"""
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.create_pet_simple(auth_key, name, animal_type, age)  # Создаем питомца
        assert status == 400  # Сверяем полученный ответ с ожидаемым результатом

    @mark.parametrize('name', (2, 10))
    @mark.parametrize('animal_type', ('кот', 'пёс'))
    @mark.parametrize('age', ('1', '15'))
    def test_create_pet_simple_with_invalid_name(self, name, animal_type, age):
        """Проверяем, что запрос на упрощенное добавление питомца с неверным api ключом возвращает код 403"""
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.create_pet_simple(auth_key, name, animal_type, age)
        assert status == 400

    def test_unsuccessful_update_self_pet_info(self, name='Мурзик', animal_type='Котэ', age=5):
        """Проверяем возможность обновления информации о питомце с неверным api ключом"""
        # Задаем неверный ключ api и сохраняем в переменную auth_key
        auth_key = {'key': '123'}
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")
    
        # Если список не пустой, то пробуем обновить его имя, тип и возраст
        if len(my_pets['pets']) > 0:
            status, result = self.pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert status == 403
        else:
            # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")
        # Тут баг, так как при неверном api ключе не выдает код 403
