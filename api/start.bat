cd /d C:\Users\User\Downloads\PI\pi-I-main\api

call venv\Scripts\activate

set DB_NAME=pi-I
set DB_USER=neondb_owner
set DB_PASSWORD=npg_9wC0GlWeRLsb
set DB_HOST=ep-quiet-sky-acbzlhu2.sa-east-1.aws.neon.tech
set DB_PORT=5432
set DB_SSL=require

python manage.py runserver

pause