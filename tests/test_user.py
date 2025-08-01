import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.backend import models


@pytest.mark.anyio
async def test_user_register(client: AsyncClient, db_session: AsyncSession):

    json = {
        'telegram_id': 1,
        'name': 'testuser'
    }

    response = await client.post('/users/register', json=json)

    assert response.status_code == 201

    response_data = response.json()

    assert 'id' in response_data
    assert response_data['name'] == 'testuser'
    assert response_data['telegram_id'] == 1

    user_id = response_data['id']
    user_name = response_data['name']

    query = select(models.User).where(models.User.id == user_id)

    result = await db_session.execute(query)

    db_user = result.scalar_one_or_none()

    assert db_user is not None
    assert db_user.id == user_id
    assert db_user.name == user_name