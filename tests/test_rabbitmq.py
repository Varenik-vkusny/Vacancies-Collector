import pytest
import aio_pika
from unittest.mock import AsyncMock, MagicMock
from src.backend.main import put_task_to_queue


@pytest.mark.anyio
async def test_put_task_to_queue(mocker):

    # Делаем mock для publish
    mock_publish = AsyncMock()

    # Делаем mock для channel, делаем так чтобы при вызове publish
    # он возвращал mock_publish
    mock_channel = AsyncMock()
    mock_channel.default_exchange.publish = mock_publish

    # Делаем mock для connection
    # Делаем так, чтобы при вызове channel (который теперь можно вызвать через await)
    # он возвращал наш mock_channel
    # Делаем так, чтобы mock_connection можно было вызвать с помощью async with (__aenter__)
    mock_connection = AsyncMock()
    mock_connection.channel.return_value = mock_channel
    mock_connection.__aenter__.return_value = mock_connection

    # Подмена
    mocker.patch('src.backend.main.aio_pika.connect_robust', return_value=mock_connection)

    await put_task_to_queue()

    # Проверка всего
    mock_connection.channel.assert_awaited_once()
    
    mock_publish.assert_awaited_once()

    args, kwargs = mock_publish.await_args

    publish_message_object = args[0]
    publish_routing_key = kwargs['routing_key']

    assert isinstance(publish_message_object, aio_pika.Message)
    assert publish_message_object.body == b'start_parsing'
    assert publish_routing_key == 'parsing_queue'