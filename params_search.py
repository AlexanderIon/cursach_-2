from random import randrange
import re
import vk_api
from patterns import pattern_hi, pattern_yes, pattern_age, pattern_gender_M, pattern_gender_W
from vk_api.longpoll import VkLongPoll, VkEventType
from search_in_vk import get_id_city, create_age, search_users, get_id_photo, get_into_user, get_user_photo


def write_msg(user_id, message,attachemt=None):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), 'attachment': attachemt})


token = " "

vk = vk_api.VkApi(token=token, api_version='5.131')
longpoll = VkLongPoll(vk)

flag_hi = False
flag_gender = False
flag_relation = False
flag_city = False
flag_age = False
age = None
relation = None
gender = None
city = None
count_res = 0
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            word_find_hi = re.match(pattern_hi, request)
            word_find_yes = re.match(pattern_yes, request)
            word_find_age = re.match(pattern_age, request)
            word_find_gander_M = re.match(pattern_gender_M, request)
            word_find_gander_W = re.match(pattern_gender_W, request)
            id_user = event.user_id
            info_user = get_into_user(id_user)

            if word_find_hi is not None:

                write_msg(id_user, f"Привет , {info_user['first_name']}.\nХотите найти новых знакомых?")

                flag_hi = True

            elif (word_find_yes is not None) and (flag_hi is True):
                write_msg(id_user, f"{info_user['first_name']}, укажите параметры поиска:\n Возраст ?  ")
                flag_age = True
                flag_hi = False

            elif (word_find_age is not None) and (flag_age is True):
                age = re.sub(pattern_age, r"\1\3-\4\6-\7\8", request)
                write_msg(id_user, "Вы ищите друга или подругу ?")
                age = create_age(age)
                flag_age = False

            elif ((word_find_gander_M is not None) or (word_find_gander_W is not None)) and gender is None:

                if word_find_gander_M is None:
                    gender = 1
                else:
                    gender = 2
                flag_gender = True
                write_msg(id_user, "Выбери:\n0-все равно\n1—не женат/не замужем\n2—есть друг/есть подруга\n4 — "
                                   "женат/замужем\n5 — всё сложно\n6 — в активном поиске")

            elif ((gender == 1) or (gender == 2)) and flag_gender is True:
                relation = request
                write_msg(id_user, "В каком городе будем искать ?")
                flag_city = True
                flag_gender = False

            elif flag_city is True:
                city = request
                city = get_id_city(city)
                write_msg(id_user,
                          f"Условия поиска:\nВозраст: от {age[0]} до {age[1]} , Пол {gender}\n Статус отнощений {relation}, город - {city} Начнем поиск?")
                print(f'Параметры поиска (age) {age}  (gender){gender} relation{relation} (city){city} Начинаем поиск???')
                flag_city = False

            elif (age is not None and city is not None and gender is not None) and (word_find_yes is not None):
                print("РЕЗУЛЬТАТ ПОИСКА")
                print(f"Смещение offset {count_res}")
                flag_city = False
                result = search_users(cityId=int(city), offset=count_res, age_from=age[0], age_to=age[1], sex=gender)
                count_users, list_id_search = result

                for id_ in list_id_search:
                    url = f"https://vk.com/id{id_}"
                    name = get_into_user(id_)['first_name']
                    surname = get_into_user(id_)['last_name']
                    status = ""
                    if get_into_user(id_)['is_closed'] is True:
                        status = "профиль ЗАКРЫТ"

                    write_msg(id_user, f'{name} {surname} {status} {url}')

                    if get_into_user(id_)['is_closed'] is not True:
                        params_photo = get_user_photo(id_)
                        likes_id_photo = get_id_photo(params_photo)
                        _id_photo = []
                        [_id_photo.append(i[1]) for i in likes_id_photo]
                        for id_image in _id_photo:
                            write_msg(id_user, "", attachemt=f"photo{id_}_{id_image}")
                    write_msg(id_user, "===============================")

                count_res += 20
                write_msg(id_user, "Продолжить поиск?")

            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, f"Не поняла Вас, {info_user['first_name']} ...")

