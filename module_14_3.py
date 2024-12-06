from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kbi = InlineKeyboardMarkup()
kbi2 = InlineKeyboardMarkup()
buttoni = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='Калории')
buttoni1 = InlineKeyboardButton(text='Формулы рассчёта', callback_data='Формулы')

button = KeyboardButton(text='Информация!')
button2 = KeyboardButton(text='Расчитать')
button3 = KeyboardButton(text='Купить')
kb.add(button, button2, button3)
kbi.add(buttoni, buttoni1)

for i in range(1, 5):
    kbi2.add(InlineKeyboardButton(f'Продукт {i}', callback_data='product_buying'))


@dp.message_handler(text='Купить')
async def handle_buy_button(message):
    await get_buying_list(message)


async def get_buying_list(message):
    product_info = 'Название: Product 1 | Описание: Обычный стандарт круглых таблеток. | Цена: 100 руб.'
    with open('1.png', 'rb') as img:
        await message.answer_photo(img, product_info)
    product_info2 = 'Название: Product 2 | Описание: Интересные таблетки ввиде бобов. | Цена: 200 руб.'
    with open('2.jpg', 'rb') as img2:
        await message.answer_photo(img2, product_info2)
    product_info3 = 'Название: Product 3 | Описание: Маленькие таблетки удобно пить. | Цена: 300 руб.'
    with open('3.jpg', 'rb') as img3:
        await message.answer_photo(img3, product_info3)
    product_info4 = 'Название: Product 4 | Описание: Самые эффективные таблетки даже цвет зеленый. | Цена: 400 руб.'
    with open('4.jpg', 'rb') as img4:
        await message.answer_photo(img4, product_info4)

    await message.answer('Выберите продукт для покупки:', reply_markup=kbi2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(text='Расчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kbi)


@dp.callback_query_handler(text='Формулы')
async def get_formulas(call):
    await call.message.answer('10 * вес(кг) + 6.25 * рост (см) – 4.92 * возраст – 161')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler(text='Информация!')
async def button1(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='Калории')
async def set_age(call):
    await call.message.answer('Введите свой возраст(г):', reply_markup=kb)
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост(см):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес(кг):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    await message.answer(f'Ваша норма калорий: {10 * data["weight"] + 6.25 * data["growth"] - 5 * data["age"] - 161}')
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start или нажмите кнопку "Информация!" чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
