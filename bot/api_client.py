import logging
from typing import Tuple, Dict, Any, Optional
import aiohttp
from bot.config import BACKEND_API_URL, BOT_API_SECRET

logger = logging.getLogger("telegram_bot")


class BackendAPIClient:
    """
    Evently Django Backend API bilan asinxron muloqot qiluvchi mijoz.
    """

    def __init__(self, base_url: Optional[str] = None, bot_secret: Optional[str] = None):
        self.base_url = (base_url or BACKEND_API_URL).rstrip("/")
        self.bot_secret = bot_secret or BOT_API_SECRET

    async def confirm_telegram_link(
        self, token: str, chat_id: int
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Backend ga POST /api/v1/telegram/confirm/ so'rovini yuboradi.
        Qaytadi: (success: bool, response_dict: dict)
        """
        url = f"{self.base_url}/telegram/confirm/"
        headers = {
            "X-Bot-Secret": self.bot_secret,
            "Content-Type": "application/json",
        }
        payload = {
            "token": token,
            "chat_id": chat_id,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    data = await response.json()
                    if response.status == 200:
                        return True, data
                    else:
                        error_detail = data.get("detail", "Noma'lum xatolik yuz berdi.")
                        return False, {"detail": error_detail, "status": response.status}
        except Exception as exc:
            logger.error(f"Backend API ga ulanishda xatolik: {exc}", exc_info=True)
            return False, {"detail": "Backend server bilan bog'lanib bo'lmadi."}
