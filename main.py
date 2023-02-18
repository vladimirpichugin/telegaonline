import argparse
import asyncio
from random import randint
from telethon import TelegramClient
from telethon import functions

parser = argparse.ArgumentParser(
                    prog='telegaonline',
                    description='The only one way to hide real status in Telegram - be online forever.',
                    epilog='The only way to protect ourselves is with a preemptive strike.')

parser.add_argument('-api_id')
parser.add_argument('-api_hash')

args = parser.parse_args()

client = TelegramClient('main', int(args.api_id), args.api_hash, receive_updates=False)


async def main():
    while True:
        async with client:
            if client.is_connected():
                await client(functions.account.UpdateStatusRequest(offline=False))

        t = randint(5, 180)

        print(f'Sleep {t} seconds..')

        await asyncio.sleep(t)


def stop():
    task.cancel()


task = client.loop.create_task(main())

try:
    client.loop.run_until_complete(task)
except asyncio.CancelledError:
    pass
