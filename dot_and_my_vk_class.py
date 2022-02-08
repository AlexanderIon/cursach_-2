import vk_api
from vk_api.longpoll import VkLongPoll
from random import randrange

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


class Vk_group():

    def __init__(self, token_group, ver_api):
        self.my_token = token_group
        self.ver_api = ver_api
        self.vk_ = vk_api.VkApi(token=self.my_token, api_version=self.ver_api)
        self.longpoll = VkLongPoll(self.vk_)

    def write_msg(self, user_id, message, attachment= None):
        self.vk_.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), 'attachment': attachment})


class Param_search:
    def __init__(self, age=None, gander=None, status=None, city=None):
        self.age = age
        self.gander = gander
        self.status = status
        self.city = city


class My_VK:
    def __init__(self, my_token, ver):
        self.token = my_token
        self.ver = ver
        self.api_vk = vk_api.VkApi(token=self.token,api_version=self.ver)

    def id_city(self,name_city: str):
        result = self.api_vk.method(method="database.getCities", values={"country_id": 1,
                                                               "q": name_city})
        return result['items'][0]['id']

    def search_users(self, q="", offset=0, count=5, sex=0, status=0, age_from=0, age_to=0, cityId=0):
        """search_users функция ищет пользователей по параметрам поиска. На выходе функции два занчения:
               1- количество совпадений
               2- список list_id"""
        result = self.api_vk.method(method='users.search', values={'q': q,
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

    def get_info_user(self, user_id, str_param="bdate,photo_id" ):
        result = self.api_vk.method(method='users.get', values={'user_ids': user_id, 'fields': str_param})

        return result[0]

    def get_id_photo(self,param_photo, count_photo=3):
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

    def get_user_photo(self, id_):
        result = self.api_vk.method(method='photos.get', values={'owner_id': id_,
                                                           'album_id': 'profile',
                                                           'rev': 0,
                                                           'extended': 1})

        return result

    def send_resutl(self, list_id):
        """функция принимает на в ход скисок ID и проверяет свойство ['is_closed'].
          Если профиль ОТРЫТ функция вернет список(длиной 3) из кортежей (id_, f'{name} {surname} {status} {url}', _id_photo)
          Если профиль ЗАКРЫТ функция вернет список(длиной 2) из коржежей (id_, f'{name} {surname} {status} {url}') """
        list_=[]
        for id_ in list_id:
            url = url = f"https://vk.com/id{id_}"
            name = self.get_info_user(id_)['first_name']
            surname =self.get_info_user(id_)['last_name']
            status = ""

            if self.get_info_user(id_)['is_closed'] is True:
                status = "профиль ЗАКРЫТ"
                result = (id_, f'{name} {surname} {status} {url}')
                list_.append(result)

            else:
                params_photo = self.get_user_photo(id_)
                likes_id_photo = self.get_id_photo(params_photo)
                _id_photo = []
                [_id_photo.append(i[1]) for i in likes_id_photo]
                result = (id_, f'{name} {surname} {status} {url}', _id_photo)
                list_.append(result)

        return list_


