import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram import types
from aiogram.filters import CommandObject

from bot.api_client import BackendAPIClient
from bot.handlers import handle_start, handle_help


def run_async(coro):
    return asyncio.run(coro)


class TestBotAPIClient:
    def test_confirm_telegram_link_success(self):
        async def _test():
            client = BackendAPIClient(base_url="http://testserver/api/v1", bot_secret="test-secret")

            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={
                "detail": "Telegram hisobi muvaffaqiyatli bog'landi.",
                "email": "user@example.com",
                "full_name": "Test User"
            })

            mock_post = MagicMock()
            mock_post.__aenter__ = AsyncMock(return_value=mock_response)
            mock_post.__aexit__ = AsyncMock(return_value=None)

            mock_session = MagicMock()
            mock_session.post.return_value = mock_post
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=None)

            with patch("aiohttp.ClientSession", return_value=mock_session):
                success, data = await client.confirm_telegram_link("token-123", 998877)
                assert success is True
                assert data["email"] == "user@example.com"
                assert data["full_name"] == "Test User"

        run_async(_test())

    def test_confirm_telegram_link_failure(self):
        async def _test():
            client = BackendAPIClient(base_url="http://testserver/api/v1", bot_secret="test-secret")

            mock_response = AsyncMock()
            mock_response.status = 400
            mock_response.json = AsyncMock(return_value={"detail": "Yaroqsiz token."})

            mock_post = MagicMock()
            mock_post.__aenter__ = AsyncMock(return_value=mock_response)
            mock_post.__aexit__ = AsyncMock(return_value=None)

            mock_session = MagicMock()
            mock_session.post.return_value = mock_post
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=None)

            with patch("aiohttp.ClientSession", return_value=mock_session):
                success, data = await client.confirm_telegram_link("bad-token", 998877)
                assert success is False
                assert "Yaroqsiz" in data["detail"]

        run_async(_test())

    def test_confirm_telegram_link_network_exception(self):
        async def _test():
            client = BackendAPIClient(base_url="http://testserver/api/v1", bot_secret="test-secret")

            mock_session = MagicMock()
            mock_session.post.side_effect = Exception("Connection refused")
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=None)

            with patch("aiohttp.ClientSession", return_value=mock_session):
                success, data = await client.confirm_telegram_link("token", 123)
                assert success is False
                assert "bog'lanib bo'lmadi" in data["detail"]

        run_async(_test())


class TestBotHandlers:
    def test_start_without_token(self):
        async def _test():
            message = AsyncMock(spec=types.Message)
            message.chat = MagicMock(id=12345)
            message.from_user = MagicMock(first_name="Sardor")
            message.answer = AsyncMock()

            command = CommandObject(prefix="/", command="start", args=None)

            await handle_start(message, command)
            assert message.answer.called
            text_arg = message.answer.call_args[0][0]
            assert "Assalomu alaykum" in text_arg
            assert "Sardor" in text_arg

        run_async(_test())

    def test_start_with_valid_token(self):
        async def _test():
            message = AsyncMock(spec=types.Message)
            message.chat = MagicMock(id=12345)
            message.from_user = MagicMock(first_name="Sardor")
            message.answer = AsyncMock()

            command = CommandObject(prefix="/", command="start", args="valid_token_abc")

            with patch("bot.handlers.api_client.confirm_telegram_link", new_callable=AsyncMock) as mock_confirm:
                mock_confirm.return_value = (True, {
                    "detail": "Success",
                    "full_name": "Sardor Xolmanov",
                    "email": "sardor@example.com"
                })

                await handle_start(message, command)
                assert message.answer.called
                text_arg = message.answer.call_args[0][0]
                assert "Tabriklaymiz" in text_arg
                assert "Sardor Xolmanov" in text_arg
                assert "sardor@example.com" in text_arg

        run_async(_test())

    def test_start_with_invalid_token(self):
        async def _test():
            message = AsyncMock(spec=types.Message)
            message.chat = MagicMock(id=12345)
            message.from_user = MagicMock(first_name="Sardor")
            message.answer = AsyncMock()

            command = CommandObject(prefix="/", command="start", args="invalid_token")

            with patch("bot.handlers.api_client.confirm_telegram_link", new_callable=AsyncMock) as mock_confirm:
                mock_confirm.return_value = (False, {
                    "detail": "Yaroqsiz yoki eskirgan token."
                })

                await handle_start(message, command)
                assert message.answer.called
                text_arg = message.answer.call_args[0][0]
                assert "xatolik yuz berdi" in text_arg
                assert "Yaroqsiz" in text_arg

        run_async(_test())

    def test_help_handler(self):
        async def _test():
            message = AsyncMock(spec=types.Message)
            message.answer = AsyncMock()

            await handle_help(message)
            assert message.answer.called
            text_arg = message.answer.call_args[0][0]
            assert "Evently Bot Yordam Markazi" in text_arg
            assert "/start" in text_arg

        run_async(_test())
