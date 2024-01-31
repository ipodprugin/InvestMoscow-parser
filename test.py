from collections import defaultdict

import random

items = [
  {
    'address': 1,
    'square': 12.5,
  },
  {
    'address': 3,
    'square': 10.0,
  },
  {
    'address': 5,
    'square': 15.0,
  },
  {
    'address': 2,
    'square': 8.7,
  },
  {
    'address': 6,
    'square': 20.0,
  },
  {
    'address': 7,
    'square': 18.5,
  },
  {
    'address': 7,
    'square': 13.2,
  },
  {
    'address': 7,
    'square': 16.8,
  },
  {
    'address': 1,
    'square': 14.3,
  },
  {
    'address': 9,
    'square': 25.0,
  },
  {
    'address': 2,
    'square': 11.9,
  },
  {
    'address': 2,
    'square': 9.6,
  },
  {
    'address': 2,
    'square': 17.1,
  },
  {
    'address': 2,
    'square': 22.4,
  },
  {
    'address': 2,
    'square': 19.7,
  },
  {
    'address': 2,
    'square': 14.8,
  },
  {
    'address': 1,
    'square': 16.2,
  },
]

items = {
  14590: {'address': 1, 'square': 12.5},
  16392: {'address': 3, 'square': 10.0},
  84259: {'address': 5, 'square': 15.0},
  50734: {'address': 2, 'square': 8.7},
  81510: {'address': 6, 'square': 20.0},
  76344: {'address': 7, 'square': 18.5},
  27263: {'address': 7, 'square': 13.2},
  83746: {'address': 7, 'square': 16.8},
  19723: {'address': 1, 'square': 14.3},
  47862: {'address': 9, 'square': 25.0},
  51924: {'address': 2, 'square': 11.9},
  49385: {'address': 2, 'square': 9.6},
  31325: {'address': 2, 'square': 17.1},
  41277: {'address': 2, 'square': 22.4},
  98499: {'address': 2, 'square': 19.7},
  24491: {'address': 2, 'square': 14.8},
  15969: {'address': 1, 'square': 16.2}
}

# for item in items:
#     item['tender_id'] = random.randint(10000, 99999)
# print(items)

# cache = defaultdict(lambda: defaultdict(int))
# for item in items:
#     square = cache[item['address']]['square']
#     if square == 0:
#         square = item['square']
#         cache[item['address']]['tender_id'] = item['tender_id']
#     else:
#         if item['square'] < square:
#             square = item['square']
#             cache[item['address']]['tender_id'] = item['tender_id']
#     cache[item['address']]['square'] = square

# cache = defaultdict(lambda: defaultdict(int))
# for key in items:
#     address = items[key]['address']
#     square = cache[address]['square']
#     new_square = items[key]['square']
#     if square == 0 or new_square < square:
#         square = new_square
#         cache[address]['tender_id'] = key
#     cache[address]['square'] = square
# print(cache)

# for item in cache:
#     print(item, cache[item])

# {'tender_id': 19337217, 'Адрес': 'Волжский бульвар, дом 1, корпус 1, этаж 4 , м/м 513', 'Округ': 'ЮВАО', 'Район': 'Рязанский район', 'Форма': 'Открытый аукцион в электронной форме', 'Начальная цена': 290000.0, 'Задаток': 58000.0, 'Проведены': 'нет', 'Дата окончания приема заявок': '01.12.2023', 'Этаж': '4', 'Колличество': 772, 'Тип парковки': 'Многоуровневая парковка', 'Место': '513', 'Ссылка на investmoscow': 'https://investmoscow.ru/tenders/tender/19337217', 'Площадь': 11.9}


parsed_objects = {19337217: {'tender_id': 19337217, 'Адрес': 'Волжский бульвар, дом 1, корпус 1, этаж 4 , м/м 513', 'Округ': 'ЮВАО', 'Район': 'Рязанский район', 'Форма': 'Открытый аукцион в электронной форме', 'Начальная цена': 290000.0, 'Задаток': 58000.0, 'Проведены': 'нет', 'Дата окончания приема заявок': '01.12.2023', 'Этаж': '4', 'Колличество': 772, 'Тип парковки': 'Многоуровневая парковка', 'Место': '513', 'Ссылка на investmoscow': 'https://investmoscow.ru/tenders/tender/19337217', 'Площадь': 11.9}}
objects_photos = {19337217: {'attached_images': [{'tender_id': 19337217, 'is_main_photo': True, 'url': 'https://investmoscow.ru/objectimages/Tenders/19337217/b20233cc6b85d9aba24538fb02735f71.jpg', 'file_base': {'name': 'ГП16938529.Машино-место.Общий фасад здания.jpg'}}, {'tender_id': 19337217, 'is_main_photo': False, 'url': 'https://investmoscow.ru/objectimages/Tenders/19337217/1e35b7c3c6f4f0841d2159bcadc9b454.jpg', 'file_base': {'name': 'ГП16938529.Машино-место.Общий фасад здания_2.jpg'}}, {'tender_id': 19337217, 'is_main_photo': False, 'url': 'https://investmoscow.ru/objectimages/Tenders/19337217/349297503538a12fdb6d511dbbd3a88c.jpg', 'file_base': {'name': 'ГП16938529.Машино-место.Общий фасад здания_3.jpg'}}, {'tender_id': 19337217, 'is_main_photo': False, 'url': 'https://investmoscow.ru/objectimages/Tenders/19337217/94d0b90fc6bacbcd2676d45746a4535a.jpg', 'file_base': {'name': 'ГП16938529.Машино-место.Общий фасад здания_4.jpg'}}, {'tender_id': 19337217, 'is_main_photo': False, 'url': 'https://investmoscow.ru/objectimages/Tenders/19337217/c7ab7ae3d6f4a859a3a63a19d6d17e31.jpg', 'file_base': {'name': 'ГП16938529.Машино-место.Фасад здания с выделенными окнами реализуемого объекта.jpg'}}, {'tender_id': 19337217, 'is_main_photo': False, 'url': 'https://investmoscow.ru/objectimages/Tenders/19337217/f746a1ee07a30c0156bc55e4ec40a7fc.jpg', 'file_base': {'name': 'ГП16938529.Машино-место.Входная группа объекта.jpg'}}, {'tender_id': 19337217, 'is_main_photo': False, 'url': 'https://investmoscow.ru/objectimages/Tenders/19337217/2f7bbe7011711dec6d2a0fbe4bc2060f.jpg', 'file_base': {'name': 'ГП16938529.Машино-место.Входная группа объекта_2.jpg'}}, {'tender_id': 19337217, 'is_main_photo': False, 'url': 'https://investmoscow.ru/objectimages/Tenders/19337217/ada24459cc22671f4ea8517d2e29df04.jpg', 'file_base': {'name': 'ГП16938529.Машино-место.Входная группа объекта_3.jpg'}}, {'tender_id': 19337217, 'is_main_photo': False, 'url': 'https://investmoscow.ru/objectimages/Tenders/19337217/816b220b3df34f5bf50545f09ee98d00.png', 'file_base': {'name': 'ГП16938529.Машино-место.План этажа _поэтажный_ с указанием границ реализуемого объекта.png'}}, {'tender_id': 19337217, 'is_main_photo': False, 'url': 'https://investmoscow.ru/objectimages/Tenders/19337217/41031db69bb774b0747e23ad5b3a3e34.jpg', 'file_base': {'name': 'ГП16938529.Машино-место.Каждое помещение_комната, входящее в состав реализуемого объекта .jpg'}}], 'tender_id': 19337217}}

def filter_duplicates_by_adress(parsed_objects, objects_photos):
    tenders = []
    photos = []
    cache = defaultdict(lambda: defaultdict(int))
    for key in parsed_objects:
        address = parsed_objects[key]['Адрес']
        square = cache[address]['Площадь']
        new_square = parsed_objects[key]['Площадь']
        if square == 0 or new_square < square:
            square = new_square
            cache[address]['tender_id'] = key
        cache[address]['Площадь'] = square
    print(cache)
    for key in cache:
        tenders.append(parsed_objects[cache[key]['tender_id']])
        photos.append(objects_photos[cache[key]['tender_id']])
    print('------------------------')
    print(tenders)
    print(photos)

filter_duplicates_by_adress(parsed_objects, objects_photos)