import pytest

from .common import create_users_api, auth_client, create_genre, create_categories, create_titles


class Test04TitleAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_title_not_auth(self, client):
        response = client.get('/api/v1/titles/')
        assert response.status_code != 404, \
            'Страница `/api/v1/titles/` не найдена, проверьте этот адрес в *urls.py*'
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/titles/` без токена авторизации возвращается статус 200'

    @pytest.mark.django_db(transaction=True)
    def test_02_title(self, user_client):
        genres = create_genre(user_client)
        categories = create_categories(user_client)
        data = {}
        response = user_client.post('/api/v1/titles/', data=data)
        assert response.status_code == 400, \
            'Проверьте, что при POST запросе `/api/v1/titles/` с не правильными данными возвращает статус 400'
        data = {'name': 'Поворот туда', 'year': 2000, 'genre': [genres[0]['slug'], genres[1]['slug']],
                'category': categories[0]['slug'], 'description': 'Крутое пике'}
        response = user_client.post('/api/v1/titles/', data=data)
        assert response.status_code == 201, \
            'Проверьте, что при POST запросе `/api/v1/titles/` с правильными данными возвращает статус 201'
        data = {'name': 'Проект', 'year': 2020, 'genre': [genres[2]['slug']], 'category': categories[1]['slug'],
                'description': 'Главная драма года'}
        response = user_client.post('/api/v1/titles/', data=data)
        assert response.status_code == 201, \
            'Проверьте, что при POST запросе `/api/v1/titles/` с правильными данными возвращает статус 201'
        assert type(response.json().get('id')) == int, \
            'Проверьте, что при POST запросе `/api/v1/titles/` возвращаете данные созданного объекта. ' \
            'Значение `id` нет или не является целым числом.'
        response = user_client.get('/api/v1/titles/')
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/titles/` возвращает статус 200'
        data = response.json()
        assert 'count' in data, \
            'Проверьте, что при GET запросе `/api/v1/titles/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `count`'
        assert 'next' in data, \
            'Проверьте, что при GET запросе `/api/v1/titles/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `next`'
        assert 'previous' in data, \
            'Проверьте, что при GET запросе `/api/v1/titles/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `previous`'
        assert 'results' in data, \
            'Проверьте, что при GET запросе `/api/v1/titles/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `results`'
        assert data['count'] == 2, \
            'Проверьте, что при GET запросе `/api/v1/titles/` возвращаете данные с пагинацией. ' \
            'Значение параметра `count` не правильное'
        assert type(data['results']) == list, \
            'Проверьте, что при GET запросе `/api/v1/titles/` возвращаете данные с пагинацией. ' \
            'Тип параметра `results` должен быть список'
        assert len(data['results']) == 2, \
            'Проверьте, что при GET запросе `/api/v1/titles/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` не правильное'
        if data['results'][0].get('name') == 'Поворот туда':
            title = data['results'][0]
        elif data['results'][1].get('name') == 'Поворот туда':
            title = data['results'][1]
        else:
            assert False, \
                'Проверьте, что при GET запросе `/api/v1/titles/` возвращаете данные с пагинацией. ' \
                'Значение параметра `results` неправильное, `name` не найдено или не сохранилось при POST запросе.'
        assert title.get('rating') is None, \
            'Проверьте, что при GET запросе `/api/v1/titles/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` неправильное, `rating` без отзывов должен быть равен `None`'
        assert title.get('category') == categories[0], \
            'Проверьте, что при GET запросе `/api/v1/titles/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` неправильное, значение `category` неправильное ' \
            'или не сохранилось при POST запросе.'
        assert genres[0] in title.get('genre', []) and genres[1] in title.get('genre', []), \
            'Проверьте, что при GET запросе `/api/v1/titles/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` неправильное, значение `genre` неправильное ' \
            'или не сохранилось при POST запросе.'
        assert title.get('year') == 2000, \
            'Проверьте, что при GET запросе `/api/v1/titles/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` неправильное, значение `year` неправильное ' \
            'или не сохранилось при POST запросе.'
        assert title.get('description') == 'Крутое пике', \
            'Проверьте, что при GET запросе `/api/v1/titles/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` неправильное, значение `description` неправильное ' \
            'или не сохранилось при POST запросе.'
        assert type(title.get('id')) == int, \
            'Проверьте, что при GET запросе `/api/v1/titles/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` неправильное, значение `id` нет или не является целым числом.'
        data = {'name': 'Поворот', 'year': 2020, 'genre': [genres[1]['slug']],
                'category': categories[1]['slug'], 'description': 'Крутое пике'}
        user_client.post('/api/v1/titles/', data=data)
        response = user_client.get(f'/api/v1/titles/?genre={genres[1]["slug"]}')
        data = response.json()
        assert len(data['results']) == 2, \
            'Проверьте, что при GET запросе `/api/v1/titles/` фильтуется по `genre` параметру `slug` жанра'
        response = user_client.get(f'/api/v1/titles/?category={categories[0]["slug"]}')
        data = response.json()
        assert len(data['results']) == 1, \
            'Проверьте, что при GET запросе `/api/v1/titles/` фильтуется по `category` параметру `slug` категории'
        response = user_client.get(f'/api/v1/titles/?year=2000')
        data = response.json()
        assert len(data['results']) == 1, \
            'Проверьте, что при GET запросе `/api/v1/titles/` фильтуется по `year` параметру года'
        response = user_client.get(f'/api/v1/titles/?name=Поворот')
        data = response.json()
        assert len(data['results']) == 2, \
            'Проверьте, что при GET запросе `/api/v1/titles/` фильтуется по `name` параметру названия'

    @pytest.mark.django_db(transaction=True)
    def test_03_titles_detail(self, client, user_client):
        titles, categories, genres = create_titles(user_client)
        response = client.get(f'/api/v1/titles/{titles[0]["id"]}/')
        assert response.status_code != 404, \
            'Страница `/api/v1/titles/{title_id}/` не найдена, проверьте этот адрес в *urls.py*'
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/` ' \
            'без токена авторизации возвращается статус 200'
        data = response.json()
        assert type(data.get('id')) == int, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/` возвращаете данные объекта. ' \
            'Значение `id` нет или не является целым числом.'
        assert data.get('category') == categories[0], \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/` возвращаете данные объекта. ' \
            'Значение `category` неправильное.'
        assert data.get('name') == titles[0]['name'], \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/` возвращаете данные объекта. ' \
            'Значение `name` неправильное.'
        data = {
            'name': 'Новое название',
            'category': categories[1]['slug']
        }
        response = user_client.patch(f'/api/v1/titles/{titles[0]["id"]}/', data=data)
        assert response.status_code == 200, \
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/` возвращается статус 200'
        data = response.json()
        assert data.get('name') == 'Новое название', \
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/` возвращаете данные объекта. ' \
            'Значение `name` изменено.'
        response = user_client.get(f'/api/v1/titles/{titles[0]["id"]}/')
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/` ' \
            'без токена авторизации возвращается статус 200'
        data = response.json()
        assert data.get('category') == categories[1], \
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/` изменяете значение `category`.'
        assert data.get('name') == 'Новое название', \
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/` изменяете значение `name`.'

        response = user_client.delete(f'/api/v1/titles/{titles[0]["id"]}/')
        assert response.status_code == 204, \
            'Проверьте, что при DELETE запросе `/api/v1/titles/{title_id}/` возвращаете статус 204'
        response = user_client.get('/api/v1/titles/')
        test_data = response.json()['results']
        assert len(test_data) == len(titles) - 1, \
            'Проверьте, что при DELETE запросе `/api/v1/titles/{title_id}/` удаляете объект'

    def check_permissions(self, user, user_name, titles, categories, genres):
        client_user = auth_client(user)
        data = {'name': 'Чудо юдо', 'year': 1999, 'genre': [genres[2]['slug'], genres[1]['slug']],
                'category': categories[0]['slug'], 'description': 'Бум'}
        response = client_user.post('/api/v1/titles/', data=data)
        assert response.status_code == 403, \
            f'Проверьте, что при POST запросе `/api/v1/titles/` ' \
            f'с токеном авторизации {user_name} возвращается статус 403'
        response = client_user.patch(f'/api/v1/titles/{titles[0]["id"]}/', data=data)
        assert response.status_code == 403, \
            f'Проверьте, что при PATCH запросе `/api/v1/titles/{{title_id}}/` ' \
            f'с токеном авторизации {user_name} возвращается статус 403'
        response = client_user.delete(f'/api/v1/titles/{titles[0]["id"]}/')
        assert response.status_code == 403, \
            f'Проверьте, что при DELETE запросе `/api/v1/titles/{{title_id}}/` ' \
            f'с токеном авторизации {user_name} возвращается статус 403'

    @pytest.mark.django_db(transaction=True)
    def test_04_titles_check_permission(self, client, user_client):
        titles, categories, genres = create_titles(user_client)
        data = {'name': 'Чудо юдо', 'year': 1999, 'genre': [genres[2]['slug'], genres[1]['slug']],
                'category': categories[0]['slug'], 'description': 'Бум'}
        response = client.post('/api/v1/titles/', data=data)
        assert response.status_code == 401, \
            f'Проверьте, что при POST запросе `/api/v1/titles/` ' \
            f'без токена авторизации возвращается статус 401'
        response = client.patch(f'/api/v1/titles/{titles[0]["id"]}/', data=data)
        assert response.status_code == 401, \
            f'Проверьте, что при PATCH запросе `/api/v1/titles/{{title_id}}/` ' \
            f'без токена авторизации возвращается статус 401'
        response = client.delete(f'/api/v1/titles/{titles[0]["id"]}/')
        assert response.status_code == 401, \
            f'Проверьте, что при DELETE запросе `/api/v1/titles/{{title_id}}/` ' \
            f'без токена авторизации возвращается статус 401'
        user, moderator = create_users_api(user_client)
        self.check_permissions(user, 'обычного пользователя', titles, categories, genres)
        self.check_permissions(moderator, 'модератора', titles, categories, genres)
