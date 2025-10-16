import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# =============== CONFIG ===============
BOT_TOKEN = "8409337414:AAF__2KloxUy49Hj2_3fLOWmtes9Bc67_x4"
AI_API_URL = "https://viscodev.x10.mx/ChatGPT-4-turbo/api.php"

ADMINS = [7098943602]
PREMIUM_USERS = set()
# =====================================

# ✅ Botni to‘g‘ri ishga tushirish (parse_mode HTML)
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# =============== MENU ===============
def main_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💻 Kod snippetlar"), KeyboardButton(text="🌐 API izlash")],
            [KeyboardButton(text="🧠 Intervyu testlar"), KeyboardButton(text="💼 Freelance loyihalar")],
            [KeyboardButton(text="🤖 AI yordamchi")]
        ],
        resize_keyboard=True
    )
    return kb
# ====================================

# =============== /START ===============
@dp.message(CommandStart())
async def start_cmd(msg: types.Message):
    await msg.answer(
        f"👋 Salom, <b>{msg.from_user.first_name}</b>!\n\n"
        "Men — <b>DevHelper AI Bot</b> 🤖\n"
        "Dasturchilar uchun kuchli yordamchiman 💻\n\n"
        "🧩 Bo‘limlardan birini tanlang:",
        reply_markup=main_menu()
    )
# ====================================

def is_premium(user_id: int) -> bool:
    return user_id in PREMIUM_USERS or user_id in ADMINS

# =============== SNIPPETS ===============
SNIPPETS = {
    "python sort list": "my_list = [5,2,9]\nmy_list.sort()\nprint(my_list)",
    "flask route": "@app.route('/')\ndef home():\n    return 'Hello Flask!'",
    "js fetch": "fetch('url').then(res=>res.json()).then(data=>console.log(data))"
}

@dp.message(F.text == "💻 Kod snippetlar")
async def show_snippets(msg: types.Message):
    txt = "🔍 Mashhur snippetlar:\n\n"
    for k in SNIPPETS.keys():
        txt += f"• <code>{k}</code>\n"
    txt += "\nKod nomini yozing (masalan: <b>python sort list</b>)"
    await msg.answer(txt)
# =======================================

# =============== API SEARCH ===============
API_LINKS = {
    "requests": "https://requests.readthedocs.io/",
    "flask": "https://flask.palletsprojects.com/",
    "aiogram": "https://docs.aiogram.dev/",
    "fastapi": "https://fastapi.tiangolo.com/"
}

@dp.message(F.text == "🌐 API izlash")
async def api_section(msg: types.Message):
    txt = "🔗 Mashhur API hujjatlar:\n"
    for name, url in API_LINKS.items():
        txt += f"• <b>{name}</b> — {url}\n"
    txt += "\nAPI nomini yozing (masalan: <b>flask</b>)"
    await msg.answer(txt)
# ========================================

# =============== INTERVIEW TEST ===============
TESTS = [
    {"q": "Python’da list va tuple farqi?", "a": "List o‘zgaradi, tuple o‘zgarmaydi."},
    {"q": "OOP nima?", "a": "Object-Oriented Programming — obyektga yo‘naltirilgan dasturlash."},
    {"q": "HTTP 404 kodi nimani bildiradi?", "a": "Sahifa topilmadi."}
]

@dp.message(F.text == "🧠 Intervyu testlar")
async def start_test(msg: types.Message):
    if not is_premium(msg.from_user.id):
        return await msg.answer("🔒 Bu bo‘lim faqat PREMIUM foydalanuvchilar uchun!")
    await msg.answer("🧩 Testni boshlaymiz!\n\nJavob yozing:")
    for i, t in enumerate(TESTS, start=1):
        await msg.answer(f"{i}. {t['q']}\n\n👉 Javob: {t['a']}")
# =============================================

# =============== FREELANCE ===============
PROJECTS = [
    "🧑‍💻 Flask API loyihasi — $80",
    "🌍 React landing page — $50",
    "🤖 Telegram bot (aiogram) — $100"
]

@dp.message(F.text == "💼 Freelance loyihalar")
async def freelance_jobs(msg: types.Message):
    txt = "💼 Oxirgi freelance buyurtmalar:\n\n" + "\n".join(PROJECTS)
    if not is_premium(msg.from_user.id):
        txt += "\n\n⚠️ To‘liq ro‘yxat uchun PREMIUM ga o‘ting!"
    await msg.answer(txt)
# ========================================

# =============== AI YORDAMCHI ===============
@dp.message(F.text == "🤖 AI yordamchi")
async def ai_info(msg: types.Message):
    await msg.answer("🧠 Menga savol yozing, masalan:\n<code>Python da fayl o‘qish qanday?</code>")

@dp.message(F.text.regexp(r".+"))
async def ai_response(msg: types.Message):
    text = msg.text.lower()
    user_id = msg.from_user.id

    if text in SNIPPETS:
        return await msg.answer(f"<b>{text}</b>:\n<code>{SNIPPETS[text]}</code>")
    if text in API_LINKS:
        return await msg.answer(f"🔗 {API_LINKS[text]}")

    await msg.answer("⏳ Javob olinmoqda...")

    async with aiohttp.ClientSession() as session:
        payload = {"text": msg.text, "chat_id": str(user_id), "message_id": str(msg.message_id)}
        try:
            async with session.post(AI_API_URL, json=payload, timeout=60) as resp:
                data = await resp.json()
                if data.get("success"):
                    await msg.answer(data["response"])
                else:
                    await msg.answer("⚠️ Xatolik: " + data.get("error", "noma’lum"))
        except Exception as e:
            await msg.answer(f"❌ AI bilan bog‘lanib bo‘lmadi.\n{e}")
# =========================================

# =============== ADMIN (PREMIUM) ===============
@dp.message(F.text.startswith("/premium"))
async def add_premium(msg: types.Message):
    if msg.from_user.id not in ADMINS:
        return await msg.answer("⛔ Siz admin emassiz!")
    try:
        user_id = int(msg.text.split()[1])
        PREMIUM_USERS.add(user_id)
        await msg.answer(f"✅ {user_id} premiumga qo‘shildi!")
    except:
        await msg.answer("❌ Foydalanuvchi ID ni yozing: /premium 123456789")
# =========================================

# =============== RUN =====================
async def main():
    print("✅ DevHelper AI Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
