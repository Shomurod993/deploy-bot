from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    phone = State()
    photo = State()


class EditState(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    phone = State()
    photo = State()


