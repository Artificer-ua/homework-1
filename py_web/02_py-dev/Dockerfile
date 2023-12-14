FROM python:3.11-slim

#ENV APP_HOME /app
#WORKDIR $APP_HOME
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./tough_assistant /app/

#EXPOSE 5000

#ENTRYPOINT ["python", "main.py"]
CMD ["python", "main.py"]