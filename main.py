from urllib import parse

from fastapi import FastAPI, Request
from loguru import logger
from peewee import SqliteDatabase

from config import *

logger.add(**LOGGER_ERRORS)
logger.add(**LOGGER_DEBUG)

db = SqliteDatabase(**DATABASE_CONFIG)


def update_user_balance_requests(data):
    # quantity = data.get('products[0][quantity]')
    payment_status = data.get('payment_status')
    package_name = data.get('products[0][name]')
    quantity = PAYMENTS_PACKAGES.get(package_name).get('quantity')
    user_id = data.get('_param_user_id')
    order_id_payment_system = data.get('order_id')
    order_num = data.get('order_num')

    if quantity and user_id:
        with db:
            db.execute_sql(f'UPDATE users SET balance_requests = balance_requests + ? WHERE user_id= ?;',
                           (quantity, user_id))
            db.execute_sql(f'UPDATE payments SET payment_status = ?, notification_data = ?, order_id_payment_system = ?'
                           f' WHERE id = ?;', (payment_status, data, order_id_payment_system, order_num))

            cursor = db.execute_sql(f'SELECT balance_requests FROM users WHERE user_id = ?;', (user_id,))
            if update_user_balance_request := cursor.fetchone():
                result = {'new_balance': update_user_balance_request[0]}
            else:
                result = {'error': 'user not found', 'user_id': user_id}
            return {'user_id': user_id, 'quantity': quantity} | result
    return {'error': 'not valid', 'user_id': user_id, 'quantity': quantity}


app = FastAPI()


@app.post('/payment_form_data')
async def post_payment_form_data(request: Request) -> dict:
    sign = request.headers.get('Sign')
    in_data = await request.body()
    decoded_data = parse.unquote(in_data.decode('utf-8'))
    data = dict(parse.parse_qsl(decoded_data))

    if data.get('payment_status') == 'success':
        try:
            result = update_user_balance_requests(data)
        except Exception as exc:
            result = {'ERROR': exc}
    else:
        result = {"payment_status": f"not valid -> {data.get('payment_status')}"}

    if result.get('new_balance'):
        logger.info(f'request -> POST -> {result=}| {data=} | {sign=}')
        response = {'internal_processing_result': 'Successful'}
    else:
        logger.error(f'request -> POST -> {result=} | {data=} | {sign=}')
        response = {'internal_processing_result': 'Failed'}

    return response
