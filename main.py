import argparse
import asyncio
import datetime
from random import randint
from telethon import TelegramClient
from telethon import functions
from telethon.tl.types import UserStatusOnline, UserStatusOffline

parser = argparse.ArgumentParser(
                    prog='telegaonline',
                    description='The only one way to hide real status in Telegram - be online forever.',
                    epilog='The only way to protect ourselves is with a preemptive strike.')

parser.add_argument('-api_id')
parser.add_argument('-api_hash')

args = parser.parse_args()

client = TelegramClient('main', int(args.api_id), args.api_hash, receive_updates=False)


async def update_status(offline):
    await client(functions.account.UpdateStatusRequest(offline=offline))

    if offline:
        t = randint(4, 60 * 3)
    else:
        t = randint(9, 34)

    print(('Offline' if offline else 'Online') + f' {t} seconds..')

    await asyncio.sleep(t)


async def now_status():
    me = await client.get_me()
    status = me.status

    if type(status) == UserStatusOnline:
        expires = status.expires + datetime.timedelta(hours=3)
        return f'Now online, expires: {expires}'
    if type(status) == UserStatusOffline:
        was_online = status.was_online + datetime.timedelta(hours=3)
        return f'Now offline, last seen: {was_online}'

    return 'Unknown status'

async def main():
    while True:
        async with client:
            if client.is_connected():
                print(await now_status())
                await update_status(offline=False)
                await update_status(offline=True)

                continue

        await asyncio.sleep(5)


def stop():
    task.cancel()


task = client.loop.create_task(main())

try:
    client.loop.run_until_complete(task)
except asyncio.CancelledError:
    pass
