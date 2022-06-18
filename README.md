# Шаблон телеграм бот + админ панель джанго.

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## Описание проекта:
Созданы модели:
- Заказов
- Категорий
- Подкатегорий
- Клиентов телеграмм бота
- Товары

Установлена связь телеграмм бота и Django.

## Запуск проекта

Склонируйте репозиторий.

Запустить проект можно командой:
 
``` 
docker-compose up
``` 

Утановите разрешенный IP (IP вашего сервера) для админ панели. В папке admin_panel ➡️ admin_panel ➡️ settings.py

```buildoutcfg
ALLOWED_HOSTS = ['<IP вашего сервера>', '127.0.0.1', 'localhost']
```

После команды docker-compose up. Перейдите в контейнер admin_panel

``` 
sudo docker exec -it admin_panel bash
``` 

И пропишите команду для создания супер пользователя:

``` 
python django_app.py createsuperuser
``` 

Все миграции выполняются автоматически.