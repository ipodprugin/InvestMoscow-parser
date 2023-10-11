import json

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
