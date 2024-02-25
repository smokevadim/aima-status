from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import SimpleCalendar, get_user_locale, SimpleCalendarCallback

from api import content, datatypes, menu
from api.fsm import Form

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(content.greet, reply_markup=menu.menu)


@router.message(F.text == "menu")
async def menu_handler(msg: Message):
    await msg.answer(content.menu, reply_markup=menu.menu)


@router.callback_query(F.data == "help")
async def help_handler(query: CallbackQuery):
    await query.message.answer(content.greet)


@router.callback_query(F.data == "subscribe")
async def subscribe_handler(query: CallbackQuery):
    calendar = SimpleCalendar(show_alerts=True)
    calendar.set_dates_range(datetime(2020, 1, 1), datetime.now())
    await query.message.answer(
        "Select a date when you applied for residence: ",
        reply_markup=await calendar.start_calendar(year=2023, month=1)
    )


@router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(
        locale=await get_user_locale(query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(query, callback_data)
    if selected:
        await state.set_state(Form.date)
        await state.update_data(date=date)
        await state.set_state(Form.city)
        await query.message.answer(
            f"You selected {date.strftime('%d/%m/%Y')}.\nNow, choose AIMA/SEF city: ",
            reply_markup=menu.cities_keyboard
        )
    else:
        await query.message.answer('Canceled date', reply_markup=menu.menu)


@router.callback_query(F.data.startswith('city_'))
async def aima_handler(query: CallbackQuery, state: FSMContext):
    await state.update_data(city=query.data)
    await query.message.answer(
        "Choose AIMA/SEF office: ",
        reply_markup=menu.aima_keyboard
    )


@router.callback_query(F.data.startswith('aima_'))
async def article_handler(query: CallbackQuery, state: FSMContext):
    await state.update_data(aima=query.data)
    await query.message.answer(
        "Choose the residence article: ",
        reply_markup=menu.articles_keyboard
    )


@router.callback_query(F.data.startswith("article_"))
async def preview_handler(query: CallbackQuery, state: FSMContext):
    await state.update_data(article=query.data)
    data = await state.get_data()
    preview = datatypes.PreviewData(**data).preview_text()
    await query.message.answer(
        f"Everything correct?\n{preview}",
        reply_markup=menu.preview_keyboard
    )


@router.callback_query(F.data.startswith("finish"))
async def preview_handler(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    preview = datatypes.PreviewData(**data)
    await query.message.answer(
        content.subscription_finish,
        reply_markup=menu.menu
    )


@router.callback_query(F.data == "report_status")
async def report_status_handler(query: CallbackQuery):
    await query.message.answer("Reported!")
