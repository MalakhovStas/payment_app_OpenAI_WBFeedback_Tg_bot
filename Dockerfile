#с докером нее работает нетдоступа к БД
FROM python:3.10
WORKDIR /OpenAI_WBFeedback_Tg_bot_patment_app
COPY ./requirements.txt /OpenAI_WBFeedback_Tg_bot_patment_app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /OpenAI_WBFeedback_Tg_bot_patment_app/requirements.txt
COPY . .
#CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "5.44.40.79", "--port", "1234"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
