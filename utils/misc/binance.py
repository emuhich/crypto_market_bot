from binance import AsyncClient

from utils.db_api.db_commands import get_binance_key


class Binance:

    @staticmethod
    async def get_client():
        api_key, api_secret = await get_binance_key()
        return await AsyncClient.create(api_key, api_secret)

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

