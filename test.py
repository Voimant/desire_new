
str_num = 'sity'


if type(str_num) == int:
    print("Да это цифра")
elif type(int(str_num)) == int:
    print("работает перевод буквоцифры")
else:
    print('вообще не цифры')
