FROM python:3

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /usr/src/app/shopyo
RUN python manage.py db init    && \
    python manage.py db migrate && \
    python manage.py db upgrade && \
    python initialise.py        && \
    python apply_settings.py
EXPOSE 5000
CMD [ "python", "run.py" ]