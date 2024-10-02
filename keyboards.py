from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_button = [[
    KeyboardButton(text='Помощь'),
    KeyboardButton(text='Перейти в наш чат')]]
main_keyboard = ReplyKeyboardMarkup(keyboard=main_button, resize_keyboard=True)

profile_kb_1 = [[InlineKeyboardButton(text='тест колбека', callback_data='hi')]]
profile_markup = InlineKeyboardMarkup(inline_keyboard=profile_kb_1)

start_profile_button = [[
    InlineKeyboardButton(text='Мужчина 🙎‍♂', callback_data='🙎‍♂️️️'),
    InlineKeyboardButton(text='Девушка 🙍‍♀️', callback_data='🙍‍♀️'),
    InlineKeyboardButton(text='Пара 🙍‍♀️🙎‍♂️', callback_data='🙍‍♀️🙎‍♂️')
]]

start_profile_button_1 = [[
    InlineKeyboardButton(text='Мужчину 🙎‍♂', callback_data='🙎‍♂️️️'),
    InlineKeyboardButton(text='Девушку 🙍‍♀️', callback_data='🙍‍♀️'),
    InlineKeyboardButton(text='Пару 🙍‍♀️🙎‍♂️', callback_data='🙍‍♀️🙎‍♂️'),
    InlineKeyboardButton(text='Назад', callback_data='back')
]]
start_profile_markup_1 = InlineKeyboardMarkup(inline_keyboard=start_profile_button_1)

next_back_kb = [[
    InlineKeyboardButton(text='Назад', callback_data='back'),
]]

search_profile = [[
    InlineKeyboardButton(text="❤️", callback_data='like'),
    InlineKeyboardButton(text="👎", callback_data='dislike'),
]]

search_begin = [[
    InlineKeyboardButton(text="Начать поиск❤️", callback_data='go')
]]


search_go = [[
    InlineKeyboardButton(text="Продолжить поиск❤️", callback_data='go')
]]

new_go = InlineKeyboardMarkup(inline_keyboard=search_go)


city_button = [
    [InlineKeyboardButton(text='Москва', callback_data='Москва')],
    [InlineKeyboardButton(text='Санкт-Петербург', callback_data='Санкт-Петербург')],
    [InlineKeyboardButton(text='Юг России', callback_data='Юг России')],
    [InlineKeyboardButton(text='Сибирь', callback_data='Сибирь')],
    [InlineKeyboardButton(text='Урал', callback_data='Урал')],
    [InlineKeyboardButton(text='Дальний Восток и Камчатка', callback_data='Дальний Восток и Камчатка')],
    [InlineKeyboardButton(text='Другой', callback_data='Другой')]
]

no_new_profile = [[InlineKeyboardButton(text='Перейти в наш чат', url='https://t.me/+fJvilb1aY1NiMjRi'),
                   InlineKeyboardButton(text='Поcмотреть заново', callback_data='go_again')]]

admin_keyboards = [[InlineKeyboardButton(text='Рассылка', callback_data='send'),
                    InlineKeyboardButton(text='Отмена', callback_data='canc')]]

edit_profile_button = [
    [InlineKeyboardButton(text='Заполнить анкету заново', callback_data='edit_profile')],
    [InlineKeyboardButton(text='Частично поменять анкету', callback_data='edit_1_profile')]
]

edit_pro_button = [
    [InlineKeyboardButton(text='Изменить имя', callback_data="edit_name")],
    [InlineKeyboardButton(text='Изменить возраст', callback_data="edit_age")],
    [InlineKeyboardButton(text='Изменить пол', callback_data='edit_gender')],
    [InlineKeyboardButton(text='Изменить фото', callback_data='edit_photo')],
    [InlineKeyboardButton(text='Изменить информацию о себе', callback_data='edit_about')],
    [InlineKeyboardButton(text='Изменить кого ищу', callback_data='edit_perf')],
    [InlineKeyboardButton(text='Изменить город', callback_data='edit_city')],
    [InlineKeyboardButton(text='Изменить возраст поиска', callback_data='pref_age')],
    [InlineKeyboardButton(text='Назад', callback_data='cancell')]
]

admin_button = [[InlineKeyboardButton(text='Рассылка', callback_data='send_all')]]
admin_markup = InlineKeyboardMarkup(inline_keyboard=admin_button)

admin_1_button = [[
    InlineKeyboardButton(text='Отправить всем', callback_data='send'),
    InlineKeyboardButton(text='Отмена', callback_data='cancel')
]]
admin_1_markup = InlineKeyboardMarkup(inline_keyboard=admin_1_button)

age_button = [
    [InlineKeyboardButton(text='18-40', callback_data='20'),
     InlineKeyboardButton(text='40+', callback_data='40'), ]

]
age_markup = InlineKeyboardMarkup(inline_keyboard=age_button)
edit_pro_cancel = [[InlineKeyboardButton(text='Назад', callback_data='cancell')]]
edit_pro_cancel_markup = InlineKeyboardMarkup(inline_keyboard=edit_pro_cancel)
edit_pro_markup = InlineKeyboardMarkup(inline_keyboard=edit_pro_button)

edit_profile_markup = InlineKeyboardMarkup(inline_keyboard=edit_profile_button)

again_markup = InlineKeyboardMarkup(inline_keyboard=no_new_profile)
city_markup = InlineKeyboardMarkup(inline_keyboard=city_button)
next_back_kb_markup = InlineKeyboardMarkup(inline_keyboard=next_back_kb)
start_profile_markup = InlineKeyboardMarkup(inline_keyboard=start_profile_button)
search_profile_markup = InlineKeyboardMarkup(inline_keyboard=search_profile)
search_begin_markup = InlineKeyboardMarkup(inline_keyboard=search_begin)

cancel_button = [[InlineKeyboardButton(text="Отмена", callback_data='cancel')]]
cancel_markup = InlineKeyboardMarkup(inline_keyboard=cancel_button)

key_button = [
    [InlineKeyboardButton(text='Отправить', callback_data='bun_bun')],
    [InlineKeyboardButton(text="Отмена", callback_data='cancel')]
]

key_markup = InlineKeyboardMarkup(inline_keyboard=key_button)

new_start_button = [[InlineKeyboardButton(text='Ознакомиться с правилами', url='https://t.me/vip_desire_club/82')],
                    [InlineKeyboardButton(text='Начать регистрацию', callback_data='reg')]]

new_start_markup = InlineKeyboardMarkup(inline_keyboard=new_start_button)