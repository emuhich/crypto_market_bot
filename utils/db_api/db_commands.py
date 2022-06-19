from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404

from admin_panel.telebot.models import Product, Client, Questions, Category, SubCategory


@sync_to_async
def select_all_products():
    return Product.objects.all()


@sync_to_async()
def select_client(telegram_id):
    return Client.objects.get(telegram_id=telegram_id)


@sync_to_async()
def create_client(username, telegram_id):
    Client.objects.get_or_create(telegram_id=telegram_id, username=username)


@sync_to_async
def select_all_questions():
    return Questions.objects.all()


@sync_to_async
def get_question(pk):
    return get_object_or_404(Questions, pk=pk)


@sync_to_async
def update_client_info(telegram_id, fio=None, address=None, phone=None):
    user = Client.objects.get(telegram_id=telegram_id)
    if fio:
        user.full_name = fio
        user.save(update_fields=["full_name"])
        return user
    if address:
        user.address = address
        user.save(update_fields=["address"])
        return user
    if phone:
        user.phone = phone
        user.save(update_fields=["phone"])
        return user


@sync_to_async
def get_all_category():
    return Category.objects.all()


@sync_to_async
def get_category(pk):
    return Category.objects.get(pk=pk)


@sync_to_async
def get_sub_categories(pk):
    category = Category.objects.get(pk=pk)
    return category.sub_category.all()


@sync_to_async
def get_sub_category(pk):
    return SubCategory.objects.get(pk=pk)


@sync_to_async
def get_products(pk):
    sub_category = SubCategory.objects.get(pk=pk)
    return sub_category.products.exclude(quantity=0)


@sync_to_async
def get_product(pk):
    return Product.objects.get(pk=pk)
