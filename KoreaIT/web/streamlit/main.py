import openai
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import pandas as pd
import json

openai.api_key = ''
url = ''

client = MongoClient(url)

database = client['airproject']
collection = database['adapi']

class AdGenerator :

    def __init__(self, engine = 'gpt-3.5-turbo'):
        self.engine = engine

    def using_chatgpt(self, prompt) :
        system_instruction = 'assistant 는 마케팅 문구 작성 도우미로 동작한다. user의 내용을 참고하여 마케팅 문구를 작성해라.'
        message = [{'role' : 'system', 'content' : system_instruction},
                   {'role': 'user', 'content': prompt}]
        response = openai.chat.completions.create(model = self.engine, messages= message)
        result = response.choices[0].message.content.strip()

        return result

    def generate(self, product_name, details, tone_and_manner) :
        prompt = f'제품 이름 : {product_name}\n 주요내용 : {details}\n 광고문구의 스타일 : {tone_and_manner}'
        result = self.using_chatgpt(prompt = prompt)

        return result

app = FastAPI()

class Product(BaseModel) :
    product_name : str
    details : str
    tone_and_manner : str

@app.post('/create_ad')
async def create_ad(product : Product) :
    # print(product)

    ad_generator = AdGenerator()
    ad = ad_generator.generate(product_name = product.product_name,
                           details = product.details,
                           tone_and_manner = product.tone_and_manner)

    data_insert = {'product_name' : product.product_name,
                   'details' : product.details,
                   'tone_and_manner' : product.tone_and_manner,
                   'ad' : ad}

    result = collection.insert_one(data_insert)

    result2 = collection.find({})
    datas = []

    for data in result2 :
        data.pop('_id', None)
        datas.append(data)

    # print(datas)

    return {'ad' : ad, 'datas' : datas}
