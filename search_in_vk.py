import vk_api
from vk_api import VkUpload

token_my = ""
vk_my = vk_api.VkApi(token=token_my, api_version='5.131')


def create_age(age_str: str) -> list:
    """create_age на вход принимает string ="-age1-age2" или "--age1-age2" и формирует list =[age1,age2],
       который потом идет в параметры поиска """
    list_age = age_str.split("-")
    list_age.sort()
    while "" in list_age:
        list_age.remove("")
    if len(list_age) == 1:
        list_age.append(list_age[0])
    return list_age


def get_id_city(name_city=''):
    """get_id_city на вход принимает название города в str и выдает id города для для передачи в параметры поиска.
       ID получаем только первого города  т.к. стоит [0]"""

    result = vk_my.method(method="database.getCities", values={"country_id": 1,
                                                               "q": name_city})
    return result['items'][0]['id']


def get_get_Regions(name_region="Московская"):
    result = vk_my.method(method='database.getRegions', values={'country_id': 1,
                                                                'q': name_region})
    return result


def search_users(q="", offset=0, count=5, sex=0, status=0, age_from=0, age_to=0, cityId=0):
    """search_users функция ищет пользователей по параметрам поиска. На выходе функции два занчения:
        1- количество совпадений
        2- список list_id"""
    result = vk_my.method(method='users.search', values={'q': q,
                                                         'offset': offset,
                                                         'count': count,

                                                         'sex': sex,
                                                         # 'country': 1,
                                                         'status': status,
                                                         'city': cityId,
                                                         'age_from': age_from,
                                                         'age_to': age_to})
    list_id = []
    [list_id.append(i['id']) for i in result['items']]
    return result['count'], list_id


def get_id_photo(param_photo, count_photo=3):
    """get_id_photo : на вход принимает словать из метода get_user_photo(id_user)
    потом достает из словаря данные по лайкам и номер id фото, сортирует его. В результате выдает список из COUNT_PHOTO фото
    (фото где больше всего лайков) result = [[count_likes,id_photo1],[count_likes,id_photo2],[count_likes,id_photo3]]"""
    photos = param_photo['items']
    list_photo = []
    # for dict_phot in photos:
    #     list_photo.append((dict_phot['likes']['count'], dict_phot['id']))
    [list_photo.append([i['likes']['count'], i['id']]) for i in photos]
    list_photo.sort()
    result = (list_photo[-count_photo:])
    return result


def get_into_user(user_id, str_param="bdate,photo_id"):
    result = vk_my.method(method='users.get', values={'user_ids': user_id, 'fields': str_param})
    # result = f"{responce['first_name']} {responce['last_name']}"
    return result[0]


def get_user_photo(id_):
    result = vk_my.method(method='photos.get', values={'owner_id': id_,
                                                       'album_id': 'profile',
                                                       'rev': 0,
                                                       'extended': 1})

    return result


if __name__ == "__main__":

    search = "Параметры поиска (age)20-30--  (gender)1 relation4 (city)"
    age = '30-40'
    gender = 1
    relation = 0
    city_ = 'ногинск'

    city_id = get_id_city(city_)
    age_for_search = create_age(age)

    w = 0
    while w < 200:
        search_count, search_ids = search_users(sex=gender, offset=w, status=relation, cityId=city_id,
                                                age_from=age_for_search[0], age_to=age_for_search[1])
        w += 20
        print(f"Колическво {search_count}")
        print(f"вывод {search_ids}")

    # for id_ in search_ids:
    #     url = f"https://vk.com/id{id_}"
    #     if get_into_user(id_)['is_closed'] is not True:
    #         params_photo = get_user_photo(id_)
    #         likes_id_photo = get_id_photo(params_photo)
    #         _id_photo = []
    #         [_id_photo.append(i[1]) for i in likes_id_photo]
    #         for id_image in _id_photo:
    #             print(f'photo{id_}_{id_image}')
    #     else:
    #         print(id_)

    # print(photos[2]['id'], photos[1]['likes']['count'])


