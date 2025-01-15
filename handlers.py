import asyncio
import time

from aiogram import types, Dispatcher, Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.middleware import FSMContextMiddleware
from aiogram.types import Message, CallbackQuery
from keyboards import main_keyboard, profile_markup, start_profile_markup, next_back_kb_markup, search_profile_markup, \
    city_markup, again_markup, start_profile_markup_1, edit_profile_markup, edit_pro_markup, edit_pro_cancel, \
    edit_pro_cancel_markup, age_markup, admin_markup, admin_1_markup, cancel_markup, key_markup, new_go, \
    new_start_markup
from keyboards import search_begin_markup
from aiogram.types import FSInputFile, BufferedInputFile
from pprint import pprint
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from acquaintances_db.db_func import add_user, search, search3, liked, not_liked, update_user_index, search_user, \
    my_anketa, update_index, list_liked_users, list_not_liked_users, update_user_data, update_nick_name, update_age, \
    update_gender, update_photo, update_about_me, update_preferences, update_city, update_preferences_age, list_id, \
    report, delete_user, db_bun, db_chat_id_user, db_rebun
from acquaintances_db.db import conn
from middleware import AuthoMiddlware
from source.reports import get_log_errors
import config
from aiogram.exceptions import TelegramForbiddenError

bot = Bot(token=config.TOKEN)
ADMIN_LIST = [634112358, 6192099919, 5923668994, 423947942, 497948297, 1985555563, 7241936347]
router = Router()
router.message.middleware(AuthoMiddlware())
router.callback_query.middleware(AuthoMiddlware())


STOP_WORDS = ['Помощь', 'Перейти в наш чат']

class FSMprofile(StatesGroup):
    sex = State()
    name = State()
    photo = State()
    age = State()
    text_profile = State()
    search_profile = State()
    city = State()
    age_seach_s = State()


@router.callback_query(F.data == 'cancel')
async def get_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer('Начнем поиск?', reply_markup=search_begin_markup)



@router.message(Command('start'))
async def cmd_start(mess: types.Message, state: FSMContext):
    await state.clear()
    us_name = mess.from_user.username
    if search_user(us_name) is None:
        await bot.send_message(mess.chat.id, 'Привет', reply_markup=main_keyboard)
        await bot.send_message(mess.chat.id, 'Ознакомься с правилами и заполни анкету для продолжения', reply_markup=new_start_markup)
    else:
        await state.clear()
        await bot.send_message(mess.chat.id, 'Бот обновлен', reply_markup=main_keyboard)
        await bot.send_message(mess.chat.id, 'Начнем поиск?', reply_markup=search_begin_markup)


@router.callback_query(F.data == 'reg')
async def cmd_start(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    us_name = call.from_user.username
    if search_user(us_name) is None:
        await bot.send_message(call.from_user.id, 'Кто вы?', reply_markup=start_profile_markup)
        await state.set_state(FSMprofile.sex)
    else:
        await state.clear()
        await bot.send_message(call.from_user.id, 'Бот обновлен', reply_markup=main_keyboard)
        await bot.send_message(call.from_user.id, 'Начнем поиск?', reply_markup=search_begin_markup)


@router.message(Command('my_profile'))
async def cmd_my_profile(message: types.Message):
    us_name = message.from_user.username
    info = my_anketa(us_name)
    if int(info[0]["preferences_age"]) == 20:
        o_output = (f'Ваша анкета\n'
                    f'Имя: {info[0]["nick_name"]} {info[0]["gender"]}\n'
                    f'Возраст: {info[0]["age"]}\n'
                    f'О себе: {info[0]["about_me"]}\n'
                    f'Кого ищу: {info[0]["preferences"]}\n'
                    f'Город: {info[0]["city"]}\n'
                    f'Предпочитаемый возраст: 18-40')
        await bot.send_photo(message.chat.id, info[0]['photo'], caption=o_output, reply_markup=edit_profile_markup)
    elif int(info[0]["preferences_age"]) != 20:
        o_output = (f'Ваша анкета\n'
                    f'Имя: {info[0]["nick_name"]} {info[0]["gender"]}\n'
                    f'Возраст: {info[0]["age"]}\n'
                    f'О себе: {info[0]["about_me"]}\n'
                    f'Кого ищу: {info[0]["preferences"]}\n'
                    f'Город: {info[0]["city"]}\n'
                    f'Предпочитаемый возраст: 40+')
        await bot.send_photo(message.chat.id, info[0]['photo'], caption=o_output, reply_markup=edit_profile_markup)


@router.callback_query(F.data == 'edit_profile')
async def edit_pro(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, 'Заполни анкету для продолжения', reply_markup=main_keyboard)
    await bot.send_message(call.from_user.id, 'Кто вы?', reply_markup=start_profile_markup)
    await state.set_state(FSMprofile.sex)


@router.callback_query(FSMprofile.sex)
async def name_state(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(sex=call.data)
    await bot.send_message(call.from_user.id, "Напишите как вас зовут", reply_markup=next_back_kb_markup)
    await state.set_state(FSMprofile.name)


@router.message(FSMprofile.name)
async def photo_state(message: types.Message, state: FSMContext):
    if message.text is not None and len(message.text) < 25 and message.text not in STOP_WORDS:
        await state.update_data(name=message.text)
        await state.set_state(FSMprofile.photo)
        await bot.send_message(message.chat.id,
                               'Выберите фото для вашей анкеты. На фото должны быть вы. Не допускаются фото посторонних предметов и других людей',
                               reply_markup=next_back_kb_markup)
    else:
        await bot.send_message(message.chat.id, 'Введите имя буквами и цифрами не более 25 символов')


@router.message(FSMprofile.photo)
async def about_state(message: types.Message, state: FSMContext):
    try:
        photos = message.photo[-1].file_id
        print(photos)
        await state.update_data(photo=photos)
        await state.set_state(FSMprofile.text_profile)
        await bot.send_message(message.chat.id, 'Заполните о себе буквами и цифрами, так же описание не может быть более 1024 символа', reply_markup=next_back_kb_markup)
    except TypeError:
        await bot.send_message(message.chat.id, "Фото в анкете обязательно! Нажмите на скрепку и прикрепите фото", reply_markup=next_back_kb_markup)
        await state.set_state(FSMprofile.photo)


@router.message(FSMprofile.text_profile)
async def age_state(message: types.Message, state: FSMContext):
    if message.text not in STOP_WORDS:
        await state.update_data(text_profile=message.text)
        await bot.send_message(message.chat.id, 'Укажите ваш возраст', reply_markup=next_back_kb_markup)
        await state.set_state(FSMprofile.age)
    else:
        await state.set_state(FSMprofile.text_profile)
        await message.answer('Напишите о себе', reply_markup=next_back_kb_markup)


@router.message(FSMprofile.age)
async def search_state(message: types.Message, state: FSMContext):
    try:
        if message.text == int or int(message.text) > 18 and int(message.text) < 100 and message.text not in STOP_WORDS:
            await state.update_data(age=message.text)
            await bot.send_message(message.chat.id, 'Кого будем для вас искать?', reply_markup=start_profile_markup_1)
            await state.set_state(FSMprofile.search_profile)
        else:
            await bot.send_message(message.chat.id, "Введите возраст от 18 до 100 лет")
            await state.set_state(FSMprofile.age)
    except Exception as e:
        get_log_errors(e)
        await bot.send_message(message.chat.id, "Введите возраст от 18 до 100 лет")
        await state.set_state(FSMprofile.age)


@router.callback_query(FSMprofile.search_profile)
async def search_city(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(search_profile=call.data)
    await bot.send_message(call.from_user.id, 'Выберете доступный город для поиска', reply_markup=city_markup)
    await state.set_state(FSMprofile.city)


@router.callback_query(FSMprofile.city)
async def age_seach(call: types.CallbackQuery, state: FSMContext):
    if call.data in ['Москва', 'Санкт-Петербург', 'Юг России', 'Сибирь', 'Урал', 'Дальний Восток и Камчатка', 'Другой']:
        await state.update_data(city=call.data)
        await bot.send_message(call.from_user.id, "Выберете возраст который будем искать", reply_markup=age_markup)
        await state.set_state(FSMprofile.age_seach_s)
    else:
        await call.message.answer('Что то пошло не так', reply_markup=main_keyboard)
        await state.clear()


@router.callback_query(FSMprofile.age_seach_s)
async def ready_profile(call: types.CallbackQuery, state: FSMContext):
    """Функция записи нового пользователя в базу"""
    if int(call.data) in [20, 40]:
        try:
            int(call.data)
            await state.update_data(age_seach_s=call.data)
            data = await state.get_data()
            username = call.from_user.username
            await bot.send_message(call.from_user.id, 'что то пошло не так', reply_markup=age_markup)
            await state.set_state(FSMprofile.age_seach_s)
            dataage = int(call.data)
            ret = (add_user(username, call.from_user.id, data['name'], data['age'], data['sex'], data['photo'],
                            data['text_profile'], data['search_profile'], data['city'], 0, dataage))
            conn.commit()
            print(ret)
            if ret == 'Пользователь с таким user_name уже есть в базе':
                await bot.send_message(call.from_user.id, 'пользователь уже есть в базе')
            else:
                update_user_data(data['name'], data['age'], data['sex'], data['photo'], data['text_profile'],
                                 data['search_profile'], data['city'], data['age_seach_s'], username)
                conn.commit()
                print(ret)
            if int(data["age_seach_s"]) == 20:
                x = (f'Ваша анкета\n'
                     f'Имя: {data["name"]} {data["sex"]}\n'
                     f'Возраст: {data["age"]}\n'
                     f'О себе: {data["text_profile"]}\n'
                     f'Кого ищу: {data["search_profile"]}\n'
                     f'Предпочитаю возраст: 18-40')
                y = data['photo']
                await bot.send_photo(call.from_user.id, y, caption=x, reply_markup=search_begin_markup)
                admin_1 = (f'Новая анкета\n'
                         f'@{call.from_user.username}\n'
                         f'chat_id : {call.from_user.id}\n'
                         f'Имя: {data["name"]} {data["sex"]}\n'
                         f'Возраст: {data["age"]}\n'
                         f'О себе: {data["text_profile"]}\n'
                         f'Кого ищу: {data["search_profile"]}\n'
                         f'Где ищу: {data["city"]}\n'
                         f'Предпочитаю возраст: 18-40')
                await bot.send_photo(5923668994, photo=y, caption=admin_1)
                await bot.send_photo(7241936347, photo=y, caption=admin_1)
                await state.clear()
            else:
                if int(data["age_seach_s"]) == 40:
                    x = (f'Ваша анкета\n'
                         f'Имя: {data["name"]} {data["sex"]}\n'
                         f'Возраст: {data["age"]}\n'
                         f'О себе: {data["text_profile"]}\n'
                         f'Кого ищу: {data["search_profile"]}\n'
                         f'Предпочитаю возраст: 40+')
                    y = data['photo']
                    await bot.send_photo(call.from_user.id, y, caption=x, reply_markup=search_begin_markup)
                    admin_1 = (f'Новая анкета\n'
                             f'@{call.from_user.username}\n'
                             f'chat_id : {call.from_user.id}\n'
                         f'Имя: {data["name"]} {data["sex"]}\n'
                         f'Возраст: {data["age"]}\n'
                         f'О себе: {data["text_profile"]}\n'
                         f'Кого ищу: {data["search_profile"]}\n'
                         f'Где ищу: {data["city"]}\n'
                         f'Предпочитаю возраст: 40+')
                    await bot.send_photo(5923668994, photo=y, caption=admin_1)
                    await bot.send_photo(7241936347, photo=y, caption=admin_1)
                    await state.clear()
        except ValueError:
            await bot.send_message(call.from_user.id, "Выберете возраст который будем искать", reply_markup=age_markup)
            await state.set_state(FSMprofile.age_seach_s)
    else:
        await call.message.answer('Что то пошло не так', reply_markup=main_keyboard)
        await state.clear()


# @router.callback_query(F.data == 'hi')
# async def send_profile(call: types.CallbackQuery):
#     logo = FSInputFile(r'media/хатико.jpg')
#     await bot.send_photo(call.from_user.id, logo, caption='че то работает', reply_markup=profile_markup)


@router.callback_query(F.data == 'back')
async def cancel(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        current = await state.get_state()
        if current == 'FSMprofile:name':
            await state.clear()
            await bot.send_message(call.from_user.id, 'Кто вы?', reply_markup=start_profile_markup)
            await state.set_state(FSMprofile.sex)
        elif current == 'FSMprofile:photo':
            await state.update_data(name=None)
            await bot.send_message(call.from_user.id, "Напишите как вас зовут", reply_markup=next_back_kb_markup)
            await state.set_state(FSMprofile.name)
            print(await state.get_state())
        elif current == 'FSMprofile:text_profile':
            await state.update_data(photo=None)
            await bot.send_message(call.from_user.id, 'Выберете фото для вашей анкеты,'
                                                      'если не хотите отправлять свое фото, введите любое сообещние',
                                   reply_markup=next_back_kb_markup)
            await state.set_state(FSMprofile.photo)
        elif current == 'FSMprofile:age':
            await state.update_data(text_profile=None)
            await bot.send_message(call.from_user.id, 'Напишите немного о себе', reply_markup=next_back_kb_markup)
            await state.set_state(FSMprofile.text_profile)
        elif current == 'FSMprofile:search_profile':
            await state.update_data(age=None)
            await bot.send_message(call.from_user.id, 'Укажите ваш возраст', reply_markup=next_back_kb_markup)
            await state.set_state(FSMprofile.age)
        elif current == 'FSMprofile:city':
            await state.update_data(search_profile=None)
            await bot.send_message(call.from_user.id, 'Кого будем для вас искать?', reply_markup=start_profile_markup_1)
            await state.set_state(FSMprofile.search_profile)


# @router.message
# async def my_info(message: types.Message):
#     pprint(message.from_user.username)


@router.callback_query(F.data == 'go')
async def new_profile(call: types.callback_query):
    """Начало поиска """
    username = call.from_user.username
    result_search = search(username)
    gender = result_search[0]['gender']
    age = result_search[0]['preferences_age']
    pref = result_search[0]['preferences']
    count = result_search[0]['user_index']
    c_count = 0
    while True:
        count = result_search[0]['user_index'] + c_count
        result = search3(age, pref, gender)
        try:
            if result[count]['user_name'] in list_liked_users(username):
                c_count = c_count + 1
                continue
            elif result_search[count]['user_name'] == username:
                continue
        except Exception as e:
            get_log_errors(e)
            break
        else:
            break
    result = search3(age, pref, gender)
    # print(result)
    try:
        x = (f'Имя: {result[count]["nick_name"]} {result[count]["gender"]}\n'
        f'Возраст: {result[count]["age"]}\n'
        f'О себе: {result[count]["about_me"]}')
        try:
            await bot.send_photo(call.from_user.id, result[count]['photo'], caption=x,
                                 reply_markup=search_profile_markup)
        except Exception as e:
            get_log_errors(e)
            photos = "AgACAgIAAxkBAAIFe2UfsirjHLkRHmqocmNSZIphy4FfAAKXzjEb748BSeSusLw4RhVIAQADAgADeAADMAQ"
            await bot.send_photo(call.from_user.id, photos, caption=x, reply_markup=search_profile_markup)
    except IndexError:
        await bot.send_message(call.from_user.id, 'На сегодня анкеты закончились. Хотите пообщаться в нашем чате?',
                               reply_markup=again_markup)


@router.callback_query(F.data == 'like')
async def like_do(call: types.callback_query):
    us_name = call.from_user.username
    result_search = search(us_name)
    gender = result_search[0]['gender']
    age = result_search[0]['preferences_age']
    pref = result_search[0]['preferences']
    c_count = 0
    while True:
        count = result_search[0]['user_index'] + c_count
        result = search3(age, pref, gender)
        try:
            if result[count]['user_name'] in list_liked_users(us_name):
                c_count = c_count + 1
                continue
            else:
                break
        except Exception as e:
            print(f'тут отрабатывает падла \n {e}')
            get_log_errors(e)
            break
    try:
        liked(us_name, result[count]['user_name'])
        conn.commit()
        x = count + 1
        update_user_index(x, us_name)
        conn.commit()
        result_search = search(us_name)
        gender = result_search[0]['gender']
        age = result_search[0]['preferences_age']
        pref = result_search[0]['preferences']
        count = result_search[0]['user_index']

        result = search3(age, pref, gender)
        like_user_name = result[count - 1]['user_name']
        print(like_user_name)
        print(count)
        print(list_liked_users(like_user_name))
        if us_name in list_liked_users(like_user_name):
            x = my_anketa(us_name)
            y = (f'Есть взаимная симпатия 👉🏻 @{us_name} Начинай общаться!  \n'
                 f'Имя: {x[0]["nick_name"]}\n'
                 f'О себе: {x[0]["about_me"]}\n'
                 f'Возраст: {x[0]["age"]}')
            if len(result) > 1:
                print('>1')
                profile_like = (f'Есть взаимная симпатия 👉🏻 @{result[count - 1]["user_name"]} Начинай общаться!\n'
                                f'Имя: {result[count - 1]["nick_name"]} {result[count]["gender"]}\n'
                                f'Возраст: {result[count - 1]["age"]}\n'
                                f'О себе: {result[count - 1]["about_me"]}')

                await bot.send_photo(result[count - 1]['chat_id'], x[0]['photo'], caption=y, reply_markup=new_go)
                await bot.send_photo(call.from_user.id, photo=result[count - 1]["photo"], caption=profile_like,
                                     reply_markup=new_go)
            else:
                print('елсе')
                print(result)
                print(count)
                profile_like = (f'Есть взаимная симпатия 👉🏻 @{result[0]["user_name"]} Начинай общаться!\n'
                                f'Имя: {result[0]["nick_name"]} {result[0]["gender"]}\n'
                                f'Возраст: {result[0]["age"]}\n'
                                f'О себе: {result[0]["about_me"]}')

                await bot.send_photo(result[0]['chat_id'], x[0]['photo'], caption=y, reply_markup=new_go)
                await bot.send_photo(call.from_user.id, photo=result[0]["photo"], caption=profile_like,
                                     reply_markup=main_keyboard)
            # print(list_liked_users(like_user_name))
        else:
            newprofile1 = (f'Имя: {result[count]["nick_name"]}\n'
                           f'Пол: {result[count]["gender"]}\n'
                           f'Возраст: {result[count]["age"]}\n'
                           f'О себе: {result[count]["about_me"]}')
            await bot.send_photo(call.from_user.id, photo=result[count]['photo'], caption=newprofile1,
                                 reply_markup=search_profile_markup)
        # except TypeError:
        #     photos = "AgACAgIAAxkBAAIFe2UfsirjHLkRHmqocmNSZIphy4FfAAKXzjEb748BSeSusLw4RhVIAQADAgADeAADMAQ"
        #     await bot.send_photo(call.from_user.id, photos, caption=newprofile1, reply_markup=search_profile_markup)

    except IndexError as e:
        print(e)
        print('попал на индекс еррор')
        await bot.send_message(call.from_user.id, 'На сегодня анкеты закончились. Хотите пообщаться в нашем чате?',
                               reply_markup=again_markup)
    except TelegramForbiddenError:
        pass


@router.callback_query(F.data == 'dislike')
async def like_not(call: types.callback_query):
    us_name = call.from_user.username
    result_search = search(us_name)
    gender = result_search[0]['gender']
    age = result_search[0]['preferences_age']
    pref = result_search[0]['preferences']
    count = result_search[0]['user_index']
    result = search3(age, pref, gender)
    c_count = 0
    while True:
        count = result_search[0]['user_index'] + c_count
        result = search3(age, pref, gender)
        try:
            if result[count]['user_name'] in list_not_liked_users(us_name):
                c_count = c_count + 1
                continue
        except Exception as e:
            print(e)
            break
        else:
            break
    try:
        not_liked(us_name, result[count - 1]['user_name'])
        conn.commit()
        x = count + 1
        update_user_index(x, us_name)
        conn.commit()
        result_search = search(us_name)
        gender = result_search[0]['gender']
        age = result_search[0]['preferences_age']
        pref = result_search[0]['preferences']
        count = result_search[0]['user_index']
        result = search3(age, pref, gender)
        x = (f'Имя: {result[count]["nick_name"]} {result[count]["gender"]}\n'
             f'Возраст: {result[count]["age"]}\n'
             f'О себе: {result[count]["about_me"]}')
        try:
            await bot.send_photo(call.from_user.id, result[count]['photo'], caption=x,
                                 reply_markup=search_profile_markup)
        except TypeError:
            photos = "AgACAgIAAxkBAAIFe2UfsirjHLkRHmqocmNSZIphy4FfAAKXzjEb748BSeSusLw4RhVIAQADAgADeAADMAQ"
            await bot.send_photo(call.from_user.id, photos, caption=x, reply_markup=search_profile_markup)
    except IndexError:
        await bot.send_message(call.from_user.id, 'На сегодня анкеты закончились. Хотите пообщаться в нашме чате?',
                               reply_markup=again_markup)


@router.callback_query(F.data == 'go_again')
async def profile_again(call: types.callback_query):
    """начинает просмотр анкет заного"""
    update_index(call.from_user.username)

    await bot.send_message(call.from_user.id, 'Начнем поиск?', reply_markup=search_begin_markup)


@router.callback_query(F.data == 'cancell')
async def back(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.from_user.id, 'Начнем поиск?', reply_markup=search_begin_markup)
    await state.clear()
    print("Стадии очищены")


"""**********************Редактирование анкет по этапам***************************"""


@router.callback_query(F.data == 'edit_1_profile')
async def edit_pro_1(call: types.callback_query):
    await bot.send_message(call.from_user.id, 'Что вы хотите поменять?', reply_markup=edit_pro_markup)


"""ИМЯ"""


class Fsmeditname(StatesGroup):
    fname = State()


@router.callback_query(F.data == 'edit_name')
async def edit_name(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.from_user.id, 'Введите новое имя', reply_markup=edit_pro_cancel_markup)
    await state.set_state(Fsmeditname.fname)


@router.message(Fsmeditname.fname)
async def try_name(message: types.Message, state: FSMContext):
    if message.text is not None and len(message.text) < 25 and message.text not in STOP_WORDS:
        print(message.text)
        await state.update_data(fname=message.text)
        data = await state.get_data()
        us_name = message.from_user.username
        update_nick_name(data['fname'], us_name)
        conn.commit()
        await state.clear()
        await bot.send_message(message.chat.id, 'Имя изменено', reply_markup=edit_pro_markup)
    else:
        await state.clear()
        await bot.send_message(message.chat.id, "Введите имя буквами и цифрами до 25 символов",
                               reply_markup=edit_pro_markup)


class Fsmeditage(StatesGroup):
    editage = State()


@router.callback_query(F.data == 'edit_age')
async def edit_age(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.from_user.id, 'Введите другой возраст', reply_markup=edit_pro_cancel_markup)
    await state.set_state(Fsmeditage.editage)


@router.message(Fsmeditage.editage)
async def try_age(message: types.Message, state: FSMContext):
    try:
        if message.text == int or int(message.text) > 18 and int(message.text) < 100:
            await state.update_data(editage=message.text)
            data = await state.get_data()
            us_name = message.from_user.username
            update_age(data['editage'], us_name)
            conn.commit()
            await state.clear()
            await bot.send_message(message.chat.id, 'Возраст изменен', reply_markup=edit_pro_markup)
        else:
            await bot.send_message(message.chat.id, "Возраст можно ввести до 100 лет")
            await state.set_state(Fsmeditage.editage)
    except Exception as e:
        get_log_errors(e)
        await bot.send_message(message.chat.id, "Возраст можно ввести от 18 до 100 лет")
        await state.set_state(Fsmeditage.editage)


class Fsmeditgender(StatesGroup):
    editgender = State()


@router.callback_query(F.data == 'edit_gender')
async def edit_gender(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.from_user.id, 'Выберете ваш пол', reply_markup=start_profile_markup)
    await state.set_state(Fsmeditgender.editgender)


@router.callback_query(Fsmeditgender.editgender)
async def try_gender(call: types.Message, state: FSMContext):
    await state.update_data(editgender=call.data)
    data = await state.get_data()
    us_name = call.from_user.username
    update_gender(data['editgender'], us_name)
    conn.commit()
    await state.clear()
    await bot.send_message(call.from_user.id, 'Вы изменили пол в анкете', reply_markup=edit_pro_markup)


class Fsmphoto(StatesGroup):
    editphoto = State()


@router.callback_query(F.data == 'edit_photo')
async def edit_photo(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, 'Отправте новое фото', reply_markup=edit_pro_cancel_markup)
    await state.set_state(Fsmphoto.editphoto)


@router.message(Fsmphoto.editphoto)
async def try_photo(message: types.Message, state: FSMContext):
    user = message.from_user.username
    try:
        photos = message.photo[-1].file_id
        await state.update_data(editphoto=photos)
        print(photos)
        data = await state.get_data()
        update_photo(data['editphoto'], user)
        conn.commit()
        await bot.send_message(message.chat.id, "Фото анкеты изменено", reply_markup=edit_pro_markup)
        await state.clear()
    except TypeError:
        await bot.send_message(message.chat.id, "Анкета будет без фотографии, потом сможете это изменить",
                               reply_markup=edit_pro_markup)
        photos = "AgACAgIAAxkBAAMkZSjzLcAlLnNyUjUHpZGt_PAsJK4AAu3RMRsyykhJqXzKkCaEr7ABAAMCAAN4AAMwBA"
        await state.update_data(editphoto=photos)
        data = await state.get_data()
        update_photo(data['editphoto'], user)
        conn.commit()
        await state.clear()


class Fsmabout(StatesGroup):
    editabout = State()


@router.callback_query(F.data == 'edit_about')
async def edit_about(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.from_user.id, 'Напишите о вас', reply_markup=edit_pro_cancel_markup)
    await state.set_state(Fsmabout.editabout)


@router.message(Fsmabout.editabout)
async def try_about(message: types.Message, state: FSMContext):
    if message.text is not None and len(message.text) < 1024 and message.text not in STOP_WORDS:
        await state.update_data(editabout=message.text)
        data = await state.get_data()
        us_name = message.from_user.username
        update_about_me(data['editabout'], us_name)
        conn.commit()
        await state.clear()
        await bot.send_message(message.chat.id, 'Описание профиля именено', reply_markup=edit_pro_markup)
    else:
        await state.set_state(Fsmabout.editabout)
        await bot.send_message(message.chat.id, "Заполните информацию о себе и о том что вы ищите (описание не может быть более 1024 символов)")


class Fsmperf(StatesGroup):
    editperf = State()


@router.callback_query(F.data == 'edit_perf')
async def edit_perf(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.from_user.id, 'выберете кого будем искать', reply_markup=start_profile_markup_1)
    await state.set_state(Fsmperf.editperf)


@router.callback_query(Fsmperf.editperf)
async def try_perf(call: types.Message, state: FSMContext):
    if call.data == 'back':
        await state.clear()
        await bot.send_message(call.from_user.id, "Изменения отменены", reply_markup=edit_pro_markup)
    else:
        await state.update_data(editperf=call.data)
        data = await state.get_data()
        us_name = call.from_user.username
        update_preferences(data['editperf'], us_name)
        conn.commit()
        await state.clear()
        await bot.send_message(call.from_user.id, 'Вы изменили предпочтения по поиску', reply_markup=edit_pro_markup)


class Fsmcity(StatesGroup):
    editcity = State()


@router.callback_query(F.data == 'edit_city')
async def edit_city(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, 'Выберете ваш город', reply_markup=city_markup)
    await state.set_state(Fsmcity.editcity)


@router.callback_query(Fsmcity.editcity)
async def try_city(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(editcity=call.data)
    us_name = call.from_user.username
    data = await state.get_data()
    update_city(data['editcity'], us_name)
    await bot.send_message(call.from_user.id, 'Ваш город изменен', reply_markup=edit_pro_markup)
    await state.clear()


@router.message(F.text == 'Помощь')
async def help1(message: types.Message):
    x = (f'Воспользуйтесь следующими командами если произошла ошибка:\n'
         f'/start - обновление бота\n'
         f'/my_profile - для редактирования анкеты\n'
         f'Если не можете справиться сами, напишите нам сюда: @Supdesire_bot')
    await bot.send_message(message.chat.id, x)


@router.message(F.text == 'Перейти в наш чат')
async def my_chat(message: types.Message):
    x = """Для перехода в наш чат, воспользуйтесь ссылкой ниже:
    https://t.me/+fJvilb1aY1NiMjRi
    """
    await bot.send_message(message.chat.id, x)


class FSMage(StatesGroup):
    agestep_1 = State()
    agestep_2 = State()


@router.callback_query(F.data == 'pref_age')
async def edit_pref_age(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "Выберете возраст поиска", reply_markup=age_markup)
    await state.set_state(FSMage.agestep_1)


@router.callback_query(FSMage.agestep_1)
async def try_pref_age(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'cancell':
        await bot.send_message(call.from_user.id, 'Что хотите поменять?', reply_markup=edit_pro_markup)
        await state.clear()
    else:
        await state.update_data(agestep_1=call.data)
        data = await state.get_data()
        try:
            int(data['agestep_1'])
        except ValueError:
            await bot.send_message(call.from_user.id, 'что то пошло не так', reply_markup=edit_pro_markup)
            await state.clear()
        update_preferences_age(int(data['agestep_1']), call.from_user.username)
        await bot.send_message(call.from_user.id, "Вы изменили предпочитаемый возраст", reply_markup=edit_pro_markup)
        await state.clear()


class Fsm1(StatesGroup):
    message_all = State()
    image_al = State()
    resl = State()
    ready = State()


@router.message(Command('admin'))
async def admin(message: types.Message):
    await message.answer('Введите пароль:', )


@router.message(F.text == '124ffsf')
async def ad_key(message: types.Message, state: FSMContext):
    if message.text == '124ffsf':
        await message.answer('Выберете действие', reply_markup=admin_markup)


@router.callback_query(F.data == 'send_all')
async def mess_all(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, 'Отправьте текст рассылки')
    await state.set_state(Fsm1.message_all)


@router.message(Fsm1.message_all)
async def image_all(message: types.Message, state: FSMContext):
    await state.update_data(message_all=message.text)
    await bot.send_message(message.chat.id, 'Добавьте картинку для рассылки')
    await state.set_state(Fsm1.image_al)


@router.message(Fsm1.image_al)
async def res(message: types.Message, state: FSMContext):
    photos = message.photo[-1].file_id
    await state.update_data(image_al=photos)
    data = await state.get_data()
    await bot.send_photo(message.chat.id, photo=data['image_al'], caption=data['message_all'])
    await bot.send_message(message.chat.id, 'Проверяйте правильность сообщения и нажмите отправить',
                           reply_markup=admin_1_markup)
    await state.set_state(Fsm1.resl)


@router.callback_query(Fsm1.resl)
async def sends_all(call: types.CallbackQuery, state: FSMContext):
    lim = 0
    if call.data == 'send':
        data = await state.get_data()
        x = 0
        for user_ids in list_id():
            try:
                if lim >= 10:
                    await bot.send_photo(user_ids, photo=data['image_al'], caption=data['message_all'])
                    lim = lim + 1
                else:
                    lim = 0
                    await asyncio.sleep(2)
            except Exception as e:
                x = x + 1
        await call.message.answer(f'Не отправлено {str(x)} Пользователям')
        await state.clear()
    elif call.data == 'cancel':
        await bot.send_message(call.from_user.id, 'Возврат в главное меню', reply_markup=search_profile_markup)
        await state.clear()


@router.message(Command('rt'))
async def get_rt_report(mess: Message, state: FSMContext):
    await state.clear()
    if mess.from_user.id in [5923668994, 634112358]:
        report()
        file = FSInputFile('report.xlsx')
        await mess.answer_document(file, caption='Анкеты скачаны')
    else:
        await mess.answer('У вас не хватает прав скачать отчет.')




class Fsmoder(StatesGroup):
    usern = State()
    mess_user = State()
    user_block = State()




@router.message(Command("d"))
async def administrator(mess: Message, state: FSMContext):
    if mess.from_user.id in ADMIN_LIST:
        await state.clear()
        await mess.answer('Введите Юзернейм', reply_markup=cancel_markup)
        await state.set_state(Fsmoder.usern)
    else:
        await mess.answer('Вы не являетесь администратором')


@router.message(Fsmoder.usern)
async def admin_next(mess: Message, state: FSMContext):
    await state.update_data(usern=mess.text)
    await mess.answer('Введите сообщение пользователю',reply_markup=cancel_markup)
    await state.set_state(Fsmoder.mess_user)


@router.message(Fsmoder.mess_user)
async def admin_text(mess: Message, state: FSMContext):
    await state.update_data(mess_user=mess.text)
    await mess.answer('Нажмите отправить для блокировки или отмена', reply_markup=key_markup)
    await state.set_state(Fsmoder.user_block)


@router.callback_query(Fsmoder.user_block)
async def admin_block(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_block = data['usern']
    chat_id_bun = db_chat_id_user(user_block.replace('@', ''))
    if chat_id_bun is not None:
        await call.message.answer('Анкета гостя очищена!\n'
                                  ' Команды администратора:\n'
                                  ' /d - удалить анкету\n'
                                  ' /b - заблокировать пользователя\n'
                                  ' /u - разблокировать пользователя\n'
                                  ' /rt - скачать отчет')
        text_admin = ('Сожалеем, но ваша анкета удалена администрацией бота, так как не соответсвует [правилам комьюнити](https://t.me/vip_desire_club/82)\n'
                      'Наш бот поддержки: @vip\_desire\_bot\n'
                      'Комментарий администрации:\n')
        delete_user(user_block.replace('@', ''))
        conn.commit()
        try:
            await bot.send_message(int(chat_id_bun), f"{text_admin}"
                                                     f"{data['mess_user']}\n /start что бы начать заново", reply_markup=main_keyboard, parse_mode='Markdown')
        except TelegramForbiddenError:
            pass
    else:
        await call.message.answer('Пользователь с таким юзернейм уже очищен')
    await state.clear()



class Fsmbun(StatesGroup):
    usern = State()
    mess_user = State()
    user_block = State()

@router.message(Command("b"))
async def administrator(mess: Message, state: FSMContext):
    if mess.from_user.id in ADMIN_LIST:
        await state.clear()
        await mess.answer('Введите Юзернейм', reply_markup=cancel_markup)
        await state.set_state(Fsmbun.usern)
    else:
        await mess.answer('Вы не являетесь администратором')


@router.message(Fsmbun.usern)
async def admin_next(mess: Message, state: FSMContext):
    await state.update_data(usern=mess.text)
    await mess.answer('Введите сообщение пользователю',reply_markup=cancel_markup)
    await state.set_state(Fsmbun.mess_user)


@router.message(Fsmbun.mess_user)
async def admin_text(mess: Message, state: FSMContext):
    await state.update_data(mess_user=mess.text)
    await mess.answer('Нажмите отправить для блокировки или отмена', reply_markup=key_markup)
    await state.set_state(Fsmbun.user_block)


@router.callback_query(Fsmbun.user_block)
async def admin_block(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_block = data['usern']
    chat_id_bun = db_chat_id_user(user_block.replace('@', ''))
    print(user_block)
    await call.message.answer('Пользователь заблокирован!\n'
                              ' Команды администратора:\n'
                              ' /d - удалить анкету\n'
                              ' /b - заблокировать пользователя\n'
                              ' /u - разблокировать пользователя\n'
                              ' /rt - скачать отчет')

    text_admin = ('Сожалеем, но вы заблокированы за [нарушение правил](https://t.me/vip_desire_club/82)\n'
                  'Наш бот поддержки: @vip\_desire\_bot\n'
                  'Комментарий администрации:\n')
    try:
        await bot.send_message(int(chat_id_bun), f"{text_admin}\n"
                                                 f"Причина блокировки:\n"
                                                 f"\n{data['mess_user']}", reply_markup=main_keyboard, parse_mode='Markdown')
    except TelegramForbiddenError:
        pass
    db_bun(user_block.replace('@', ''))
    conn.commit()
    await state.clear()


class FsmUnBun(StatesGroup):
    usern = State()
    mess_user = State()
    user_block = State()

@router.message(Command("u"))
async def administrator(mess: Message, state: FSMContext):
    if mess.from_user.id in ADMIN_LIST:
        await state.clear()
        await mess.answer('Введите Юзернейм', reply_markup=cancel_markup)
        await state.set_state(FsmUnBun.usern)
    else:
        await mess.answer('Вы не являетесь администратором')


@router.message(FsmUnBun.usern)
async def admin_next(mess: Message, state: FSMContext):
    await state.update_data(usern=mess.text)
    await mess.answer('Введите сообщение пользователю',reply_markup=cancel_markup)
    await state.set_state(FsmUnBun.mess_user)


@router.message(FsmUnBun.mess_user)
async def admin_text(mess: Message, state: FSMContext):
    await state.update_data(mess_user=mess.text)
    await mess.answer('Нажмите отправить для блокировки или отмена', reply_markup=key_markup)
    await state.set_state(FsmUnBun.user_block)


@router.callback_query(FsmUnBun.user_block)
async def admin_block(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_block = data['usern']
    chat_id_bun = db_chat_id_user(user_block.replace('@', ''))
    print(user_block)
    await call.message.answer('Пользователь разаблокирован!\n'
                              ' Команды администратора:\n'
                              ' /d - удалить анкету\n'
                              ' /b - заблокировать пользователя\n'
                              ' /u - разблокировать пользователя\n'
                              ' /rt - скачать отчет')
    try:
        await bot.send_message(int(chat_id_bun), f"Администрацией бота сняты ограничения для вашего аккаунта, вы снова можете пользоваться ботом", reply_markup=main_keyboard)
    except TelegramForbiddenError:
        pass
    db_rebun(user_block.replace('@', ''))
    conn.commit()
    await state.clear()
    await state.clear()
