from datetime import datetime

from aiogram_calendar import SimpleCalendar, get_user_locale

from api import content, menu, datatypes
from api.fsm import Form


async def start(msg):
    await msg.answer(content.greet, reply_markup=menu.menu)


async def show_menu(msg):
    await msg.answer(content.menu, reply_markup=menu.menu)


async def help(query):
    await query.message.answer(content.greet)


async def subscribe(query):
    calendar = SimpleCalendar(show_alerts=True)
    calendar.set_dates_range(datetime(2020, 1, 1), datetime.now())
    await query.message.answer(
        "Select a date when you applied for residence: ",
        reply_markup=await calendar.start_calendar(year=2023, month=1)
    )


async def process_calendar(query, callback_data, state):
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
            reply_markup=await menu.create_cities_keyboard()
        )
    else:
        await query.message.answer('Canceled date', reply_markup=menu.menu)


async def aima(query, state):
    await state.update_data(city=query.data)
    await query.message.answer(
        "Choose AIMA/SEF office: ",
        reply_markup=menu.aima_keyboard
    )


async def article(query, state):
    await state.update_data(aima=query.data)
    await query.message.answer(
        "Choose the residence article: ",
        reply_markup=menu.articles_keyboard
    )


async def preview(query, state):
    await state.update_data(article=query.data)
    data = await state.get_data()
    preview = datatypes.PreviewData(**data).preview_text()
    await query.message.answer(
        f"Everything correct?\n{preview}",
        reply_markup=menu.preview_keyboard
    )


async def finish(query, state):
    data = await state.get_data()
    preview = datatypes.PreviewData(**data)
    await query.message.answer(
        content.subscription_finish,
        reply_markup=menu.menu
    )


async def report_status(query, state):
    await query.message.answer("Reported!")
