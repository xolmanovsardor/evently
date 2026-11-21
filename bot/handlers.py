from aiogram import Router, types
from aiogram.filters import CommandStart, Command, CommandObject
from bot.api_client import BackendAPIClient

router = Router(name="main_router")
api_client = BackendAPIClient()


@router.message(CommandStart())
async def handle_start(message: types.Message, command: CommandObject):
    """
    /start yoki /start <token> komandalarini qabul qiladi.
    Deep-linking orqali token kelsa, backend bilan chat_id ni bog'laydi.
    """
    token = command.args.strip() if command.args else None

    if token:
        # Foydalanuvchi saytdan generatsiya qilingan havola orqali kirdi
        success, result = await api_client.confirm_telegram_link(token=token, chat_id=message.chat.id)

        if success:
            full_name = result.get("full_name") or "Foydalanuvchi"
            email = result.get("email") or ""
            text = (
                f"✅ <b>Tabriklaymiz, {full_name}!</b>\n\n"
                f"Sizning Telegram hisobingiz Evently profilingizga (<code>{email}</code>) muvaffaqiyatli bog'landi.\n\n"
                f"Endi siz:\n"
                f"• Tadbirlarga ro'yxatdan o'tganingizda tasdiq xabarlarini;\n"
                f"• Tadbirlar boshlanishidan 24 soat oldin avtomatik eslatmalarni bevosita shu yerda qabul qilasiz!"
            )
        else:
            detail = result.get("detail", "Yaroqsiz token")
            text = (
                f"❌ <b>Bog'lashda xatolik yuz berdi:</b> {detail}\n\n"
                f"Iltimos, Evently veb-saytiga kirib, yangi havola oling yoki qo'llab-quvvatlash xizmatiga murojaat qiling."
            )
        await message.answer(text, parse_mode="HTML")
    else:
        # Oddiy /start bosilganda
        user_name = message.from_user.first_name if message.from_user else "Foydalanuvchi"
        text = (
            f"👋 Assalomu alaykum, <b>{user_name}</b>!\n\n"
            f"Men <b>Evently</b> platformasining rasmiy bildirishnoma va eslatmalar botiman.\n\n"
            f"Hisobingizni platformaga bog'lash uchun:\n"
            f"1. Evently platformasiga kiring;\n"
            f"2. Profilingizdan <b>Telegramni bog'lash</b> tugmasini bosing;\n"
            f"3. Botga taqdim etilgan havola orqali kiring.\n\n"
            f"Yordam uchun: /help buyrug'ini yuboring."
        )
        await message.answer(text, parse_mode="HTML")


@router.message(Command("help"))
async def handle_help(message: types.Message):
    """
    /help buyrug'i uchun yordam matni.
    """
    text = (
        f"ℹ️ <b>Evently Bot Yordam Markazi</b>\n\n"
        f"Mavjud buyruqlar:\n"
        f"• /start — Botni ishga tushirish\n"
        f"• /start [token] — Evently hisobingizni Telegram botga ulash\n"
        f"• /help — Bot haqida ma'lumot va yordam\n\n"
        f"<i>Savollar yoki takliflar bo'lsa, platforma ma'muriyatiga murojaat qiling.</i>"
    )
    await message.answer(text, parse_mode="HTML")
