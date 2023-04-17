import re
from typing import Annotated

from fastapi import FastAPI, Request
from loguru import logger
from peewee import SqliteDatabase

from config import *

logger.add(**LOGGER_ERRORS)
logger.add(**LOGGER_DEBUG)

db = SqliteDatabase(**DATABASE_CONFIG)


def update_user_balance_requests(data):
    quantity = data.get('quantity')
    user_id = data.get('user_id')
    if quantity and user_id:
        with db:
            db.execute_sql(f'UPDATE users SET balance_requests = balance_requests + ? WHERE user_id= ?;',
                           (quantity, user_id))

            cursor = db.execute_sql(f'SELECT balance_requests FROM users WHERE user_id = ?;', (user_id,))
            if update_user_balance_request := cursor.fetchone():
                result = {'new_balance': update_user_balance_request[0]}
            else:
                result = {'error': 'user not found'}
            return {'user_id': user_id} | result
    return {'error': 'data not valid'}


app = FastAPI()


@app.post('/payment_form_data')
async def post_payment_form_data(request: Request) -> dict:
    sign = request.headers.get('Sign')
    in_data = (await request.body()).decode('utf-8')
    logger.debug(in_data)
    order_id = re.search(r"'order_id' => '(\d+)'", in_data)
    user_id = re.search(r"'_param_user_id' => '(\d+)'", in_data)
    quantity = re.search(r"'quantity' => '(\d+)'", in_data)
    payment_status = re.search(r"'payment_status' => '(\S+)'", in_data)

    data = {
        "order_id": order_id.group(1) if order_id else None,
        "user_id": user_id.group(1) if user_id else None,
        "quantity": quantity.group(1) if quantity else None,
        "payment_status": payment_status.group(1) if payment_status else None,
    }

    if data.get('payment_status') == 'success':
        try:
            result = update_user_balance_requests(data)
        except Exception as exc:
            result = {'ERROR': exc}
    else:
        result = {"payment_status": f"not valid -> {data.get('payment_status')}"}

    if result.get('new_balance'):
        logger.info(f'incoming request -> method POST -> multipart/form-data -> {data=}  | {result=} | {sign=}')
        response = {'internal_processing_result': 'Successful'}
    else:
        logger.error(f'incoming request -> method POST -> multipart/form-data -> {data=}  | {result=} | {sign=}')
        response = {'internal_processing_result': 'Failed'}

    return response
