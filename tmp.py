import aiohttp
import asyncio
import json

from urllib.parse import urlencode

from config import settings
from models.tender_models import Tender


def get_images_list():
    with open('tender_data.json', 'r', encoding='utf-8') as f:
        tender = Tender.model_validate_json(f.read())
    # for image in tender.image_info.attached_images:
    #     print(image.tender_id)
    #     print(image.url)
    #     print(image.is_main_photo)
    #     print(image.file_base.name)
    #     print('------------------------\n')
    return tender.image_info.attached_images


async def get_drive_info(session):
    url = 'https://cloud-api.yandex.net/v1/disk/'
    async with session.get(url) as response:
        return response.status, await response.json()


async def get_item_info(session, url=None, path=None):
    params = {
        'fields': 'name,type,_embedded,_embedded.path,_embedded.items.path,_embedded.items.type,_embedded.items.name'
    }
    if not url:
        params['path'] = path
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
    async with session.get(url, params=params) as response:
        return response.status, await response.json()


async def create_folder(session, path):
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {'path': path}
    async with session.put(url, params=params) as response:
        return response.status, await response.json()


async def upload_file_from_web(session, url, path):
    url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    params = {
        'url': url,
        'path': path
    }
    async with session.put(url, params=params) as response:
        return response.status, await response.json()


async def get_operation_status(session, path):
    ...


async def upload_files(session, path, images):
    for image in images:
        status, response = await upload_file_from_web(
            session,
            image.url,
            f'{path}/{image.file_base.name}'
        )
        print('upload', response, status)
        async with session.get(response['href']) as response:
            print('statue', await response.json())


async def main():
    headers =  {'accept': 'application/json', 'Authorization': f'OAuth {settings.YADISK_OAUTH_TOKEN}'}
    tender_id = 19284836
    path = f'app:/parking_spaces/{tender_id}'

    images = get_images_list()
    async with aiohttp.ClientSession(headers=headers) as session:
        status, response = await create_folder(session, 'app:/parking_spaces')
        if status != 201 and status != 409:
            print('Cant create folder:', response)
            return
        if status == 201:
            status, response = await create_folder(session, path=path)
            if status != 201:
                print('Cant create folder:', response)
                return
            # for tender in tenders:
            await upload_files(session, path, images)
        else:
            status, response = await get_item_info(session, path=path)
            if status == 404:
                status, response = await create_folder(session, path=path)
                if status != 201:
                    print('Cant create folder:', response)
                    return
            await upload_files(session, path, images)
            
    with open('disk.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(response, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    asyncio.run(main())
