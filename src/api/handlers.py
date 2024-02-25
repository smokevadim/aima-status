from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import SimpleCalendarCallback

from api import usecases

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await usecases.start(msg)


@router.message(F.text == "menu")
async def menu_handler(msg: Message):
    await usecases.show_menu(msg)


@router.callback_query(F.data == "help")
async def help_handler(query: CallbackQuery):
    await usecases.help(query)


@router.callback_query(F.data == "subscribe")
async def subscribe_handler(query: CallbackQuery):
    await usecases.subscribe(query)


@router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    await usecases.process_calendar(query, callback_data, state)


@router.callback_query(F.data.startswith('city_'))
async def aima_handler(query: CallbackQuery, state: FSMContext):
    await usecases.aima(query, state)


@router.callback_query(F.data.startswith('aima_'))
async def article_handler(query: CallbackQuery, state: FSMContext):
    await usecases.article(query, state)


@router.callback_query(F.data.startswith("article_"))
async def preview_handler(query: CallbackQuery, state: FSMContext):
    await usecases.preview(query, state)


@router.callback_query(F.data.startswith("finish"))
async def finish_handler(query: CallbackQuery, state: FSMContext):
    await usecases.finish(query, state)


@router.callback_query(F.data == "report_status")
async def report_status_handler(query: CallbackQuery, state: FSMContext):
    await usecases.report_status(query, state)
