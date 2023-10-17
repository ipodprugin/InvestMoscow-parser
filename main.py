import asyncio
import pygsheets
import pandas as pd

from datetime import datetime

from config import settings
from src import handlers
from src.pandas_helpers import merge_data_to_sheet
from models.tender_models import Tender
from models.tenders_list_models import BaseTender
from src.upload_images import upload_images

import json


sheet_headers = [
    'tender_id',
    'Адрес',
    'Округ',
    'Район',
    'Форма',
    'Начальная цена',
    'Задаток',
    'Проведены',
    'Дата окончания приема заявок',
    'Колличество',
    'Этаж',
    'Тип парковки',
    'Ссылка на investmoscow',
    'Место',
    'площадь'
]


def parse_objects_tenders(objects, parsed_objects, objects_photos, objtype):
    for object_ in objects['entities']:
        count = object_['count']
        tenders = object_['tenders']

        tender_index = 0
        if count > 1:
            tender_index = handlers.find_smallest_area_tender(tenders)

        tender = BaseTender.model_validate(tenders[tender_index])

        tender_data = handlers.get_tender(tender_id=tender.id)
        with open('details.json', 'w', encoding='utf-8') as f:
            json.dump(tender_data, f, ensure_ascii=False, indent=4)
        tender_details = Tender.model_validate(tender_data)

        deposit = list(filter(lambda x: x.label == 'Размер задатка', tender_details.procedure_info))
        form = list(filter(lambda x: x.label == 'Форма проведения', tender_details.procedure_info))
        floor = list(filter(lambda x: x.label == 'Этаж', tender_details.object_info))
        if objtype == settings.PARK_OBJTYPE_ID:
            parking_type = list(filter(lambda x: x.label == 'Тип парковки', tender_details.object_info))
            parking_type = parking_type[0].value if parking_type else None

            parking_place = list(filter(lambda x: x.label == 'Расположение', tender_details.object_info))
            parking_place = settings.GET_PARKPLACE_REGEX.findall(parking_place[0].value)
            parking_place = parking_place[0][-1] if parking_place else None
        else:
            entrance_type = list(filter(lambda x: x.label == 'Тип входа', tender_details.object_info))
            entrance_type = entrance_type[0].value if entrance_type else None

        if deposit[0].value:
            deposit = deposit[0].value.replace('\xa0', '')
            deposit = settings.GET_PRICE_REGEX.findall(deposit)
            if deposit:
                deposit = float(deposit[0].replace(" ", "").replace(",", "."))
            else:
                deposit = 0
        else:
            deposit = 0
        form = form[0].value if form else None
        floor = floor[0].value if floor else None
        end_date = datetime.strptime(tender.request_end_date, settings.DATETIME_FORMAT)

        sheet_row = {}
        sheet_row['tender_id'] = tender.id
        sheet_row['Адрес'] = tender_details.header_info.address
        sheet_row['Округ'] = tender.region_name
        sheet_row['Район'] = tender.district_name
        sheet_row['Форма'] = form
        sheet_row['Начальная цена'] = tender.start_price if tender.start_price else deposit * 2
        sheet_row['Задаток'] = deposit
        sheet_row['Проведены'] = 'да' if datetime.now() >= end_date else 'нет'
        sheet_row['Дата окончания приема заявок'] = end_date.strftime('%d.%m.%Y')
        sheet_row['Этаж'] = floor
        if objtype == settings.PARK_OBJTYPE_ID:
            sheet_row['Колличество'] = count
            sheet_row['Тип парковки'] = parking_type
            sheet_row['Место'] = parking_place
        else:
            sheet_row['Вход'] = entrance_type
            sheet_row['Рыночная'] = deposit * 10
            sheet_row['Цена за кв м'] = sheet_row['Рыночная'] / tender.object_area
        sheet_row['Ссылка на investmoscow'] = settings.BASEURL + tender.url
        sheet_row['Площадь'] = tender.object_area
        parsed_objects.append(sheet_row)
        # objects_photos[tender.id] = tender_details.image_info.attached_images
        images = tender_details.image_info.model_dump()
        images['tender_id'] = tender.id
        objects_photos.append(images)
        print(sheet_row)


def parse_tenders(objtype):
    objects = handlers.get_tenders(settings.PAGENUMBER, settings.PAGESIZE, objtype)
    # with open('objects.json', 'r', encoding='utf-8') as f:
        # objects = json.loads(f.read())
    with open('objects.json', 'w', encoding='utf-8') as f:
        json.dump(objects, f, ensure_ascii=False, indent=4)
    total_count = objects['totalCount']

    total_pages_count = total_count // settings.PAGESIZE + (1 if total_count % settings.PAGESIZE else 0) 

    parsed_objects = []
    objects_photos = []
    parse_objects_tenders(objects, parsed_objects, objects_photos, objtype)
    for pagenum in range(settings.PAGENUMBER + 1, total_pages_count + 1):
        objects = handlers.get_tenders(pagenum, settings.PAGESIZE, objtype)
        with open('objects.json', 'a', encoding='utf-8') as f:
            json.dump(objects, f, ensure_ascii=False, indent=4)
        parse_objects_tenders(objects, parsed_objects, objects_photos, objtype)
    return parsed_objects, objects_photos


async def main(objtype):
    tenders, tenders_photos = parse_tenders(objtype)

    sa = pygsheets.authorize(service_file=settings.GSHEETS_CREDS_PATH)
    sh = sa.open_by_url(settings.GSHEETURL)
    worksheet = settings.PARKING_PLACES_WORKSHEET_NAME if objtype == settings.PARK_OBJTYPE_ID else settings.NONRESIDENTIAL_SPACES_WORKSHEET_NAME
    worksheet = sh.worksheet_by_title(worksheet)

    sheet = pd.DataFrame(worksheet.get_all_records())
    parsed = pd.DataFrame(tenders)
    newdf = merge_data_to_sheet(sheet, parsed, on='tender_id', columns_order=settings.PARKING_SHEET_COLUMNS if objtype == settings.PARK_OBJTYPE_ID else settings.NONRESIDENTIAL_SHEET_COLUMNS)

    with open('photos.json', 'w', encoding='utf-8') as f:
        json.dump({'images': tenders_photos}, f, ensure_ascii=False, indent=4)
    

    worksheet.set_dataframe(
        newdf.loc[:, :'Ссылка на investmoscow'], 
        start='A2', 
        nan='',
        copy_head=False,
        escape_formulae=True
    )
    if objtype == settings.PARK_OBJTYPE_ID:
        newdf = newdf.astype({'Колличество': 'int32'})
        worksheet.set_dataframe(
            newdf.loc[:, 'Место':],
            start='W2', 
            nan='',
            copy_head=False,
            escape_formulae=True
        )
    else: 
        worksheet.set_dataframe(
            newdf.loc[:, 'Цена за кв м':],
            start='P2', 
            nan='',
            copy_head=False,
            escape_formulae=True
        )

    if objtype == settings.PARK_OBJTYPE_ID:
        folder = 'parking_spaces'
    else:
        folder = 'nonresidential'

    await upload_images(folder)

if __name__ == '__main__':
    types = {'1': 'машиноместа', '2': 'нежилые помещения'}
    choosing = True
    while choosing:
        objtype = input('Выберите что парсить: 1 - машиноместа, 2 - нежилые помещения\nВведите число или нажмите Enter для выхода: ')
        if objtype in ['1', '2']:
            while True:
                confirm = input(f'Парсим {types[objtype]}? (y/n): ')
                if confirm == 'n':
                    break
                elif confirm == 'y':
                    if objtype == '1':
                        objtype = settings.PARK_OBJTYPE_ID
                    if objtype == '2':
                        objtype = settings.NONRESIDENTIAL_OBJTYPE_ID
                    choosing = False
                    break
        elif objtype == '':
            import sys
            print('Выход...')
            sys.exit()
    asyncio.run(main(objtype))

    # from images import collect_images_links_for_avito
    
    # sa = pygsheets.authorize(service_file=settings.GSHEETS_CREDS_PATH)
    # sh = sa.open_by_url(settings.GSHEETURL)
    # worksheet = settings.PARKING_PLACES_WORKSHEET_NAME if objtype == settings.PARK_OBJTYPE_ID else settings.NONRESIDENTIAL_SPACES_WORKSHEET_NAME
    # worksheet = sh.worksheet_by_title(worksheet)
    
    # if objtype == settings.PARK_OBJTYPE_ID:
    #     folder = 'parking_spaces'
    # else:
    #     folder = 'nonresidential'
    # collect_images_links_for_avito(worksheet=worksheet, foldername=folder)
