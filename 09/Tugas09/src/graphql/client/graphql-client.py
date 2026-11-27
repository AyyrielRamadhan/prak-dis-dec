import asyncio
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

async def main():
    transport = AIOHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport)

    query = gql(
        """
        query getProduks {
            produks {
                id
                kode
                nama
                stok
                harga
                tersedia
            }
        }
        """
    )

    async with client as session:
        result = await session.execute(query)
        print(result)

asyncio.run(main())
