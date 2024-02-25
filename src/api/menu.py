from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from api import datatypes
from api import utils

menu = [
    [InlineKeyboardButton(text="📝 Subscribe", callback_data="subscribe"),
     InlineKeyboardButton(text="🖼 Report status", callback_data="report_status")],
    [InlineKeyboardButton(text="🔎 Help", callback_data="help")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
# exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Back to menu")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Back to menu", callback_data="menu")]])

calendar_keyboard = utils.generate_inline_keyboard(back_name='subscribe', next_name='city')

cities = [str(datatypes.City(_)) for _ in ('Lisbon', 'Setubal', 'Algarve', 'Porto')]
cities_keyboard = utils.generate_inline_keyboard(cities, datatypes.City.prefix)

aima = [str(datatypes.AIMA(_)) for _ in ('Alfa', 'Bravo', 'Charly', 'Delta', 'Echo')]
aima_keyboard = utils.generate_inline_keyboard(aima, datatypes.AIMA.prefix)

articles = [str(datatypes.Article(_)) for _ in ('90.2', '89.1', '77', '90.33')]
articles_keyboard = utils.generate_inline_keyboard(articles, datatypes.Article.prefix)

preview_keyboard = utils.generate_inline_keyboard(back_name='subscribe', next_name='finish')
