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
  'http://127.0.0.1:8000/payment_form_data' \
  -H 'Sign=bjclbljblcaskkcnak' \
  -d 'date=2023-04-18T00%3A00%3A00%2B03%3A00&order_id=1&order_num=test&domain=marpla.payform.ru&sum=1000.00&customer_phone=%2B79999999999&customer_email=email%40domain.com&customer_extra=%D1%82%D0%B5%D1%81%D1%82&payment_type=%D0%9F%D0%BB%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%BE%D0%B2%D0%B0%D1%8F+%D0%BA%D0%B0%D1%80%D1%82%D0%B0+Visa%2C+MasterCard%2C+%D0%9C%D0%98%D0%A0&commission=3.5&commission_sum=35.00&attempt=1&sys=test&products%5B0%5D%5Bname%5D=%D0%94%D0%BE%D1%81%D1%82%D1%83%D0%BF+%D0%BA+%D0%BE%D0%B1%D1%83%D1%87%D0%B0%D1%8E%D1%89%D0%B8%D0%BC+%D0%BC%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D0%B0%D0%BC&products%5B0%5D%5Bprice%5D=1000.00&products%5B0%5D%5Bquantity%5D=1&products%5B0%5D%5Bsum%5D=1000.00&payment_status=success&payment_status_description=%D0%A3%D1%81%D0%BF%D0%B5%D1%88%D0%BD%D0%B0%D1%8F+%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D0%B0'


curl -X 'POST' \
  'http://5.44.40.79/payment_form_data' \
  -H 'Content-Type: application/json' \
  -d '{"user_id": "1438292311", "add_to_balance": 15}'

curl -X 'POST' \
  'http://5.44.40.79/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"user_id": "1438292311", "add_to_balance": 15}'

curl -X 'POST' \
  'http://127.0.0.1:8000/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{ "date":"2023-04-17T19:53:10+03:00",
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
        "payment_init":"manual"}'


  -H 'Content-type:text/plain;charset=utf-8' \

curl -X 'POST' \
'https://demo.payform.ru/' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{"do": "link", "order_id": 1, "products": {"name": "Запрос к боту", "price": 10, "quantity": 30}, "customer_extra": "Оплата от пользователя - 12345", "urlReturn": "https://t.me/BotForDev_bot", "urlSuccess": "https://t.me/BotForDev_bot", "urlNotification": "", "sys": "", "npd_income_type": "FROM_INDIVIDUAL", "paid_content": "Благодарим за оплату", "demo_mode": 1, "signature": "2y2aw4oknnke80bp1a8fniwuuq7tdkwmmuq7vwi4nzbr8z1182ftbn6p8mhw3bhz"}'