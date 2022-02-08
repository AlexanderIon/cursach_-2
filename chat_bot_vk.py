import re

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from patterns import pattern_hi, pattern_yes, pattern_age, pattern_gender_M, pattern_gender_W

from dot_and_my_vk_class import My_VK, Vk_group, Param_search, create_age

from db import engine, get_connection, get_serial_id_user, get_set_db_ids,get_new_id, fill_out_found_users


if __name__ == "__main__":
    my_token = ""
    token_group = ''
    ver_ = "5.131"
    bot = Vk_group(token_group, ver_)
    my_vk = My_VK(my_token, ver_)
    count_res = 0
    look_for = Param_search()

    for event in bot.longpoll.listen():
        if (event.type == VkEventType.MESSAGE_NEW) and event.to_me:
            id_user = event.user_id
            request = event.text

            if re.match(pattern_hi, request) is not None:
                bot.write_msg(id_user, f"Привет.{my_vk.get_info_user(id_user)['first_name']} Начнем поиски ? ")

            elif (re.match(pattern_yes, request) is not None) and look_for.age is None:
                bot.write_msg(id_user, "Укажите возраст")

            elif (look_for.age is None) and (re.match(pattern_age,request) is not None):
                look_for.age = create_age(request)
                bot.write_msg(id_user, "Вы ищите друга или подругу,?")
                print(f"Возраст:{look_for.age}")

            elif (look_for.gander is None) and (re.match(pattern_gender_M,request) is not None):
                look_for.gander = '2'
                bot.write_msg(id_user,"Укажите станус:\n0-все равно\n1—не женат/не замужем\n2—есть друг/есть подруга\n4 —женат/замужем\n5 — всё сложно\n6 — в активном поиске")
            elif (look_for.gander is None) and (re.match(pattern_gender_W,request) is not None):
                look_for.gander = '1'
                bot.write_msg(id_user,"Укажите станус:\n0-все равно\n1—не женат/не замужем\n2—есть друг/есть подруга\n4 —женат/замужем\n5 — всё сложно\n6 — в активном поиске")
            elif (look_for.gander is not None) and (look_for.status is None):
                look_for.status = request
                bot.write_msg(id_user,"Укажите город поиска:")
            elif (look_for.status is not None) and (look_for.city is None):
                look_for.city = my_vk.id_city(request)
                bot.write_msg(id_user, f"Параметры поиска: {look_for.age},{look_for.gander},{look_for.status},{look_for.city}\nНачать поиск?")
            elif ((look_for.age is not None) and (look_for.city is not None)) and re.match(pattern_yes, request):
                print("Результат поиска:")
                connection = get_connection(engine)

                if connection is not None:
                    id_user = str(id_user)
                    serial_id_user = get_serial_id_user(id_user, connection)
                    set_ids_db_for_user = get_set_db_ids(serial_id_user, connection)
                    result = my_vk.search_users(cityId=look_for.city, offset=count_res, status=look_for.status,
                                                age_from=look_for.age[0], age_to=look_for.age[1], sex=look_for.gander)
                    count_users, list_id_search = result
                    list_id_search = [str(element) for element in list_id_search]
                    list_id_search = get_new_id(set_ids_db_for_user, list_id_search)
                    w = 5

                    while list_id_search is None:
                        result = my_vk.search_users(cityId=look_for.city, offset=count_res, status=look_for.status,
                                                    age_from=look_for.age[0], age_to=look_for.age[1],
                                                    sex=look_for.gander)
                        count_users, list_id_search = result
                        list_id_search = [str(element) for element in list_id_search]
                        list_id_search = get_new_id(set_ids_db_for_user, list_id_search)
                        w += 5
                    fill_out_found_users(serial_id_user, list_id_search, connection)
                    send_res = my_vk.send_resutl(list_id_search)
                else:
                    result = my_vk.search_users(cityId=look_for.city,offset=count_res,status=look_for.status ,age_from=look_for.age[0], age_to=look_for.age[1], sex=look_for.gander)
                    count_users, list_id_search = result
                    print(count_users, list_id_search)
                    send_res = my_vk.send_resutl(list_id_search)
                    print(send_res)

                for user in send_res:
                    if len(user) == 3:
                        id_ = user[0]
                        bot.write_msg(id_user,f'{user[1]}')
                        for id_photo in  user[2]:

                            attach = f"{id_}_{id_photo}"
                            bot.write_msg(id_user, "", attachment=f"photo{id_}_{id_photo}")
                    else:
                        bot.write_msg(id_user, user[1])

                count_res += 5
                bot.write_msg(id_user, "Продолжить поиск?")


            else:
                bot.write_msg(id_user, "<<<Я Вас не понял>>>")



