from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    date = State()
    city = State()
    aima = State()
    article = State()
