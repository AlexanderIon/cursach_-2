import sqlalchemy


""" Создана база  vk_bot c таблицами  List_users и Found_users
   create table if not exists List_users(count_ serial primary key, id_user varchar (80) not null) 
   create table if not exists Found_users(id_serial integer not null references List_users (count_),found_ids varchar(256)_not null )"""


def get_connection(any_engine):
    try:
        connect = any_engine.connect()
    except Exception:

        connect = None
    return connect


"""Функция принимает на в ход номер ID пользователя, проверяет ID по базе данных если он есть возвращает его SERIAl.
   Если пользователь новый то записывает его ID в db и  возвращает его SERIAl"""
def get_serial_id_user(id_: str,connect):
    result = connect.execute(f"""SELECT id_user FROM list_users
                                     WHERE id_user = '{id_}' """).fetchone()
    if result is None:
        connect.execute(f"""INSERT INTO list_users(id_user)
                               VALUES({id_});  """)
        result = connect.execute(f"""SELECT count_ FROM list_users
                                     WHERE id_user = '{id_}' ;""").fetchone()
    #
    else:
        result = connect.execute(f"""SELECT count_ FROM list_users
                                        WHERE id_user ='{id_}'""").fetchone()

    return result[0]


"""get_set_db_ids это функция принимает serial из таблицы list_users
   и  возвращает set всех id ,которые были найдены для USERA  """
def get_set_db_ids(serial_user,connect):
    set_common = set()
    show_history_id_user = connect.execute(f"""SELECT found_ids FROM found_users
                                                  WHERE id_serial = {serial_user}""").fetchall()
    for ids in show_history_id_user:
        str_ids = ids[0]
        list_ids = str_ids.split()
        set_common = set_common | set(list_ids)
    return set_common


"""get_new_id на вход принимает set из функции get_set_db и список найденных ID и определяет старые и новые ID
    на возврашает список новых ID """
def get_new_id(set_db,list_ids):
    set_found = set(list_ids)
    set_new_found = ((set_db ^ set_found) - set_db)
    if set_new_found == set():
        result = None
    else:
        result = list(set_new_found)
    return result


"""fill_out на вход принимает serial_id_user и список новых найденных id и заносит их в таблицу found_users"""
def fill_out_found_users(serial_: int, list_ids: list,connect):
    str_ids = " ".join(list_ids)
    connect.execute(f"""INSERT INTO found_users (id_serial,found_ids)
                           VALUES({serial_},'{str_ids}')""")



user_db = ""
password_db = ''
name_db = ''
engine = sqlalchemy.create_engine(f'postgresql://{user_db}:{password_db}@localhost:5432/{name_db}')

if __name__ == "__main__":
    connection = get_connection(engine)
    print(connection)

    """Получаем историю запросвов """

    print("ТАБЛИЦА found_users")
    print(connection.execute("""SELECT * FROM found_users""").fetchall())

    print("ТАБЛИЦА List_users")
    print(connection.execute("""SELECT * FROM list_users""").fetchall())

    # print("++++++++++")
    #
    # serial_id_user = get_serial_id_user('34375364', connection)
    # print(f"ID user serial {serial_id_user}")
    # set_user_db = get_set_db_ids(serial_id_user, connection)
    # print(set_user_db)
    # list_ = ['21664247', '18864042', '20414634', '7070519', '251970407']
    # list_new_ids = get_new_id(set_user_db, list_)
    # print(list_new_ids)
    # #
    # #
    # if list_new_ids is None:
    #     print("НОВЫХ ID нет")
    #
    #
    # else:
    #     print(f"Новые ID {list_new_ids}")
    #     fill_out_found_users(serial_id_user, list_new_ids)
    #
    # print("ТАБЛИЦА found_users")
    # print(connection.execute("""SELECT * FROM found_users""").fetchall())
    #
    # print("ТАБЛИЦА List_users")
    # print(connection.execute("""SELECT * FROM list_users""").fetchall())
    #
    # print("++++++++++")
    #

    # connection.execute("""DELETE FROM found_users""")
    # fill_out_found_users(serial_id_user, list_)
    # set_ = get_set_found_ids()
    #
    # list_1 = ['35', '36', '31', '34']
    # set_common = set_ ^ set(list_1)
    # set_different = set_common - set_
    # if set_common is not set():
    #     set_ = set_ | set_common
    #
    #     print(list(set_))
    #
    # print(list(set_different))
    #
    # set_db = {1,2,3,4,12}
    # set_found = {2,12}
    # set_new_found = ((set_db^set_found)-set_db)
    # print(set_new_found)
    # set_db = set_db|set_new_found
    # print(set_db)
    # list_for_set = []
    # set_common = set()
    # for ids in show_history_id_user:
    #     str_ = ids[0]
    #     str_ = str_.split()
    #     print(set(str_))
    #     if (set_common & set(str_)) == set():
    #         set_common = set_common | set(str_)
    #
    # print(set_common)
        # list_for_set.append(str_)

    # set_1 = set(list_for_set[0])
    # set_2 = set(list_for_set[5])
    # set_3 = set(list_for_set[4])
    #
    # print(set_1,set_2)
    # print(f"чем отличаются {set_1 ^ set_2}")
    # if set_1 ^ set_2 == set():
    #     print("Множество одинакково")
    # else :
    #     print("ОТЛИЧАЮТСЯ ")
    # print(f"чем похожи {set_1 & set_2}")
    # print(f"обьединяет.(удаляет повторы) {set_1 | set_2}")