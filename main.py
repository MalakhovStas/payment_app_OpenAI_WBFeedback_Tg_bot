from fastapi import FastAPI, Query
from peewee import SqliteDatabase
from config import *
from loguru import logger


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


@app.post('/')
def router_post_update(data: dict) -> dict:
    logger.warning(f'incoming request -> method POST {data=}')
    user_id = data.get('user_id')
    add_to_balance = data.get('add_to_balance')

    update_data = update_user_balance_requests(add_to_balance=add_to_balance, user_id=user_id)

    if update_data.get('error'):
        logger.warning(str(update_data.get('error')))
    return update_data


@app.get('/')
def router_get_update() -> dict:
    logger.warning(f'incoming request -> method GET')
    return {'detail': 'method not allowed'}

# import subprocess
# subprocess.run('uvicorn main:app --reload')
