import pytest
import aiohttp
from aiohttp import ClientConnectionError
from aioresponses import aioresponses
from main import check_methods, is_url, main
from unittest.mock import patch


@pytest.mark.asyncio
async def test_is_url():
    assert await is_url("https://youtube.com") is True
    assert await is_url("https://youtube.com") is True
    assert await is_url("youtube.com") is False
    assert await is_url("ftp://youtube.com") is False


@pytest.mark.asyncio
async def test_check_methods():
    url = "https://youtube.com"
    with aioresponses() as mocked:
        mocked.get(url, status=200)
        mocked.post(url, status=400)
        mocked.put(url, status=405)
        mocked.delete(url, status=405)
        mocked.head(url, status=200)
        mocked.options(url, status=405)
        mocked.patch(url, status=405)

        result = await check_methods(url)

    expected = {
        "GET": 200,
        "POST": 400,
        "PUT": 405,
        "DELETE": 405,
        "HEAD": 200,
        "OPTIONS": 405,
        "PATCH": 405,
    }
    assert result == expected


@pytest.mark.asyncio
async def test_check_methods_connection_error():
    url = "https://not-url.com"
    with aioresponses() as mocked:
        mocked.get(url, exception=ClientConnectionError("Ошибка подключения"))

        result = await check_methods(url)

    assert result == {}


@pytest.mark.asyncio
async def test_check_methods_client_error():
    url = "https://youtube.com"
    with aioresponses() as mocked:
        mocked.get(url, exception=aiohttp.ClientError("Ошибка клиента"))

        result = await check_methods(url)

    assert result == {}


@pytest.mark.asyncio
async def test_main_valid_url(mocker):
    inputs = ["1", "https://youtube.com"]
    expected_output = {"https://youtube.com": {"GET": 200}}

    with patch("builtins.input", side_effect=inputs):
        mock_check_methods = mocker.patch("main.check_methods", return_value={"GET": 200})
        with patch("builtins.print") as mock_print:
            await main()

    mock_print.assert_any_call("\nРезультат работы программы:")
    mock_print.assert_any_call(expected_output)
    mock_check_methods.assert_called_once_with("https://youtube.com")


@pytest.mark.asyncio
async def test_main_invalid_url(mocker):
    inputs = ["1", "not_url"]

    with patch("builtins.input", side_effect=inputs):
        with patch("builtins.print") as mock_print:
            await main()

    mock_print.assert_any_call('Строка "not_url" не является ссылкой.')
    mock_print.assert_any_call("\nРезультат работы программы:")
    mock_print.assert_any_call({})
