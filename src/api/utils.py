from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_inline_keyboard(entities: Iterable = None, callback_prefix: str = None,
                             back_name: str = None, next_name: str = None) -> InlineKeyboardMarkup:
    if not entities:
        entities = []
    extra_buttons = []
    if back_name:
        extra_buttons.append(InlineKeyboardButton(text="◀️ Back", callback_data=back_name))
    if next_name:
        extra_buttons.append(InlineKeyboardButton(text="◀️ Next", callback_data=next_name))
    keyboard_buttons = [
        [InlineKeyboardButton(text=entity, callback_data=f"{callback_prefix}{entity}") for entity in entities],
        extra_buttons
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard
