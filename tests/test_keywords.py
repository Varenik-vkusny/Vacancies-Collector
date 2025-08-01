import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend import models


@pytest.mark.anyio
async def test_create_keyword(client: AsyncClient, db_session: AsyncSession):

    # ПРЕДУСЛОВИЕ
    user = models.User(id=1, telegram_id=1, name='createkeyword')

    db_session.add(user)
    await db_session.commit()


    json = {
        'telegram_id': user.telegram_id,
        'text': 'python'
    }

    response = await client.post('/keywords', json=json)

    assert response.status_code == 201

    keyword_data = response.json()

    assert 'id' in keyword_data
    assert 'text' in keyword_data

    db_keyword = await db_session.get(models.Keywords, keyword_data['id'])

    assert db_keyword is not None
    assert db_keyword.text == 'python'



@pytest.mark.anyio
async def test_duplicate_keyword(client: AsyncClient, db_session: AsyncSession):
    
    # ПРЕДУСЛОВИЕ
    user = models.User(id=2, telegram_id=2, name='duplicateuser')
    existing_keyword = models.Keywords(id=1, text='python', user_id=user.id)
    db_session.add_all([user, existing_keyword])
    await db_session.commit()


    json = {
        'telegram_id': user.telegram_id,
        'text': 'python'
    }

    response = await client.post('/keywords', json=json)

    assert response.status_code == 409
    assert response.json()['detail'] == 'У вас уже есть такое ключевое слово'



@pytest.mark.anyio
async def test_nonexistent_user_post(client: AsyncClient):

    # ПРЕДУСЛОВИЕ

    json = {
        'telegram_id': 23946324,
        'text': 'python'
    }

    response = await client.post('/keywords', json=json)

    assert response.status_code == 404
    assert response.json()['detail'] == 'Пользователь не найден'



@pytest.mark.anyio
async def test_get_keywords(client: AsyncClient, db_session: AsyncSession):

    # ПРЕДУСЛОВИЕ
    user = models.User(id=3, telegram_id=3, name='getkwuser')
    kw1 = models.Keywords(id=2, text='python', user_id=user.id)
    kw2 = models.Keywords(id=3, text='API', user_id=user.id)

    db_session.add_all([user, kw1, kw2])
    await db_session.commit()


    params = {
        'telegram_id': user.telegram_id
    }

    response = await client.get('/keywords', params=params)

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)

    keywords_text = {item['text'] for item in data}
    assert 'python' in keywords_text
    assert 'API' in keywords_text



@pytest.mark.anyio
async def test_nonexistent_user_get(client: AsyncClient):

    params = {
        'telegram_id': 98765
    }

    response = await client.get('/keywords', params=params)

    assert response.status_code == 404
    assert response.json()['detail'] == 'Пользователь не найден'



@pytest.mark.anyio
async def test_no_keywords_get(client: AsyncClient, db_session: AsyncSession):

    # ПРЕДУСЛОВИЕ
    user = models.User(id=4, telegram_id=4, name='nokwuser')

    db_session.add(user)
    await db_session.commit()

    params = {
        'telegram_id': user.telegram_id
    }

    response = await client.get('/keywords', params=params)

    assert response.status_code == 404
    assert response.json()['detail'] == 'У вас нет заданных ключевых слов.'



@pytest.mark.anyio
async def test_delete_keywords(client: AsyncClient, db_session: AsyncSession):

    # ПРЕДУСЛОВИЕ

    user = models.User(id=5, telegram_id=5, name='deletekwuser')
    kw = models.Keywords(id=4, text='python', user_id=user.id)

    db_session.add_all([user, kw])
    await db_session.commit()


    params = {
        'telegram_id': user.telegram_id,
        'keyword_text': kw.text
    }

    response = await client.delete('/keywords', params=params)

    assert response.status_code == 204



@pytest.mark.anyio
async def test_nonexistent_user_delete_kw(client: AsyncClient):

    params = {
        'telegram_id': 87482394,
        'keyword_text': 'python'
    }

    response = await client.delete('/keywords', params=params)

    assert response.status_code == 404
    assert response.json()['detail'] == 'Пользователь не найден'



@pytest.mark.anyio
async def test_no_keywords_delete(client: AsyncClient, db_session: AsyncSession):

    # ПРЕДУСЛОВИЕ

    user = models.User(id=6, telegram_id=6, name='nokwdeleteuser')

    db_session.add(user)
    await db_session.commit()

    params = {
        'telegram_id': user.telegram_id,
        'keyword_text': 'python'
    }

    response = await client.delete('/keywords', params=params)

    assert response.status_code == 404
    assert response.json()['detail'] == 'У вас нет заданных ключевых слов, чтобы удалить ключи сначала задайте новые'