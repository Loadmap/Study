from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# 터미널에서 uvicorn main:app --reload

app = FastAPI()

users = {
    0 : {'userid' : 'apple', 'name' : '사과'},
    1 : {'userid' : 'orange', 'name' : '오렌지'},
    2 : {'userid' : 'lemon', 'name' : '레몬'},
    3 : {'userid' : 'cherry', 'name' : '체리'}
}

# http://127.0.0.1:8000 내 컴퓨터에서 동작하는 가상 ip, port 번호
@app.get('/')
async def root() :

    return{'message' : 'Hello FastAPI!'}

# http://127.0.0.1:8000/users/{id}
@app.get('/users/{id}')
async def find_user(id : int) :
    item = users[id]

    return item

# http://127.0.0.1:8000/users/0/userid

@app.get('/users/{id}/{key}')
async def find_user_by_key(id : int, key : str) :
    user = users[id][key]

    return user

# http://127.0.0.1:8000/users/id-by-name?name=사과

# @app.get('/users/id-by-name')
# async def find_user_by_name(name : str) :
#
#     for userid, user in users.items() :
#
#         if user['name'] == name :
#
#             return user
#
#     return {'error' : '데이터를 찾지 못함'}

# http://127.0.0.1:8000/users/0 확인불가
class User(BaseModel) :
    userid : str
    name : str

@app.post('/users/{id}')
async def create_user(id : int, user : User) :

    if id in users :

        return {'error' : '이미 존재하는 키'}

    users[id] = user.__dict__

    return {'success' : 'ok'}

class UserForUpdate(BaseModel) :
    userid : Optional[str]
    name : Optional[str]

@app.put('/users/{id}')
async def update_user(id : int, user : UserForUpdate) :

    if id not in users :
        return{'error' : 'id 가 존재하지 않음'}

    if user.userid :
        users[id]['userid'] = user.userid

    if user.name :
        users[id]['name'] = user.name

    return {'success' : 'ok'}

@app.delete('/users/{id}')
def delete_item(id : int) :
    users.pop(id)

    return{'success' : 'ok'}
