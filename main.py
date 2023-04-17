from fastapi import FastAPI, File
from peewee import SqliteDatabase
from config import *
from loguru import logger
from typing import Annotated

logger.add(**LOGGER_ERRORS)
logger.add(**LOGGER_DEBUG)

db = SqliteDatabase(**DATABASE_CONFIG)


def update_user_balance_requests(add_to_balance, user_id):
    with db:
        db.execute_sql(f'UPDATE users SET balance_requests = balance_requests + ? WHERE user_id= ?;',
                       (add_to_balance, user_id))

        cursor = db.execute_sql(f'SELECT balance_requests FROM users WHERE user_id = ?;', (user_id,))
        if update_user_balance_request := cursor.fetchone():
            result = {'new_balance': update_user_balance_request[0]}
        else:
            result = {'error': 'user not found'}
        return {'user_id': user_id} | result


app = FastAPI()


@app.post('/json')
def router_post_update(data: dict) -> dict:
    logger.warning(f'incoming request -> method POST {data=}')

    user_id = data.get('_param_user_id')
    add_to_balance = data.get('products')[0].get('quantity')
    print(user_id, add_to_balance)
    update_data = update_user_balance_requests(add_to_balance=add_to_balance, user_id=user_id)

    if update_data.get('error'):
        logger.warning(str(update_data.get('error')))
    return update_data


@app.post('/form_data')
def router_post_update(file: Annotated[bytes, File()]) -> dict:
    logger.warning(f'incoming request -> method POST -> multipart/form-data {file}')
    return {"file_size": len(file)}


@app.get('/')
def router_get_update() -> dict:
    logger.warning(f'incoming request -> method GET')
    return {'detail': 'method not allowed'}

# import subprocess
# subprocess.run('uvicorn main:app --reload')

"""{
"date":"2023-04-17T19:53:10+03:00",
"order_id":"11665981",
"order_num":"1",
"domain":"marpla.payform.ru",
"sum":"300.00","currency":"rub",
"customer_phone":"",
"customer_email":"super.nvhelp@yandex.ru",
"customer_extra":"",
"payment_type":"\u041e\u043f\u043b\u0430\u0442\u0430 \u043a\u0430\u0440\u0442\u043e\u0439, \u0432\u044b\u043f\u0443\u0449\u0435\u043d\u043d\u043e\u0439 \u0432 \u0420\u0424",
"commission":"3.5",
"commission_sum":"10.50",
"attempt":"1",
"_param_user_id":"1438292311",
"products":[{"name":"\u0417\u0430\u043f\u0440\u043e\u0441",
             "price":"10.00",
             "quantity":"30",
             "sum":"300.00"}],
"payment_status":"success",
"payment_status_description":"\u0423\u0441\u043f\u0435\u0448\u043d\u0430\u044f \u043e\u043f\u043b\u0430\u0442\u0430",
"payment_init":"manual"}"""