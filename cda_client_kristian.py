"""
Client class that communicates with a Continuous Double Auction exchange following the
Ouch Message Protocol
todo: Reconstruct on client side using built-in book class
client attributes: balance, orders, etc.
Feel free to use this as a reference for any future additions
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


class Client():
    def __init__(self):
        self.reader = None
        self.writer = None

    def _order_direction_condition(self, user_input):
        """Order direction must be 'B' or 'S'
        Arg: string containing user input that specifies order direction

        Return: boolean that describes whether the user entered a valid direction
        """
        if user_input == "B" or user_input == "S":
            return True
        print(f"Invalid direction {user_input}")
        return False


    def _validate_user_input(self, prompt, expected_type, conditions=None):
        """Check that user input matches specified type
        
        Args: 
            prompt: A string displayed to the user
            expected_type: A builtin or custom class type specifier
            conditions: any additional conditions associated with the prompt and type
        Returns: value of expected_type from user input

        (Ex):  user_int = validate_user_input("Enter a price: ",int()) 
            Asks for another input if the user enters anything other than an int
        (Ex2): user_direction = validate_user_input("Enter a direction: ",str(), self._order_direction_condition)
            Similar to previous example but with added conditions. In this case the user must enter 'B' or 'S'.
        """
        while True:
            try:
                valid_input = None
                if isinstance(expected_type, int):
                    valid_input = int(input(prompt))
                if isinstance(expected_type, str):
                    valid_input = input(prompt)
                if isinstance(expected_type, float):
                    valid_input = float(input(prompt))
                # Conditions present
                if conditions:
                    res = conditions(valid_input)
                    # Conditions not met user needs to enter valid input
                    if not res:
                        continue
                # Valid input was entered
                return valid_input
            except ValueError:
                print(f"Received {type(input)}, Expected {type(expected_type)}")

    def _user_order_input(self):
        """USED FOR CODE TESTING get needed input from terminal to make an order
        
        returns: Tuple(order token:int, order direction: str, shares: int,price: int)
        """
        return (
            self._validate_user_input("Order Token: ", int()),
            self._validate_user_input("Buy(B) or Sell(S): ", str(), self._order_direction_condition),
            1,
            self._validate_user_input("Enter a price: ", int()),
        )

    async def recv(self):
        """Convert response from bytes into ouch response format
        
        Returns: OuchServer.ouch_message object in the format of one of the many formats
        (found in Lines past 134 in OuchServer\ouch_messages.py):
        """
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

    # NOTE: Unused and unsure if it is needed for anything - Kristian M.
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
        """Send Ouch message to server"""
        self.writer.write(bytes(request))
        await self.writer.drain()

    def _handle_order(self, new_order_token : int, direction : str,  shares: int , price : int):
        """Convert Limit Order into Ouch order
        args:
            new_order_token: int that represents order id
            direction: string that represents whether the order is buy or sell
            shares: int that represents quantity of an order
            price: int that represents price to buy the stock at
        return:
            Ouchmessage in the form of an order
        """
        order_request = OuchClientMessages.EnterOrder(
                order_token=f'{new_order_token:014d}'.encode('ascii'),
                buy_sell_indicator=b'B' if direction == 'B' else b'S',
                shares=shares,
                stock=b'AMAZGOOG',
                price=price,
                time_in_force=options.time_in_force,
                firm=b'OUCH',
                display=b'N',
                capacity=b'O',
                intermarket_sweep_eligibility=b'N',
                minimum_quantity=1,
                cross_type=b'N',
                customer_type=b' ',
                midpoint_peg=b' ',
                client_id=b'10')
        return order_request
        
    def _handle_cancel(self):
        """Convert user input into cancel order """
        cancel_request = OuchClientMessages.CancelOrder(
            order_token=f'{self._validate_user_input("Order Token to Cancel: ", int()):014d}'.encode('ascii'), 
            shares=1,
        )
        return cancel_request
    async def sender(self):
        """"""
        if self.reader is None:
            reader, writer = await asyncio.streams.open_connection(
            options.host, 
            options.port)
            self.reader = reader
            self.writer = writer
        while True:
            response = None
            cmd = input("Make a command: ")
            if cmd == "order":
                await self.send(self._handle_order(*self._user_order_input()))
                response = await self.recv()
            elif cmd == "cancel":
                await self.send(self._handle_cancel())
                response = await self.recv()
            else:
                print(f"Invalid command {cmd}")
                continue
            print(f"Server response: {response}, {type(response)}")
def main():
    log.basicConfig(level=log.INFO if not options.debug else log.DEBUG)
    log.debug(options)
    # creates a client and connects to our server
    client = Client()
    loop = asyncio.new_event_loop()
   
    asyncio.ensure_future(client.sender(), loop = loop)

    try:
        loop.run_forever()       
    finally:
        loop.close()


if __name__ == '__main__':   
    main()