import datetime

import requests
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from admin_panel.telebot.forms import AddForm
from admin_panel.telebot.models import Client, Orders, BOT_TOKEN


def statistics(request):
    form = AddForm(request.POST or None)
    template = 'statistics/index.html'
    count_clients = Client.objects.all().count()
    count_orders = Orders.objects.all().count()
    delivered_orders = Orders.objects.filter(status="delivered").count()
    amount_orders = Orders.objects.aggregate(Sum('price'))['price__sum']

    date = datetime.datetime.today()
    week = date.strftime("%V")
    count_orders_week = Orders.objects.filter(created__week=week).count()
    amount_orders_week = Orders.objects.filter(created__week=week).aggregate(Sum('price'))['price__sum']
    count_clients_week = Client.objects.filter(created__week=week).count()
    cost_price_week = Orders.objects.filter(created__week=week).aggregate(Sum('cost_price'))['cost_price__sum']

    now = timezone.now()
    count_orders_today = Orders.objects.filter(created__date=now.date()).count()
    amount_orders_today = Orders.objects.filter(created__date=now.date()).aggregate(Sum('price'))['price__sum']
    count_clients_today = Client.objects.filter(created__date=now.date()).count()
    cost_price_today = Orders.objects.filter(created__date=now.date()).aggregate(Sum('cost_price'))['cost_price__sum']

    count_orders_months = Orders.objects.filter(created__gt=timezone.now() - relativedelta(months=1)).count()
    amount_orders_months = \
        Orders.objects.filter(created__gt=timezone.now() - relativedelta(months=1)).aggregate(Sum('price'))[
            'price__sum']
    count_clients_months = Client.objects.filter(created__gt=timezone.now() - relativedelta(months=1)).count()
    cost_price_months = \
        Orders.objects.filter(created__gt=timezone.now() - relativedelta(months=1)).aggregate(Sum('cost_price'))[
            'cost_price__sum']

    if amount_orders_week is None:
        amount_orders_week = 0
    if cost_price_week is None:
        cost_price_week = 0
    if amount_orders_today is None:
        amount_orders_today = 0
    if cost_price_today is None:
        cost_price_today = 0
    if amount_orders_months is None:
        amount_orders_months = 0
    if cost_price_months is None:
        cost_price_months = 0
    if amount_orders is None:
        amount_orders = 0
    context = {
        'count_orders': count_orders,
        'count_clients': count_clients,
        'delivered_orders': delivered_orders,
        'amount_orders': amount_orders,
        'count_orders_week': count_orders_week,
        'amount_orders_week': amount_orders_week,
        'count_clients_week': count_clients_week,
        'count_orders_today': count_orders_today,
        'amount_orders_today': amount_orders_today,
        'count_clients_today': count_clients_today,
        'count_orders_months': count_orders_months,
        'amount_orders_months': amount_orders_months,
        'count_clients_months': count_clients_months,
        'cost_price_today': cost_price_today,
        'cost_price_week': cost_price_week,
        'cost_price_months': cost_price_months,

    }
    if request.method != 'POST':
        context.update({'form': form})
        return render(request, template, context)
    if not form.is_valid():
        return render(request, template, {'form': form})
    if form.is_valid():
        message = form.cleaned_data.get("message")
        users = Client.objects.all()
        count_users = Client.objects.all().count()
        for user in users:
            requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/"
                f"sendMessage?chat_id={user.telegram_id}&text="
                f"{message}&parse_mode=html"
            )
        form = AddForm()
        context.update({'form': form})
        is_mailing = True
        context.update({'is_mailing': is_mailing})
        context.update({'count_users': count_users})
        return render(request, template, context)
