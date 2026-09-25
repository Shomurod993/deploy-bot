from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.default.main import main_keyboard
from loader import db
from states.main import RegisterState, EditState

start_router = Router()

@start_router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Hello {message.from_user.first_name}", reply_markup=main_keyboard)

@start_router.message(F.text == '📝 Регистрация')
async def register_func(message: Message, state: FSMContext):
    await message.answer('Имя: ')
    await state.set_state(RegisterState.first_name)

@start_router.message(RegisterState.first_name)
async def register_first_name(message: Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    await message.answer('Фамилия: ')
    await state.set_state(RegisterState.last_name)

@start_router.message(RegisterState.last_name)
async def register_last_name(message: Message, state: FSMContext):
    last_name = message.text
    await state.update_data(last_name=last_name)
    await message.answer('Возраст: ')
    await state.set_state(RegisterState.age)

@start_router.message(RegisterState.age)
async def register_age(message: Message, state: FSMContext):
    age = message.text
    await state.update_data(age=age)
    await message.answer('📸 Отправьте фотографию: ')
    await state.set_state(RegisterState.photo)


@start_router.message(RegisterState.photo)
async def register_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)
    await message.answer('Номер телефона: ')
    await state.set_state(RegisterState.phone)


@start_router.message(RegisterState.phone)
async def register_phone(message: Message, state: FSMContext):
    phone = message.text

    data = await state.get_data()

    first_name = data['first_name']
    last_name = data['last_name']
    age = data['age']
    photo = data['photo']
    try:
        db.add_user(
            id=message.from_user.id,
            username=message.from_user.username,
            first_name=first_name,
            last_name=last_name,
            age=age,
            phone=phone,
        )
    except Exception as e:
        print(e)
    await message.answer('Muvoffaqiyatli: ')
    await state.clear()

@start_router.message(F.text == '👤 Мои данные')
async def my_data(message: Message):

    user = db.select_user(id=message.from_user.id)
    if not user:
        await message.answer('❌ Вы ещё не зарегистрированы!')
        return
    await message.answer_photo(
        photo=user[6],
        caption=(
            f'👤 <b>Мои данные</b>\n\n'
            f'🆔 Telegram ID: {user[0]}\n'
            f'👤 Имя: {user[2]}\n'
            f'📝 Фамилия: {user[3]}\n'
            f'🎂 Возраст: {user[4]}\n'
            f'📱 Телефон: {user[5]}'
        )
    )

@start_router.message(F.text == '✏️ Изменить данные')
async def edit_start(message: Message, state: FSMContext):

    user = db.select_user(
        id=message.from_user.id
    )

    if not user:
        await message.answer(
            '❌ Вы ещё не зарегистрированы!'
        )
        return

    await message.answer('📸 Отправьте новую фотографию:')
    await state.set_state(EditState.photo)

@start_router.message(EditState.photo)
async def edit_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer('❌ Отправьте именно фотографию!')
        return
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)
    await message.answer('Введите новое имя:')
    await state.set_state(EditState.first_name)

@start_router.message(EditState.first_name)
async def edit_first_name(message: Message, state: FSMContext):

    await state.update_data(
        first_name=message.text
    )

    await message.answer('Введите новую фамилию:')
    await state.set_state(EditState.last_name)


@start_router.message(EditState.last_name)
async def edit_last_name(message: Message, state: FSMContext):

    await state.update_data(
        last_name=message.text
    )

    await message.answer('Введите новый возраст:')
    await state.set_state(EditState.age)


@start_router.message(EditState.age)
async def edit_age(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer(
            '❌ Возраст должен быть числом!'
        )
        return

    await state.update_data(
        age=int(message.text)
    )

    await message.answer(
        'Введите новый номер телефона:'
    )

    await state.set_state(EditState.phone)


@start_router.message(EditState.phone)
async def edit_phone(message: Message, state: FSMContext):

    phone = message.text

    data = await state.get_data()

    db.update_user(
        id=message.from_user.id,
        first_name=data['first_name'],
        last_name=data['last_name'],
        age=data['age'],
        phone=phone
    )

    db.update_photo(id=message.from_user.id, photo_id=data['photo'])

    await state.clear()

    await message.answer(
        '✅ Данные успешно изменены!',
        reply_markup=main_keyboard
    )

@start_router.message(F.text == '🗑 Удалить данные')
async def delete_data(message: Message):

    user = db.select_user(id=message.from_user.id)
    if not user:
        await message.answer('❌ У вас нет данных!')
        return

    db.delete_user(id=message.from_user.id)
    await message.answer('🗑 Ваши данные удалены!', reply_markup=main_keyboard)

@start_router.message(F.text == '👥 Все студенты')
async def all_students(message: Message):
    users = db.select_all_users()
    if not users:
        await message.answer('📭 Студентов пока нет')
        return
    text = '👥<b>Все студенты:</b>/n/n'

    for number, user in enumerate(users, start=1):
        text += (
            f'{number}. '
            f'{user[2]} {user[3]} — '
            f'{user[4]} лет\n'
        )

    await message.answer(text)

@start_router.message(Command('stats'))
async def stats(message: Message):

    ADMIN_ID = 5069071823

    if message.from_user.id != ADMIN_ID:
        await message.answer(
            '❌ У вас нет доступа!'
        )
        return

    count = db.count_users()[0]

    await message.answer(
        f'👥 Всего студентов: {count}'
    )

    













