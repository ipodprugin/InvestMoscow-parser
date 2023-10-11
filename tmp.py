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


async def upload_file_from_web(session, imageurl, path):
    url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    params = {
        'url': imageurl,
        'path': path
    }
    async with session.post(url, params=params) as response:
        return response.status, await response.json()


async def get_operation_status(session, url):
    async with session.get(url) as response:
        resp = await response.json()
        return resp['status']


async def upload_files(session, path, images):
    status_links = {}
    upload_error = {}
    for image in images:
        status, response = await upload_file_from_web(
            session,
            image.url,
            f'{path}/{image.file_base.name}'
        )
        if status == 202:
            status_links[image.url] = response['href']
        else:
            upload_error[image.url] = response
        print('upload', response, status)
    return status_links, upload_error


async def check_images_upload_status(session, images_status_links):
    # in_progress = {}
    for tender_id, images in images_status_links.items():
        for imageurl, statusurl in images.items(): 
            async with session.get(statusurl) as response:
                resp = await response.json()
                print('statue', resp['status'], imageurl, statusurl)


async def main():
    headers =  {'accept': 'application/json', 'Authorization': f'OAuth {settings.YADISK_OAUTH_TOKEN}'}
    tender_id = 19284836
    path = f'app:/parking_spaces/{tender_id}'

    images = get_images_list()
    images_status_links = {}
    async with aiohttp.ClientSession(headers=headers) as session:
        status, response = await create_folder(session, 'app:/parking_spaces')
        if status != 201 and status != 409:
            print('Cant create folder:', response)
            return
        if status == 201:
            # for tender in tenders:
            status, response = await create_folder(session, path=path)
            if status != 201:
                print('Cant create folder:', response)
                return
            status_links, upload_error = await upload_files(session, path, images)
            images_status_links[tender_id] = status_links
        else:
            status, response = await get_item_info(session, path=path)
            if status == 404:
                status, response = await create_folder(session, path=path)
                if status != 201:
                    print('Cant create folder:', response)
                    return
            status_links, upload_error = await upload_files(session, path, images)
            images_status_links[tender_id] = status_links
            print(images_status_links)
        
        await check_images_upload_status(session, images_status_links)
            
    with open('disk.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(response, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    asyncio.run(main())
