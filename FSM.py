from aiogram.dispatcher.filters.state import StatesGroup, State


class SiteStates(StatesGroup):
    write_name = State()
    write_site = State()
