from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Пересадка волосся", callback_data="hair")],
    [InlineKeyboardButton(text="Пересадка бороди", callback_data="beard")],
    [InlineKeyboardButton(text="Пересадка брів", callback_data="brows")]
])

consult_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Так", callback_data="yes")],
    [InlineKeyboardButton(text="Ні", callback_data="no")]
])
