from aiogram import Router, types
from bot_config import database
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

survey_router = Router()


class BookSurvey(StatesGroup):
    name = State()
    age = State()
    occupation = State()
    salary = State()


@survey_router.message(Command('survey'))
async def start_survey(message: types.Message, state: FSMContext):
    await state.set_state(BookSurvey.name)
    await message.answer('Enter your name')


@survey_router.message(BookSurvey.name)
async def process_name(message: types.Message, state:FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookSurvey.age)
    await message.answer('Enter your age')


@survey_router.message(BookSurvey.age)
async def process_age(message: types.Message, state: FSMContext):
    age = int(message.text)
    if age < 17:
        await state.clear()
        await message.answer('Спасибо за прохождения опроса')
    else:
        await state.update_data(age=message.text)
        await state.set_state(BookSurvey.occupation)
        await message.answer('Enter: ваш род занятий')


@survey_router.message(BookSurvey.occupation)
async def process_occupation(message: types.Message, state: FSMContext):
    await state.update_data(occupation=message.text)
    await state.set_state(BookSurvey.salary)
    await message.answer('Enter: вашу заработную плату')


@survey_router.message(BookSurvey.salary)
async def process_salary(message: types.Message, state: FSMContext):
    await state.update_data(salary=message.text)
    data = await state.get_data()
    print(data)
    await database.execute('''
                        INSERT INTO survey_results (name, age, occupation, salary) 
                        VALUES (?, ?, ?, ?)
    ''', (data['name'], data['age'], data['occupation'], data['salary']))
    await state.clear()
    await message.answer('Спасибо: за прохождение опроса!')