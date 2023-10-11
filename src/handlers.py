import http.client
import json

conn = http.client.HTTPSConnection('api.investmoscow.ru')


def get_tenders(page_number, page_size):
    payload = """
    {
        "pageNumber": %d,
        "pageSize": %d,
        "orderBy": "Relevance",
        "orderAsc": false,
        "objectTypes": ["nsi:41:30011578"],
        "tenderStatus": "nsi:tender_status_tender_filter:1",
        "timeToPublicTransportStop": {
            "noMatter": true
        }
    }
    """
    headers = {
        'authority': "api.investmoscow.ru",
        'accept': "application/json",
        'accept-language': "ru-RU",
        'content-type': "application/json",
        'origin': "https://investmoscow.ru",
        'referer': "https://investmoscow.ru/",
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-site",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.2271 YaBrowser/23.9.0.2271 Yowser/2.5 Safari/537.36",
        'x-requested-with': "XMLHttpRequest"
        }

    api_url = '/investmoscow/tender/v2/filtered-tenders/searchTenderObjects'
    conn.request(
        'POST', 
        api_url, 
        payload % (page_number, page_size), 
        headers
    )

    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)
    return data


def get_tender(tender_id):
    headers = {
        'authority': "api.investmoscow.ru",
        'accept': "application/json",
        'accept-language': "ru-RU",
        'origin': "https://investmoscow.ru",
        'referer': "https://investmoscow.ru/",
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-site",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.2271 YaBrowser/23.9.0.2271 Yowser/2.5 Safari/537.36",
        'x-requested-with': "XMLHttpRequest"
        }

    conn.request("GET", f'/investmoscow/tender/v1/object-info/getTenderObjectInformation?tenderId={tender_id}', headers=headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)
    return data


def find_smallest_area_tender(tenders):
    tender_index = 0
    for index, tender in enumerate(tenders):
        min_area = tender.get('objectArea', None)
        if min_area:
            tender_index = index
            break
    else:
        return tender_index
    for index, tender in enumerate(tenders[tender_index:]):
        tender_area = tender.get('objectArea', None)
        if tender_area:
            if tender['objectArea'] < min_area:
                min_area = tender['objectArea']
                tender_index = index
    return tender_index
