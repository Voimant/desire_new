from aiogram import types, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards import main_keyboard, profile_markup, start_profile_markup, next_back_kb_markup, search_profile_markup
from keyboards import search_begin_markup
from aiogram.types import FSInputFile
from pprint import pprint
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from create_bot import bot, dp

class Fsm1(StatesGroup):
    message_all = State()
    image_al = State()
    resl = State()




# async def admin(message: types.Message):
#     await message.answer('Введите пароль:',)
#
# #@dp.message_handler()
# async def ad_key(message: types.Message):
#     if message.text == '124ffsf':
#         await message.answer('Меню админа', reply_markup=markup2)
#     elif message.text == "Контакты":
#         url = 'https://nb-bot.ru/#o_rasrabotchike'
#         pprint(get_test_re(url))
#
# async def mess_all(call):
#     await bot.send_message(call.from_user.id, 'Отправьте текст рассылки')
#     await Fsm1.message_all.set()
#
# async def image_all(message: types.Message, state: FSMContext):
#     await state.update_data(message_all=message.text)
#     await bot.send_message(message.chat.id, 'Добавьте картинку для рассылки')
#     await Fsm1.image_al.set()
#
# async def res(message: types.Message, state: FSMContext):
#     photos = message.photo[-1].file_id
#     await state.update_data(image_al=photos)
#     data = await state.get_data(state)
#
#     await bot.send_photo(message.chat.id, photo=data['image_al'], caption=data['message_all'])
#     await bot.send_message(message.chat.id, 'Проверяйте правильность сообщения и нажмите отправить', reply_markup=markup4)
#     await Fsm1.resl.set()
#
# async def sends_all(callback: types.CallbackQuery, state:FSMContext):
#     if callback.data == 'send':
#         data = await state.get_data(state)
#         for user_ids in list_id():
#             await bot.send_photo(user_ids, photo=data['image_al'], caption=data['message_all'])
#             # await bot.send_message(user_ids, data['message_all'])
#         await state.finish()
#     elif callback.data == 'cancel':
#         await bot.send_photo(callback.from_user.id, 'возврат в главное меню', reply_markup=markup)
#         await state.finish()