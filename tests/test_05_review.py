import pytest

from .common import create_users_api, auth_client, create_titles, create_reviews


class Test05ReviewAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_review_not_auth(self, client, user_client):
        titles, _, _ = create_titles(user_client)
        response = client.get(f'/api/v1/titles/{titles[0]["id"]}/reviews/')
        assert response.status_code != 404, \
            'Страница `/api/v1/titles/{title_id}/reviews/` не найдена, проверьте этот адрес в *urls.py*'
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/` ' \
            'без токена авторизации возвращается статус 200'

    def create_review(self, client_user, title_id, text, score):
        data = {'text': text, 'score': score}
        response = client_user.post(f'/api/v1/titles/{title_id}/reviews/', data=data)
        assert response.status_code == 201, \
            'Проверьте, что при POST запросе `/api/v1/titles/{title_id}/reviews/` ' \
            'с правильными данными возвращает статус 201, api доступен для любого аутентифицированные пользователя'
        return response

    @pytest.mark.django_db(transaction=True)
    def test_02_review(self, user_client, admin):
        titles, _, _ = create_titles(user_client)
        user, moderator = create_users_api(user_client)
        client_user = auth_client(user)
        client_moderator = auth_client(moderator)
        data = {}
        response = user_client.post(f'/api/v1/titles/{titles[0]["id"]}/reviews/', data=data)
        assert response.status_code == 400, \
            'Проверьте, что при POST запросе `/api/v1/titles/{title_id}/reviews/` ' \
            'с не правильными данными возвращает статус 400'
        self.create_review(user_client, titles[0]["id"], 'qwerty', 5)
        self.create_review(client_user, titles[0]["id"], 'qwerty123', 3)
        self.create_review(client_moderator, titles[0]["id"], 'qwerty321', 4)

        self.create_review(user_client, titles[1]["id"], 'qwerty432', 2)
        self.create_review(client_user, titles[1]["id"], 'qwerty534', 4)
        response = self.create_review(client_moderator, titles[1]["id"], 'qwerty231', 3)

        assert type(response.json().get('id')) == int, \
            'Проверьте, что при POST запросе `/api/v1/titles/{title_id}/reviews/` ' \
            'возвращаете данные созданного объекта. Значение `id` нет или не является целым числом.'

        data = {'text': 'kjdfg', 'score': 4}
        response = user_client.post(f'/api/v1/titles/999/reviews/', data=data)
        assert response.status_code == 404, \
            'Проверьте, что при POST запросе `/api/v1/titles/{title_id}/reviews/` ' \
            'с не существующим title_id возвращается статус 404.'
        data = {'text': 'аывв', 'score': 11}
        response = user_client.post(f'/api/v1/titles/{titles[0]["id"]}/reviews/', data=data)
        assert response.status_code == 400, \
            'Проверьте, что при POST запросе `/api/v1/titles/{title_id}/reviews/` ' \
            'с `score` больше 10 возвращается статус 400.'
        data = {'text': 'аывв', 'score': 0}
        response = user_client.post(f'/api/v1/titles/{titles[0]["id"]}/reviews/', data=data)
        assert response.status_code == 400, \
            'Проверьте, что при POST запросе `/api/v1/titles/{title_id}/reviews/` ' \
            'с `score` меньше 1 возвращается статус 400.'
        data = {'text': 'аывв', 'score': 2}
        response = user_client.post(f'/api/v1/titles/{titles[0]["id"]}/reviews/', data=data)
        assert response.status_code == 400, \
            'Проверьте, что при POST запросе `/api/v1/titles/{title_id}/reviews/` ' \
            'на уже оставленный отзыв для объекта возвращается статус 400.'

        response = user_client.get(f'/api/v1/titles/{titles[0]["id"]}/reviews/')
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/` возвращает статус 200'
        data = response.json()
        assert 'count' in data, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `count`'
        assert 'next' in data, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `next`'
        assert 'previous' in data, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `previous`'
        assert 'results' in data, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `results`'
        assert data['count'] == 3, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/` возвращаете данные с пагинацией. ' \
            'Значение параметра `count` не правильное'
        assert type(data['results']) == list, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/` возвращаете данные с пагинацией. ' \
            'Тип параметра `results` должен быть список'
        assert len(data['results']) == 3, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` не правильное'

        if data['results'][0].get('text') == 'qwerty':
            review = data['results'][0]
        elif data['results'][1].get('text') == 'qwerty':
            review = data['results'][1]
        elif data['results'][2].get('text') == 'qwerty':
            review = data['results'][2]
        else:
            assert False, \
                'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/` ' \
                'возвращаете данные с пагинацией. Значение параметра `results` неправильное, ' \
                '`text` не найдено или не сохранилось при POST запросе.'
        assert review.get('score') == 5, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` неправильное, `score` не найдено или не сохранилось при POST запросе'
        assert review.get('author') == admin.username, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` неправильное, `author` не найдено или не сохранилось при POST запросе.'
        assert review.get('pub_date'), \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` неправильное, `pub_date` не найдено.'
        assert type(review.get('id')) == int, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` неправильное, значение `id` нет или не является целым числом.'

        response = user_client.get(f'/api/v1/titles/{titles[0]["id"]}/')
        data = response.json()
        assert data.get('rating') == 4, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/` ' \
            'с отзывами возвращается правильно значение `rating`'
        response = user_client.get(f'/api/v1/titles/{titles[1]["id"]}/')
        data = response.json()
        assert data.get('rating') == 3, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/` ' \
            'с отзывами возвращается правильно значение `rating`'

    @pytest.mark.django_db(transaction=True)
    def test_03_review_detail(self, client, user_client, admin):
        reviews, titles, user, moderator = create_reviews(user_client, admin)
        response = client.get(f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[0]["id"]}/')
        assert response.status_code != 404, \
            'Страница `/api/v1/titles/{title_id}/reviews/{review_id}/` не найдена, проверьте этот адрес в *urls.py*'
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` ' \
            'без токена авторизации возвращается статус 200'
        data = response.json()
        assert type(data.get('id')) == int, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` ' \
            'возвращаете данные объекта. Значение `id` нет или не является целым числом.'
        assert data.get('score') == reviews[0]['score'], \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` ' \
            'возвращаете данные объекта. Значение `score` неправильное.'
        assert data.get('text') == reviews[0]['text'], \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` ' \
            'возвращаете данные объекта. Значение `text` неправильное.'
        assert data.get('author') == reviews[0]['author'], \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` ' \
            'возвращаете данные объекта. Значение `author` неправильное.'

        data = {
            'text': 'rewq',
            'score': 10
        }
        response = user_client.patch(f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[0]["id"]}/', data=data)
        assert response.status_code == 200, \
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` ' \
            'возвращается статус 200'
        data = response.json()
        assert data.get('text') == 'rewq', \
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` ' \
            'возвращаете данные объекта. Значение `text` изменено.'
        response = user_client.get(f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[0]["id"]}/')
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` ' \
            'без токена авторизации возвращается статус 200'
        data = response.json()
        assert data.get('text') == 'rewq', \
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` ' \
            'изменяете значение `text`.'
        assert data.get('score') == 10, \
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` ' \
            'изменяете значение `score`.'

        client_user = auth_client(user)
        data = {
            'text': 'fgf',
            'score': 1
        }
        response = client_user.patch(f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[2]["id"]}/', data=data)
        assert response.status_code == 403, \
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` ' \
            'от обычного пользователя при попытки изменить не свой отзыв возвращается статус 403'

        data = {
            'text': 'jdfk',
            'score': 7
        }
        response = client_user.patch(f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[1]["id"]}/', data=data)
        assert response.status_code == 200, \
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` ' \
            'возвращается статус 200'
        data = response.json()
        assert data.get('text') == 'jdfk', \
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` ' \
            'возвращаете данные объекта. Значение `text` изменено.'
        response = user_client.get(f'/api/v1/titles/{titles[0]["id"]}/')
        data = response.json()
        assert data.get('rating') == 7, \
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/` ' \
            'с отзывами возвращается правильно значение `rating`'

        client_moderator = auth_client(moderator)
        response = client_moderator.delete(f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[1]["id"]}/')
        assert response.status_code == 204, \
            'Проверьте, что при DELETE запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` ' \
            'возвращаете статус 204'
        response = user_client.get(f'/api/v1/titles/{titles[0]["id"]}/reviews/')
        test_data = response.json()['results']
        assert len(test_data) == len(reviews) - 1, \
            'Проверьте, что при DELETE запросе `/api/v1/titles/{title_id}/reviews/{review_id}/` удаляете объект'

    def check_permissions(self, user, user_name, reviews, titles):
        client_user = auth_client(user)
        data = {'text': 'jdfk', 'score': 7}
        response = client_user.patch(f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[0]["id"]}/', data=data)
        assert response.status_code == 403, \
            f'Проверьте, что при PATCH запросе `/api/v1/titles/{{title_id}}/reviews/{{review_id}}/` ' \
            f'с токеном авторизации {user_name} возвращается статус 403'
        response = client_user.delete(f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[0]["id"]}/')
        assert response.status_code == 403, \
            f'Проверьте, что при DELETE запросе `/api/v1/titles/{{title_id}}/reviews/{{review_id}}/` ' \
            f'с токеном авторизации {user_name} возвращается статус 403'

    @pytest.mark.django_db(transaction=True)
    def test_04_reviews_check_permission(self, client, user_client, admin):
        reviews, titles, user, moderator = create_reviews(user_client, admin)
        data = {'text': 'jdfk', 'score': 7}
        response = client.post(f'/api/v1/titles/{titles[0]["id"]}/reviews/', data=data)
        assert response.status_code == 401, \
            f'Проверьте, что при POST запросе `/api/v1/titles/{{title_id}}/reviews/` ' \
            f'без токена авторизации возвращается статус 401'
        response = client.patch(f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[1]["id"]}/', data=data)
        assert response.status_code == 401, \
            f'Проверьте, что при PATCH запросе `/api/v1/titles/{{title_id}}/reviews/{{review_id}}/` ' \
            f'без токена авторизации возвращается статус 401'
        response = client.delete(f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[1]["id"]}/')
        assert response.status_code == 401, \
            f'Проверьте, что при DELETE запросе `/api/v1/titles/{{title_id}}/reviews/{{review_id}}/` ' \
            f'без токена авторизации возвращается статус 401'
        self.check_permissions(user, 'обычного пользователя', reviews, titles)
