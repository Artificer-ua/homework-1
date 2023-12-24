import argparse
import asyncio
import json
import logging
from datetime import date, datetime, timedelta
from pathlib import Path

import aiohttp
import names
import websockets
from aiofile import async_open
from websockets import ConnectionClosed, WebSocketServerProtocol

"""
Works...but smells a little.
"""

BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?date="
TODAY = date.today().strftime("%d.%m.%Y")
YESTERDAY = (date.today() - timedelta(days=1)).strftime("%d.%m.%Y")
MAX_DAYS = 10

LOG_FILENAME = "exchange.log"
LOG_STORAGE = "storage"
BASE_DIR = Path()

"""
This two lists should be refactored and make by parsing PB json at start...one day.
"""
BASIC_CURRENCY = ["USD", "EUR"]
ALL_CURRENCY = [
    "AUD",
    "AZN",
    "BYN",
    "CAD",
    "CHF",
    "CNY",
    "CZK",
    "DKK",
    "EUR",
    "GBP",
    "GEL",
    "HUF",
    "ILS",
    "JPY",
    "KZT",
    "MDL",
    "NOK",
    "PLN",
    "SEK",
    "SGD",
    "TMT",
    "TRY",
    "UAH",
    "USD",
    "UZS",
    "XAU",
]
NB_CURRENCY = [
    "AUD",
    "AZN",
    "BYN",
    "CAD",
    "CNY",
    "DKK",
    "GEL",
    "HUF",
    "ILS",
    "JPY",
    "KZT",
    "MDL",
    "NOK",
    "SEK",
    "SGD",
    "TMT",
    "TRY",
    "UAH",
    "UZS",
    "XAU",
]

"""
--days [-d] <number of days>
--currency [-c] CHF GBP PLZ SEK XAU CAD etc..
"""

parser = argparse.ArgumentParser(
    prog="Exchange helper bot",
    description="App for getting exchange rates",
    epilog="Thanks for using",
)
parser.add_argument(
    "--days",
    "-d",
    help="Currency history for X days",
    default="1",
    type=int,
    required=False,
)
parser.add_argument(
    "--currency", "-c", nargs="+", help=f"Additional currency: {str(ALL_CURRENCY)}"
)

args = vars(parser.parse_args())  # object -> dict

days_input = args.get("days")
currency_input = []
currency_input.extend(BASIC_CURRENCY)
if args.get("currency") is not None:
    currency_input.extend(args.get("currency"))

logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.INFO,
    handlers=[
        # logging.FileHandler("exchange.log"),
        logging.StreamHandler()
    ],
)


async def file_logging(log_msg: str) -> None:
    async with async_open(
        BASE_DIR.joinpath(LOG_STORAGE + "/" + LOG_FILENAME), "a", encoding="utf-8"
    ) as fh:
        await fh.write(log_msg)


async def currency_filter(currency: list, ex_rate: dict) -> dict:
    result_dict = {}
    for curr in currency:
        if curr not in ALL_CURRENCY or ex_rate == []:
            result_dict[curr] = {"sale": "Not found", "purchase": "Not found"}
        elif curr not in NB_CURRENCY:
            exchange, *_ = list(filter(lambda el: el["currency"] == curr, ex_rate))
            result_dict[curr] = {
                "sale": exchange["saleRate"],
                "purchase": exchange["purchaseRate"],
            }
        else:
            exchange, *_ = list(filter(lambda el: el["currency"] == curr, ex_rate))
            result_dict[curr] = {
                "sale": exchange["saleRateNB"],
                "purchase": exchange["purchaseRateNB"],
            }
    return result_dict


async def get_exchange(url: str, days=1) -> list:
    logging.debug(f"get_exchange: days = {days}")
    result = []
    if days == 1:
        logging.info(f"Waiting for exchange rates for {days} day.")
        res = await request_function(url + TODAY)
        ex_rate = res.get("exchangeRate")
        if len(ex_rate) == 0:
            logging.debug("Yesterday exchange")
            res = await request_function(url + YESTERDAY)
            ex_rate = res.get("exchangeRate")
            result.append(
                {
                    "Exchange rate for today not found. Using yesterday date: "
                    + str(YESTERDAY): await currency_filter(currency_input, ex_rate)
                }
            )
        result.append({TODAY: await currency_filter(currency_input, ex_rate)})
    else:
        for day in range(0, int(days)):
            logging.info(f"Waiting for exchange rates for {int(days)-day} days.")
            res = await request_function(
                url + (date.today() - timedelta(days=int(day))).strftime("%d.%m.%Y")
            )
            ex_rate = res.get("exchangeRate")
            result.append(
                {
                    (date.today() - timedelta(days=int(day))).strftime(
                        "%d.%m.%Y"
                    ): await currency_filter(currency_input, ex_rate)
                }
            )
    return result


async def request_function(url: str) -> None:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    req = await response.json()
                    return req
                logging.error(f"Error status {response.status} for {url}")
        except aiohttp.ClientConnectorError as e:
            logging.error(f"Connection error {e}")
        return None


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        await self.send_to_clients("Hello, I'm new user!", ws)
        logging.debug(f"{ws.remote_address} is connected")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        await self.send_to_clients(f"Goodbye {ws.name}.", ws)
        logging.debug(f"{ws.remote_address} was disconnected")

    async def send_to_clients(self, message: str, ws: WebSocketServerProtocol):
        if self.clients:
            [await client.send(f"{ws.name}: " + message) for client in self.clients]

    async def send_to_defined_client(
        self, message: str | dict, ws: WebSocketServerProtocol
    ):
        if isinstance(message, str):
            await ws.send("Private message: " + message)
        elif isinstance(message, list):
            for item in message:
                for day, value in item.items():
                    [
                        await ws.send(
                            "Private message: " + str(day) + f" |{currency}| "
                            "Sale - "
                            + str(value[currency].get("sale"))
                            + " Buy: "
                            + str(value[currency].get("purchase"))
                        )
                        for currency in value.keys()
                    ]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosed:
            pass
        finally:
            await self.unregister(ws)

    async def parse_command(self, message: str, ws: WebSocketServerProtocol):
        if message.lower() == "exchange":
            days = 1
        else:
            try:
                command, days = message.split(" ")[0:2]
                match command.lower():
                    case "exchange":
                        if not days.isdigit():
                            return f"Bad argument of {command}: {days}"
                        if int(days) > MAX_DAYS:
                            days = MAX_DAYS
                        elif int(days) < 1:
                            days = 1
                    case _:
                        return message
            except ValueError as e:
                logging.debug(f"{e}, return message")
                return message
            # call here exchange function with default parameters
        r = await get_exchange(url=BASE_URL, days=days)
        logging.info("Exchange rates was got successfully.")
        # write some log to file
        await file_logging(
            f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}: Exchange command was used by {ws.name}\n"
        )
        return r

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            r = await self.parse_command(message, ws)
            if r == message:
                await self.send_to_clients(r, ws)
            else:
                await self.send_to_defined_client(r, ws)


async def main():
    server = Server()
    console_exchange_rate = await get_exchange(url=BASE_URL, days=days_input)
    print(json.dumps(console_exchange_rate, sort_keys=False, indent=5))
    async with websockets.serve(server.ws_handler, "localhost", 8080):
        await asyncio.Future()


if __name__ == "__main__":
    if not BASE_DIR.joinpath(LOG_STORAGE).exists():
        BASE_DIR.joinpath(LOG_STORAGE).mkdir(exist_ok=True)
    asyncio.run(main())
