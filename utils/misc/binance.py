from datetime import datetime, timedelta
from decimal import Decimal
from random import randint

from binance import AsyncClient

from utils.db_api.db_commands import get_binance_key, check_payment_id, create_payment_id


class Binance:

    @staticmethod
    async def get_client():
        api_key, api_secret = await get_binance_key()
        return await AsyncClient.create(api_key, api_secret)

    @staticmethod
    async def get_rand_commission():
        return Decimal(randint(1, 1000)) * Decimal("0.00000000001")

    @staticmethod
    async def get_rand_commission_usdt():
        return Decimal(randint(1, 1000)) * Decimal("0.0001")

    async def get_address_btc(self):
        client = await self.get_client()
        address = await client.get_deposit_address(coin='BTC')
        await client.close_connection()
        return address['address']

    async def get_address_usd(self):
        client = await self.get_client()
        address = await client.get_deposit_address(coin='USDT')
        await client.close_connection()
        return address['address']

    async def get_address_eth(self):
        client = await self.get_client()
        address = await client.get_deposit_address(coin='ETH')
        await client.close_connection()
        return address['address']

    async def get_price_btc_eth(self, amount):
        client = await self.get_client()
        tickers = await client.get_all_tickers()
        for ticker in tickers:
            if ticker['symbol'] == "BTCUSDT":
                amount_btc = round(amount / Decimal(ticker['price']), 7)

            if ticker['symbol'] == "ETHUSDT":
                amount_eth = round(amount / Decimal(ticker['price']), 7)
        await client.close_connection()
        return amount_btc, amount_eth

    async def check_payment(self, amount, coin):
        client = await self.get_client()
        expiry_date = datetime.utcnow() - timedelta(days=90)
        operations = await client.get_deposit_history(coin=coin,
                                                      startTime=int(expiry_date.timestamp()) * 1000)
        for operation in operations:
            if Decimal(operation['amount']) == amount and not await check_payment_id(operation['txId']):
                if operation['status'] == 1:
                    await create_payment_id(operation['txId'])
                    await client.close_connection()
                    return "Confirmed"
                elif operation['status'] != 1:
                    await client.close_connection()
                    return "NotConfirmed"
        await client.close_connection()
        return "NotFound"
