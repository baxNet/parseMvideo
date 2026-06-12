import aiohttp
import asyncio
import data
import json
import random

import requests
import time
from tqdm import tqdm

import csv
import os

all_product_ids = []
all_products = []
# result = {
#     'productId': [],
#     'salePrice': [],
#     'basePrice': [],
#     'discount': [], #скидка в процентах
#     'ratingCount': [],
#     'ratingStar': [],
#     'Процессор': [],
#     'Оперативная память': [],
#     'Жесткий диск': [],
#     'Видеокарта': [],
#     'Операционная система': [],
#     'Клавиатура': [],
#     'Вес': []
# }
table = [
    ['productId', 'name', 'slug', 'salePrice', 'basePrice', 'ratingCount', 'ratingStar', 'Процессор', 'Оперативная память', 'Жесткий диск', 'Видеокарта', 'Операционная система', 'Клавиатура', 'Вес']
]

def array_to_csv(data, filename, delimiter=','):
    """
    Преобразует массив массивов в CSV файл
    
    Args:
        data: список списков (массив массивов)
        filename: имя выходного CSV файла
        delimiter: разделитель (по умолчанию ',')
    """
    if not data:
        print("Данные пусты")
        return
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter)
            writer.writerows(data)
        
        print(f"CSV файл '{filename}' успешно создан!")
    
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")


def remove_duplicates(input_list):
    return list(set(input_list))

async def main():
    global all_product_ids
    # Смотрим кол-во товаров
    async with aiohttp.ClientSession() as session:
        async with session.post(data.all_notebooks.url, cookies=data.all_notebooks.cookies, headers=data.all_notebooks.headers, json=data.all_notebooks.json_data) as response:
            first_json_data = await response.json()
            print(first_json_data['body']['cursorId'])
            print(first_json_data['body']['total'])
            json_rs = first_json_data
            for product in json_rs['body']['items']:
                all_product_ids.append(product['productId'])

    # Парсим айдишники всех товаров
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(first_json_data['body']['total']//60+1):
            json_data = data.all_notebooks.json_data.copy()
            json_data['cursorId'] = f'{i*60}'
            # print(json_data is data.all_notebooks.json_data)
            tasks.append(
                asyncio.create_task(
                    parse_first_stage(
                        session=session,
                        json_data=json_data
                    )
                )
            )
        await asyncio.gather(*tasks)

    #all_product_ids = remove_duplicates(all_product_ids)
    # print('Начинаем парсить ноутбуки асинхронно (есть шанс на блокировку парсера)')
    # #Парсим сами товары
    # async with aiohttp.ClientSession(cookies=data.notebook_data.cookies) as session:
    #     tasks = []
    #     #all_product_ids = all_product_ids[:10]
    #     for i in all_product_ids:
    #         params_cp = data.notebook_data.params.copy()
    #         params_cp['productId'] = random.choice(all_product_ids)
    #         tasks.append(
    #             asyncio.create_task(
    #                 parse_second_stage(
    #                     session=session,
    #                     params=params_cp
    #                 )
    #             )
    #         )
    #     await asyncio.gather(*tasks)
    # print('Парсинг удался! Начинаю запись в файл')

    parse_second_stage_noas(sl_time=1)

    with open('table.json', 'w', encoding='utf-8') as f:
        json.dump(table, f, indent=4, ensure_ascii=False)
        print("Файл table.json успешно записан в корневой каталог проекта")

            

def parse_second_stage_noas(sl_time=1):
    for id_id in tqdm(range(len(all_product_ids))):
        params_cp = data.notebook_data.params.copy()
        params_cp['productId'] = all_product_ids[id_id]
        response = requests.get(data.notebook_data.url, params=params_cp, cookies=data.notebook_data.cookies, headers=data.notebook_data.headers)
        if response.status_code == 200:
            rs_data = response.json()
            try:#процессор
                for j in rs_data['body']['properties']['key']:
                    if j['name'] == 'Процессор':
                        table[id_id+1].append(j['properties'][0]['value'])
                        break
            except Exception:
                table[id_id+1].append(None)
                            
            try:
                for j in rs_data['body']['properties']['key']:
                    if j['name'] == 'Оперативная память':
                        table[id_id+1].append(j['properties'][0]['value'])
                        break
            except Exception:
                table[id_id+1].append(None)
                            
            try:
                for j in rs_data['body']['properties']['key']:
                    if j['name'] == 'Жесткий диск':
                        table[id_id+1].append(j['properties'][0]['value'])
                        break
            except Exception:
                table[id_id+1].append(None)
                            
            try:
                for j in rs_data['body']['properties']['key']:
                    if j['name'] == 'Видеокарта':
                        table[id_id+1].append(j['properties'][0]['value'])
                        break
            except Exception:
                table[id_id+1].append(None)
                            
            try:
                for j in rs_data['body']['properties']['key']:
                    if j['name'] == 'Операционная система':
                        table[id_id+1].append(j['properties'][0]['value'])
                        break
            except Exception:
                table[id_id+1].append(None)
                            
            try:
                for j in rs_data['body']['properties']['key']:
                    if j['name'] == 'Клавиатура':
                        table[id_id+1].append(j['properties'][0]['value'])
                        break
            except Exception:
                table[id_id+1].append(None)
                            
            try:
                for j in rs_data['body']['properties']['key']:
                    if j['name'] == 'Вес':
                        table[id_id+1].append(j['properties'][0]['value'])
                        break
            except Exception:
                table[id_id+1].append(None)

            with open('result/table.json', 'w', encoding='utf-8') as f:
                json.dump(table, f, indent=4, ensure_ascii=False)
            #print(f'Created! {params_cp['productId']}')
            time.sleep(sl_time)
            





async def parse_second_stage(session, params):
    async with session.get(data.notebook_data.url, params=params, headers=data.notebook_data.headers) as response:
        rs_data = await response.json()
        
        for i, line in enumerate(table):
            if params['productId'] in line:
                
                try:#процессор
                    for j in rs_data['body']['properties']['key']:
                        if j['name'] == 'Процессор':
                            table[i].append(j['properties'][0]['value'])
                            break
                except Exception:
                    table[i].append(None)
                                
                try:
                    for j in rs_data['body']['properties']['key']:
                        if j['name'] == 'Оперативная память':
                            table[i].append(j['properties'][0]['value'])
                            break
                except Exception:
                    table[i].append(None)
                                
                try:
                    for j in rs_data['body']['properties']['key']:
                        if j['name'] == 'Жесткий диск':
                            table[i].append(j['properties'][0]['value'])
                            break
                except Exception:
                    table[i].append(None)
                                
                try:
                    for j in rs_data['body']['properties']['key']:
                        if j['name'] == 'Видеокарта':
                            table[i].append(j['properties'][0]['value'])
                            break
                except Exception:
                    table[i].append(None)
                                
                try:
                    for j in rs_data['body']['properties']['key']:
                        if j['name'] == 'Операционная система':
                            table[i].append(j['properties'][0]['value'])
                            break
                except Exception:
                    table[i].append(None)
                                
                try:
                    for j in rs_data['body']['properties']['key']:
                        if j['name'] == 'Клавиатура':
                            table[i].append(j['properties'][0]['value'])
                            break
                except Exception:
                    table[i].append(None)
                                
                try:
                    for j in rs_data['body']['properties']['key']:
                        if j['name'] == 'Вес':
                            table[i].append(j['properties'][0]['value'])
                            break
                except Exception:
                    table[i].append(None)
                print(f'Created! {params['productId']}')
            





async def parse_first_stage(session, json_data):
    async with session.post(data.all_notebooks.url, cookies=data.all_notebooks.cookies, headers=data.all_notebooks.headers, json=json_data) as response:
        print(json_data['cursorId'])
        json_rs = await response.json()
        for product in json_rs['body']['items']:
            all_product_ids.append(product['productId'])

            table.append([])
            table[-1].append(product['productId'])
            try:
                table[-1].append(product['name'])
            except Exception:
                table[-1].append(None)

            try:
                table[-1].append(f'https://www.mvideo.ru{product['slug']}')
            except Exception:
                table[-1].append(None)

            try:
                table[-1].append(product['price']['salePrice'])
            except Exception:
                table[-1].append(None)

            try:
                table[-1].append(product['price']['basePrice'])
            except Exception:
                table[-1].append(None)

            table[-1].append(product['rating']['count'])
            table[-1].append(product['rating']['star'])


if __name__ == '__main__':
    os.makedirs('result', exist_ok=True)
    asyncio.run(main())
    array_to_csv(table, 'result/notebooks.csv')
    
