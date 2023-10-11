import pygsheets
import pandas as pd

from datetime import datetime

from config import settings
from src import handlers
from src.pandas_helpers import merge_data_to_sheet
from models.tender_models import Tender
from models.tenders_list_models import BaseTender

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


def parse_objects_tenders(objects, parsed_objects, objects_photos):
    for object_ in objects['entities']:
        count = object_['count']
        tenders = object_['tenders']

        tender_index = 0
        if count > 1:
            tender_index = handlers.find_smallest_area_tender(tenders)

        tender = BaseTender.model_validate(tenders[tender_index])

        tender_data = handlers.get_tender(tender_id=tender.id)
        tender_details = Tender.model_validate(tender_data)

        deposit = list(filter(lambda x: x.label == 'Размер задатка', tender_details.procedure_info))
        form = list(filter(lambda x: x.label == 'Форма проведения', tender_details.procedure_info))
        floor = list(filter(lambda x: x.label == 'Этаж', tender_details.object_info))
        parking_type = list(filter(lambda x: x.label == 'Тип парковки', tender_details.object_info))
        parking_place = list(filter(lambda x: x.label == 'Расположение', tender_details.object_info))

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
        parking_type = parking_type[0].value if parking_type else None

        parking_place = settings.GET_PARKPLACE_REGEX.findall(parking_place[0].value)
        parking_place = parking_place[0][-1] if parking_place else None
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
        sheet_row['Колличество'] = count
        sheet_row['Этаж'] = floor
        sheet_row['Тип парковки'] = parking_type
        sheet_row['Ссылка на investmoscow'] = settings.BASEURL + tender.url
        sheet_row['Место'] = parking_place
        sheet_row['площадь'] = tender.object_area
        parsed_objects.append(sheet_row)
        # objects_photos[tender.id] = tender_details.image_info.attached_images
        objects_photos[tender.id] = tender_details.image_info.model_dump(mode='json')
        print(sheet_row)


def parse_tenders():
    objects = handlers.get_tenders(settings.PAGENUMBER, settings.PAGESIZE)
    total_count = objects['totalCount']

    total_pages_count = total_count // settings.PAGESIZE + (1 if total_count % settings.PAGESIZE else 0) 

    parsed_objects = []
    objects_photos = {}
    parse_objects_tenders(objects, parsed_objects, objects_photos)
    for pagenum in range(settings.PAGENUMBER + 1, total_pages_count + 1):
        objects = handlers.get_tenders(pagenum, settings.PAGESIZE)
        parse_objects_tenders(objects, parsed_objects, objects_photos)
    return parsed_objects, objects_photos


def main():
    tenders, tenders_photos = parse_tenders()

    sa = pygsheets.authorize(service_file=settings.GSHEETS_CREDS_PATH)
    sh = sa.open_by_url(settings.GSHEETURL)
    parking_spaces = sh.worksheet_by_title('Машиноместа (копия)')

    sheet = pd.DataFrame(parking_spaces.get_all_records())
    parsed = pd.DataFrame(tenders)
    newdf = merge_data_to_sheet(sheet, parsed, on='tender_id', columns_order=settings.COLUMNS)
    newdf = newdf.astype({'Колличество': 'int32'})

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(newdf)
    with open('photos.json', 'w', encoding='utf-8') as f:
        json.dump(tenders_photos, f, ensure_ascii=False, indent=4)
    
    # parking_spaces.set_dataframe(
    #     newdf.loc[:, :'Ссылка на investmoscow'], 
    #     start='A2', 
    #     nan='',
    #     copy_head=False,
    #     escape_formulae=True
    # )
    # parking_spaces.set_dataframe(
    #     newdf.loc[:, 'Место':],
    #     start='W2', 
    #     nan='',
    #     copy_head=False,
    #     escape_formulae=True
    # )

if __name__ == '__main__':
    main()