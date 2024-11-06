from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
api = ""
bot = Bot(token = api)
dp= Dispatcher(bot, storage= MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'], state=None)
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Рассчитать'), types.KeyboardButton('Информация'))
    await message.reply('Привет! Давай посчитаем твою норму калорий.', reply_markup=keyboard)

@dp.message_handler(text='Рассчитать', state=None)
async def set_age(message: types.Message, state: FSMContext):
    await message.reply('Введите свой возраст:')
    await state.set_state(UserState.age)

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.reply('Введите свой рост (в сантиметрах):')
    await state.set_state(UserState.growth)

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.reply('Введите свой вес (в килограммах):')
    await state.set_state(UserState.weight)

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']

    # Формула Миффлина - Сан Жеора (для женщин)
    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.reply(f'Ваша норма калорий: {calories:.0f} ккал')
    await state.finish()
 #Обработчик для всех остальных сообщений
@dp.message_handler()
async def all_message(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



