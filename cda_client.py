"""(1)Implement logic such that clients can decide when to make an order or when to cancel
""" 
import sys
import asyncio
import asyncio.streams
import configargparse
import logging as log
# import binascii
from random import randrange, randint
import itertools
from openai import OpenAI

from OuchServer.ouch_messages import OuchClientMessages, OuchServerMessages

p = configargparse.ArgParser()
p.add('--port', default=12345)
p.add('--host', default='127.0.0.1', help="Address of server")
p.add('--delay', default=0, type=float, help="Delay in seconds between sending messages")
p.add('--debug', action='store_true')
p.add('--time_in_force', default=99999, type=int)
options, args = p.parse_known_args()

def rounduprounddown(i, minlimit, maxlimit, roundeddown, roundedup):
    if i<minlimit:
        return roundeddown
    elif i>maxlimit:
        return roundedup
    else: 
        return i


class Client():
    def __init__(self):
        self.reader = None
        self.writer = None

    async def recv(self):
        try:
            header = (await self.reader.readexactly(1))
        except asyncio.IncompleteReadError:
            log.error('connection terminated without response')
            return None
        log.debug('Received Ouch header as binary: %r', header)
        log.debug('bytes: %r', list(header))
        message_type = OuchServerMessages.lookup_by_header_bytes(header)
        try:
            payload = (await self.reader.readexactly(message_type.payload_size))
        except asyncio.IncompleteReadError as err:
            log.error('Connection terminated mid-packet!')
            return None
        log.debug('Received Ouch payload as binary: %r', payload)
        log.debug('bytes: %r', list(payload))

        response_msg = message_type.from_bytes(payload, header=False)
        return response_msg

    async def recver(self):
        if self.reader is None:
            reader, writer = await asyncio.streams.open_connection(
            options.host, 
            options.port)
            self.reader = reader
            self.writer = writer
        index = 0
        while True:
            response = await self.recv()
            index += 1 
            while not self.reader.at_eof():
                response = await self.recv()
                index += 1
                if index % 1000==0:
                    print('received {} messages'.format(index))
            await asyncio.sleep(0.0000001)
            if index % 1000==0:
                print('received {} messages'.format(index))
            #log.info('Received msg %s', response)
            #response = await recv()
            print('recv message: ', response)
            #log.debug("Received response Ouch message: %s", response)

    async def send(self, request):
        if not request:
            return
        self.writer.write(bytes(request))
        await self.writer.drain()

    def place_order(self):
        order_token = int(input("Enter order token: "))
        direction = input("Enter 'B' for buy or 'S' for sell: ")
        if direction != 'B' and direction != 'S':
            return None
        price = int(input("Enter price per share: "))
        quantity = int(input("Enter number of shares: "))
        return self._handle_order(quantity, price, direction, order_token)

    def cancel_order(self):
        order_token = int(input("Enter order token: "))
        quantity_removed = int(input("Enter number of shares to remove: "))
        return self._handle_cancel(order_token, quantity_removed)

    def _handle_order(self, quantity, price, direction, order_token):
        order_request = OuchClientMessages.EnterOrder(
                order_token=f'{order_token:014d}'.encode('ascii'),
                buy_sell_indicator=b'B' if direction == 'B' else b'S',
                shares=quantity,#randrange(1,10**6-1),
                stock=b'AMAZGOOG',
                price=price,#rounduprounddown(randrange(1,100), 40, 60, 0, 2147483647 ),
                time_in_force=options.time_in_force,
                firm=b'OUCH',
                display=b'N',
                capacity=b'O',
                intermarket_sweep_eligibility=b'N',
                minimum_quantity=1,
                cross_type=b'N',
                customer_type=b' ',
                midpoint_peg=b' ')
        return order_request

    def _handle_cancel(self, order_token, quantity_removed):
        """Convert user input into cancel order """
        cancel_request = OuchClientMessages.CancelOrder(
            order_token=f'{order_token:014d}'.encode('ascii'), 
            shares=quantity_removed,
        )
        return cancel_request

    async def sender(self):
        if self.reader is None:
            reader, writer = await asyncio.streams.open_connection(
            options.host, 
            options.port)
            self.reader = reader
            self.writer = writer
        while True:
            cmd = input("Make a command: ")
            if cmd == "order":
                await self.send(self.place_order())
            elif cmd == "cancel":
                await self.send(self.cancel_order())
            else:
                print(f"Invalid command {cmd}")
        

    async def start(self):
        reader, writer = await asyncio.streams.open_connection(
            options.host, 
            options.port)
        self.reader = reader
        self.writer = writer
        await self.sender()
        writer.close()
        await asyncio.sleep(0.5)


def main():

    log.basicConfig(level=log.INFO if not options.debug else log.DEBUG)
    log.debug(options)

    client = Client()
    loop = asyncio.new_event_loop()
    # creates a client and connects to our server
    asyncio.ensure_future(client.sender(), loop = loop)
    asyncio.ensure_future(client.recver(), loop = loop)

    try:
        loop.run_forever()       
    finally:
        loop.close()

if __name__ == '__main__':
    # client = OpenAI()
    # userinput = input("enter prompt for openai: ")
    # completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "Market Assistant"},
    #         {"role": "user", "content": userinput}
    #     ],
    # )

    # print(completion.choices[0].message)
    
    main()