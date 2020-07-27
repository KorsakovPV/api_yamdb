import pytest
from django.contrib.auth import get_user_model

from .common import create_users_api, auth_client


class Test01UserAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_users_not_auth(self, client):
        response = client.get('/api/v1/users/')

        assert response.status_code != 404, \
            'Страница `/api/v1/users/` не найдена, проверьте этот адрес в *urls.py*'

        assert response.status_code == 401, \
            'Проверьте, что при GET запросе `/api/v1/users/` без токена авторизации возвращается статус 401'

    @pytest.mark.django_db(transaction=True)
    def test_02_users_username_not_auth(self, client, admin):
        response = client.get(f'/api/v1/users/{admin.username}/')

        assert response.status_code != 404, \
            'Страница `/api/v1/users/{username}/` не найдена, проверьте этот адрес в *urls.py*'

        assert response.status_code == 401, \
            'Проверьте, что при GET запросе `/api/v1/users/{username}/` без токена авторизации возвращается статус 401'

    @pytest.mark.django_db(transaction=True)
    def test_03_users_me_not_auth(self, client):
        response = client.get(f'/api/v1/users/me/')

        assert response.status_code != 404, \
            'Страница `/api/v1/users/me/` не найдена, проверьте этот адрес в *urls.py*'

        assert response.status_code == 401, \
            'Проверьте, что при GET запросе `/api/v1/users/me/` без токена авторизации возвращается статус 401'

    @pytest.mark.django_db(transaction=True)
    def test_04_users_get_auth(self, user_client, admin):
        response = user_client.get('/api/v1/users/')
        assert response.status_code != 404, \
            'Страница `/api/v1/users/` не найдена, проверьте этот адрес в *urls.py*'
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/users/` с токеном авторизации возвращается статус 200'
        data = response.json()
        assert 'count' in data, \
            'Проверьте, что при GET запросе `/api/v1/users/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `count`'
        assert 'next' in data, \
            'Проверьте, что при GET запросе `/api/v1/users/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `next`'
        assert 'previous' in data, \
            'Проверьте, что при GET запросе `/api/v1/users/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `previous`'
        assert 'results' in data, \
            'Проверьте, что при GET запросе `/api/v1/users/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `results`'
        assert data['count'] == 1, \
            'Проверьте, что при GET запросе `/api/v1/users/` возвращаете данные с пагинацией. ' \
            'Значение параметра `count` не правильное'
        assert type(data['results']) == list, \
            'Проверьте, что при GET запросе `/api/v1/users/` возвращаете данные с пагинацией. ' \
            'Тип параметра `results` должен быть список'
        assert len(data['results']) == 1 and data['results'][0].get('username') == admin.username \
            and data['results'][0].get('email') == admin.email, \
            'Проверьте, что при GET запросе `/api/v1/users/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` не правильное'

    @pytest.mark.django_db(transaction=True)
    def test_05_users_post_auth(self, user_client, admin):
        data = {}
        response = user_client.post('/api/v1/users/', data=data)
        assert response.status_code == 400, \
            'Проверьте, что при POST запросе `/api/v1/users/` с не правильными данными возвращает 400'
        data = {
            'username': 'TestUser1231231',
            'role': 'user'
        }
        response = user_client.post('/api/v1/users/', data=data)
        assert response.status_code == 400, \
            'Проверьте, что при POST запросе `/api/v1/users/` с не правильными данными возвращает 400'
        data = {
            'username': 'TestUser1231231',
            'role': 'user',
            'email': admin.email
        }
        response = user_client.post('/api/v1/users/', data=data)
        assert response.status_code == 400, \
            'Проверьте, что при POST запросе `/api/v1/users/` с не правильными данными возвращает 400. ' \
            '`Email` должен быть уникальный у каждого прользователя'
        data = {
            'username': admin.username,
            'role': 'user',
            'email': 'testuser@yamdb.fake'
        }
        response = user_client.post('/api/v1/users/', data=data)
        assert response.status_code == 400, \
            'Проверьте, что при POST запросе `/api/v1/users/` с не правильными данными возвращает 400. ' \
            '`Username` должен быть уникальный у каждого прользователя'
        data = {
            'username': 'TestUser1231231',
            'role': 'user',
            'email': 'testuser@yamdb.fake'
        }
        response = user_client.post('/api/v1/users/', data=data)
        assert response.status_code == 201, \
            'Проверьте, что при POST запросе `/api/v1/users/` с правильными данными возвращает 201.'
        data = {
            'first_name': 'fsdfsdf',
            'last_name': 'dsgdsfg',
            'username': 'TestUser4534',
            'bio': 'Jdlkjd',
            'role': 'moderator',
            'email': 'testuser2342@yamdb.fake'
        }
        response = user_client.post('/api/v1/users/', data=data)
        assert response.status_code == 201, \
            'Проверьте, что при POST запросе `/api/v1/users/` с правильными данными возвращает 201.'
        response_data = response.json()
        assert response_data.get('first_name') == data['first_name'], \
            'Проверьте, что при POST запросе `/api/v1/users/` с правильными данными возвращаете `first_name`.'
        assert response_data.get('last_name') == data['last_name'], \
            'Проверьте, что при POST запросе `/api/v1/users/` с правильными данными возвращаете `last_name`.'
        assert response_data.get('username') == data['username'], \
            'Проверьте, что при POST запросе `/api/v1/users/` с правильными данными возвращаете `username`.'
        assert response_data.get('bio') == data['bio'], \
            'Проверьте, что при POST запросе `/api/v1/users/` с правильными данными возвращаете `bio`.'
        assert response_data.get('role') == data['role'], \
            'Проверьте, что при POST запросе `/api/v1/users/` с правильными данными возвращаете `role`.'
        assert response_data.get('email') == data['email'], \
            'Проверьте, что при POST запросе `/api/v1/users/` с правильными данными возвращаете `email`.'
        assert get_user_model().objects.count() == 3, \
            'Проверьте, что при POST запросе `/api/v1/users/` вы создаёте пользователей.'
        response = user_client.get('/api/v1/users/')
        data = response.json()
        assert len(data['results']) == 3, \
            'Проверьте, что при GET запросе `/api/v1/users/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` не правильное'

    @pytest.mark.django_db(transaction=True)
    def test_06_users_username_get_auth(self, user_client, admin):
        user, moderator = create_users_api(user_client)
        response = user_client.get(f'/api/v1/users/{admin.username}/')
        assert response.status_code != 404, \
            'Страница `/api/v1/users/{username}/` не найдена, проверьте этот адрес в *urls.py*'
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/users/{username}/` с токеном авторизации возвращается статус 200'
        response_data = response.json()
        assert response_data.get('username') == admin.username, \
            'Проверьте, что при GET запросе `/api/v1/users/{username}/` возвращаете `username`.'
        assert response_data.get('email') == admin.email, \
            'Проверьте, что при GET запросе `/api/v1/users/{username}/` возвращаете `email`.'

        response = user_client.get(f'/api/v1/users/{moderator.username}/')
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/users/{username}/` с токеном авторизации возвращается статус 200'
        response_data = response.json()
        assert response_data.get('username') == moderator.username, \
            'Проверьте, что при GET запросе `/api/v1/users/{username}/` возвращаете `username`.'
        assert response_data.get('email') == moderator.email, \
            'Проверьте, что при GET запросе `/api/v1/users/{username}/` возвращаете `email`.'
        assert response_data.get('first_name') == moderator.first_name, \
            'Проверьте, что при GET запросе `/api/v1/users/` возвращаете `first_name`.'
        assert response_data.get('last_name') == moderator.last_name, \
            'Проверьте, что при GET запросе `/api/v1/users/` возвращаете `last_name`.'
        assert response_data.get('bio') == moderator.bio, \
            'Проверьте, что при GET запросе `/api/v1/users/` возвращаете `bio`.'
        assert response_data.get('role') == moderator.role, \
            'Проверьте, что при GET запросе `/api/v1/users/` возвращаете `role`.'

    @pytest.mark.django_db(transaction=True)
    def test_07_users_username_patch_auth(self, user_client, admin):
        user, moderator = create_users_api(user_client)
        data = {
            'first_name': 'Admin',
            'last_name': 'Test',
            'bio': 'description'
        }
        response = user_client.patch(f'/api/v1/users/{admin.username}/', data=data)
        assert response.status_code == 200, \
            'Проверьте, что при PATCH запросе `/api/v1/users/{username}/` с токеном авторизации возвращается статус 200'
        test_admin = get_user_model().objects.get(username=admin.username)
        assert test_admin.first_name == data['first_name'], \
            'Проверьте, что при PATCH запросе `/api/v1/users/{username}/` изменяете данные.'
        assert test_admin.last_name == data['last_name'], \
            'Проверьте, что при PATCH запросе `/api/v1/users/{username}/` изменяете данные.'
        response = user_client.patch(f'/api/v1/users/{user.username}/', data={'role': 'admin'})
        assert response.status_code == 200, \
            'Проверьте, что при PATCH запросе `/api/v1/users/{username}/` с токеном авторизации возвращается статус 200'
        client_user = auth_client(user)
        response = client_user.get(f'/api/v1/users/{admin.username}/')
        assert response.status_code == 200, \
            'Проверьте, что при PATCH запросе `/api/v1/users/{username}/` можно изменить роль пользователя'

    @pytest.mark.django_db(transaction=True)
    def test_08_users_username_delete_auth(self, user_client):
        user, moderator = create_users_api(user_client)
        response = user_client.delete(f'/api/v1/users/{user.username}/')
        assert response.status_code == 204, \
            'Проверьте, что при DELETE запросе `/api/v1/users/{username}/` возвращаете статус 204'
        assert get_user_model().objects.count() == 2, \
            'Проверьте, что при DELETE запросе `/api/v1/users/{username}/` удаляете пользователя'

    def check_permissions(self, user, user_name, admin):
        client_user = auth_client(user)
        response = client_user.get('/api/v1/users/')
        assert response.status_code == 403, \
            f'Проверьте, что при GET запросе `/api/v1/users/` ' \
            f'с токеном авторизации {user_name} возвращается статус 403'
        data = {
            'username': 'TestUser9876',
            'role': 'user',
            'email': 'testuser9876@yamdb.fake'
        }
        response = client_user.post('/api/v1/users/', data=data)
        assert response.status_code == 403, \
            f'Проверьте, что при POST запросе `/api/v1/users/` ' \
            f'с токеном авторизации {user_name} возвращается статус 403'

        response = client_user.get(f'/api/v1/users/{admin.username}/')
        assert response.status_code == 403, \
            f'Проверьте, что при GET запросе `/api/v1/users/{{username}}/` ' \
            f'с токеном авторизации {user_name} возвращается статус 403'
        data = {
            'first_name': 'Admin',
            'last_name': 'Test',
            'bio': 'description'
        }
        response = client_user.patch(f'/api/v1/users/{admin.username}/', data=data)
        assert response.status_code == 403, \
            f'Проверьте, что при PATCH запросе `/api/v1/users/{{username}}/` ' \
            f'с токеном авторизации {user_name} возвращается статус 403'
        response = client_user.delete(f'/api/v1/users/{admin.username}/')
        assert response.status_code == 403, \
            f'Проверьте, что при DELETE запросе `/api/v1/users/{{username}}/` ' \
            f'с токеном авторизации {user_name} возвращается статус 403'

    @pytest.mark.django_db(transaction=True)
    def test_09_users_check_permissions(self, user_client, admin):
        user, moderator = create_users_api(user_client)
        self.check_permissions(user, 'обычного пользователя', admin)
        self.check_permissions(moderator, 'модератора', admin)

    @pytest.mark.django_db(transaction=True)
    def test_10_users_me_get(self, user_client, admin):
        user, moderator = create_users_api(user_client)
        response = user_client.get(f'/api/v1/users/me/')
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/users/me/` с токеном авторизации возвращается статус 200'
        response_data = response.json()
        assert response_data.get('username') == admin.username, \
            'Проверьте, что при GET запросе `/api/v1/users/me/` возвращаете данные пользователя'
        client_user = auth_client(moderator)
        response = client_user.get(f'/api/v1/users/me/')
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/users/me/` с токеном авторизации возвращается статус 200'
        response_data = response.json()
        assert response_data.get('username') == moderator.username, \
            'Проверьте, что при GET запросе `/api/v1/users/me/` возвращаете данные пользователя'
        assert response_data.get('role') == 'moderator', \
            'Проверьте, что при GET запросе `/api/v1/users/me/` возвращаете данные пользователя'
        assert response_data.get('email') == moderator.email, \
            'Проверьте, что при GET запросе `/api/v1/users/me/` возвращаете данные пользователя'
        response = client_user.delete(f'/api/v1/users/me/')
        assert response.status_code == 405, \
            'Проверьте, что при DELETE запросе `/api/v1/users/me/` возвращается статус 405'

    @pytest.mark.django_db(transaction=True)
    def test_11_users_me_patch(self, user_client):
        user, moderator = create_users_api(user_client)
        data = {
            'first_name': 'Admin',
            'last_name': 'Test',
            'bio': 'description'
        }
        response = user_client.patch(f'/api/v1/users/me/', data=data)
        assert response.status_code == 200, \
            'Проверьте, что при PATCH запросе `/api/v1/users/me/` с токеном авторизации возвращается статус 200'
        response_data = response.json()
        assert response_data.get('bio') == 'description', \
            'Проверьте, что при PATCH запросе `/api/v1/users/me/` изменяете данные'
        client_user = auth_client(moderator)
        response = client_user.patch(f'/api/v1/users/me/', data={'first_name': 'NewTest'})
        test_moderator = get_user_model().objects.get(username=moderator.username)
        assert response.status_code == 200, \
            'Проверьте, что при PATCH запросе `/api/v1/users/me/` с токеном авторизации возвращается статус 200'
        assert test_moderator.first_name == 'NewTest', \
            'Проверьте, что при PATCH запросе `/api/v1/users/me/` изменяете данные'
