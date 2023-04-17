## Установка
pip install --upgrade pip
pip install fastapi[all] loguru peewee
pip install "uvicorn [standard]" gunicorn

## Запуск в dev
uvicorn main:app --reload

## Запуск в productions
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80

### С контейнером не получается нет доступа к файлу бд, запускать без докера 
- Создать образ контейнера - docker build -t payment_app_image .
- Запуск контейнера - docker run -d --name payment_app_container -p 8000:8000 payment_app_image

Для тестирования через curl
curl -X 'POST' \
  'http://5.44.40.79/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"user_id": "1438292311", "add_to_balance": 15}'


curl -X 'POST' \
  'http://127.0.0.1:8000/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"user_id": "1438292311", "add_to_balance": 15}'


  -H 'Content-type:text/plain;charset=utf-8' \

curl -X 'POST' \
'https://demo.payform.ru/' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{"do": "link", "order_id": 1, "products": {"name": "Запрос к боту", "price": 10, "quantity": 30}, "customer_extra": "Оплата от пользователя - 12345", "urlReturn": "https://t.me/BotForDev_bot", "urlSuccess": "https://t.me/BotForDev_bot", "urlNotification": "", "sys": "", "npd_income_type": "FROM_INDIVIDUAL", "paid_content": "Благодарим за оплату", "demo_mode": 1, "signature": "2y2aw4oknnke80bp1a8fniwuuq7tdkwmmuq7vwi4nzbr8z1182ftbn6p8mhw3bhz"}'