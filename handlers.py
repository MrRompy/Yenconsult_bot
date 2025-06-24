from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID
from keyboards import main_menu

router = Router()

# Глобальное хранилище ID клиентов для ответов от менеджера
admin_reply_targets = {}

# === 1. Приветствие и выбор направления === #
@router.message(F.text == "/start")
async def start_quiz(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пересадка волосся", callback_data="hair")],
        [InlineKeyboardButton(text="Пересадка бороди", callback_data="beard")],
        [InlineKeyboardButton(text="Пересадка брів", callback_data="brows")]
    ])
    await message.answer(
        "Привіт! Мене звати Вікторія, я медичний консультант 💙\n"
        "Підкажіть, будь ласка, що саме вас цікавить:",
        reply_markup=keyboard
    )


# === 2. Информация по каждому направлению === #
@router.callback_query(F.data.in_(["hair", "beard", "brows"]))
async def procedure_info(callback: CallbackQuery):
    data = {
        "hair":
            "🔹 Пересадка волосся в Києві з турецькими лікарями\n\n"
            "💰 Вартість: 2800 €\nМетод: FUE або DHI (максимум графт)\n\n"
            "У вартість включено:\n"
            "• операція з пересадки від 2000 до 5500 графтів;\n"
            "• усі необхідні аналізи перед операцією;\n"
            "• миття голови 10 днів після операції;\n"
            "• медикаменти, вітаміни та засоби догляду;\n"
            "• 2 сеанси PRP;\n"
            "• супровід україномовного консультанта;\n"
            "• гарантійний сертифікат;\n"
            "• підтримка 24/7 протягом року.\n\n"
            "Консультація безкоштовна 💙\n\n"
            "Бажаєте отримати консультацію?",
            
        "beard":
            "🔹 Пересадка бороди в Києві з турецькими лікарями\n\n"
            "💰 Вартість: 2800 €\nМетод: DHI (максимум графт)\n\n"
            "У вартість включено:\n"
            "• операція з пересадки бороди від 1500 до 3500 графтів;\n"
            "• усі необхідні аналізи перед операцією;\n"
            "• миття бороди 10 днів після операції;\n"
            "• медикаменти, вітаміни та засоби догляду;\n"
            "• 2 сеанси PRP;\n"
            "• супровід україномовного консультанта;\n"
            "• гарантійний сертифікат;\n"
            "• підтримка 24/7 протягом року.\n\n"
            "Консультація безкоштовна 💙\n\n"
            "Бажаєте отримати консультацію?",
            
        "brows":
            "🔹 Пересадка брів в Києві з турецькими лікарями\n\n"
            "💰 Вартість: 1500 €\nМетод: DHI (максимум графт)\n\n"
            "У вартість включено:\n"
            "• операція з пересадки брів від 800 до 1500 графтів;\n"
            "• усі необхідні аналізи перед операцією;\n"
            "• миття брів 10 днів після операції;\n"
            "• медикаменти, вітаміни та засоби догляду;\n"
            "• 2 сеанси PRP;\n"
            "• супровід україномовного консультанта;\n"
            "• гарантійний сертифікат;\n"
            "• підтримка 24/7 протягом року.\n\n"
            "Консультація безкоштовна 💙\n\n"
            "Бажаєте отримати консультацію?",
            
    }
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Так", callback_data="yes")],
        [InlineKeyboardButton(text="Ні", callback_data="no")]
    ])
    await callback.message.answer(data[callback.data], reply_markup=keyboard)
    await callback.answer()


# === 3. Да / Нет === #
@router.callback_query(F.data == "yes")
async def consult_yes(callback: CallbackQuery):
    user = callback.from_user

    # Кнопка "Відповісти"
    reply_btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Відповісти", callback_data=f"reply_to:{user.id}")]
        ]
    )

    # Сообщение клиенту
    await callback.message.answer(
        "Супер! 💙 Я підключаю нашого медичного консультанта Вікторію.\n\n"
        "А ви тим часом, будь ласка, надішліть фото:\n"
        "• спереду (анфас)\n• зліва\n• справа\n• потилиця\n• зверху голови\n\n"
        "Це потрібно для оцінки донорської зони та точного визначення кількості графтів."
    )

    # Сообщение менеджеру с кнопкой
    await callback.bot.send_message(
        ADMIN_ID,
        f"🔔 Користувач @{user.username or 'без username'} хоче консультацію.\n"
        f"👤 Ім'я: {user.full_name}\n🆔 ID: {user.id}",
        reply_markup=reply_btn
    )

    await callback.answer()



@router.callback_query(F.data == "no")
async def consult_no(callback: CallbackQuery):
    await callback.message.answer(
        "Добре! Якщо у вас з’являться запитання, звертайтеся, я завжди рада допомогти 💙\n\n"
        "Переходьте на наші ресурси. Там багато прикладів ДО/ПІСЛЯ та реальних відгуків пацієнтів\n"
        "📺 YouTube: https://www.youtube.com/@HairGlobalMedik.ua\n"
        "📸 Instagram: https://www.instagram.com/kyiv.hair.globalmedik"
    )
    await callback.answer()


# === 4. Фото от клиента === #
@router.message(F.photo)
async def handle_photo(message: Message):
    user = message.from_user
    caption = (
        f"📷 Фото від користувача:\n"
        f"👤 Ім'я: {user.full_name}\n"
        f"🔗 Username: @{user.username or 'немає'}\n"
        f"🆔 ID: {user.id}"
    )
    reply_btn = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="💬 Відповісти", callback_data=f"reply_to:{user.id}")
        ]]
    )
    await message.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=caption,
        reply_markup=reply_btn
    )


# === 5. Ответ менеджера === #
@router.callback_query(F.data.startswith("reply_to:"))
async def ask_reply(callback: CallbackQuery):
    try:
        parts = callback.data.split(":")
        if len(parts) != 2:
            await callback.message.answer("❌ Некоректний формат callback data.")
            return
        user_id = int(parts[1])
        admin_reply_targets[callback.from_user.id] = user_id
        await callback.message.answer("✍️ Введіть текст для клієнта:")
    except Exception as e:
        await callback.message.answer(f"❌ Помилка при обробці відповіді:\n{e}")


@router.message()
async def handle_message(message: Message):
    user = message.from_user

    # Менеджер отвечает клиенту
    if user.id == ADMIN_ID and user.id in admin_reply_targets:
        target_id = admin_reply_targets.pop(user.id)
        try:
            await message.bot.send_message(target_id, f"\n\n{message.text}")
            await message.answer("✅ Повідомлення надіслано клієнту.")
        except Exception as e:
            await message.answer(f"❌ Помилка надсилання клієнту:\n{e}")
        return

    # Клиент пишет сообщение
    caption = (
        f"📨 Повідомлення від користувача:\n"
        f"👤 Ім'я: {user.full_name}\n"
        f"🔗 Username: @{user.username or 'немає'}\n"
        f"🆔 ID: {user.id}\n\n"
        f"{message.text}"
    )
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Відповісти", callback_data=f"reply_to:{user.id}")]
        ]
    )
    await message.bot.send_message(ADMIN_ID, caption, reply_markup=reply_markup)
    await message.answer("Вікторія вже прямує до вас 🌪 — у робочий час ми завжди на зв'язку.")