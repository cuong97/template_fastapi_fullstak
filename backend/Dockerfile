FROM python:3.10.4 as fastapi_api
WORKDIR /backend
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /backend/requirements.txt
COPY . /backend
ENV PYTHONPATH=/backend/app
EXPOSE 8000

RUN chmod +x run.sh
CMD ["./run.sh"]