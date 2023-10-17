import asyncio
import aiohttp
import pygsheets

from config import settings
from src.upload_images import get_item_info


async def collect_images_links(worksheet, basefolder, sheet_column) -> list:
    DISK_AUTH_HEADERS: str = {'accept': 'application/json', 'Authorization': 'OAuth %s' % settings.YADISK_OAUTH_TOKEN}
    tenders_ids = worksheet.get_values_batch(['B:B'])[0][1:]
    async with aiohttp.ClientSession(headers=DISK_AUTH_HEADERS) as session:
        images = []
        for tender_id in tenders_ids:
            foldername = f'{basefolder}/{tender_id[0]}'
            status, response = await get_item_info(session=session, path='app:/' + foldername)
            if status == 200:
                _images = []
                for image in response['_embedded']['items']:
                    _images.append(image['file'])
                images.append([' | '.join(_images)])
            else:
                images.append([''])
    worksheet.update_values(f'{sheet_column}2', images)
    return images


async def collect_images_links_for_avito(worksheets, basefolders, sheet_columns):
    for worksheet, folder, column in zip(worksheets, basefolders, sheet_columns):
        images: list = await collect_images_links(
            worksheet=worksheet, 
            basefolder=folder,
            sheet_column=column
        )


if __name__ == '__main__':
    sa = pygsheets.authorize(service_file=settings.GSHEETS_CREDS_PATH)
    sh = sa.open_by_url(settings.GSHEETURL)
    wks_list = sh.worksheets()

    asyncio.run(
        collect_images_links_for_avito(
            worksheets=wks_list, 
            basefolders=['parking_spaces', 'nonresidential'],
            sheet_columns=['Y', 'T']
        )
    )
