"""
Client class that communicates with a Continuous Double Auction exchange following the
Ouch Message Protocol
todo: Reconstruct on client side using built-in book class
client attributes: balance, orders, etc.
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
import uuid

from OuchServer.ouch_messages import OuchClientMessages, OuchServerMessages

p = configargparse.ArgParser()
p.add('--port', default=12345)
p.add('--host', default='127.0.0.1', help="Address of server")
p.add('--delay', default=0, type=float, help="Delay in seconds between sending messages")
p.add('--debug', action='store_true')
p.add('--time_in_force', default=99999, type=int)
options, args = p.parse_known_args()

DEFAULT_BALANCE = 100

class Client():
    def __init__(self, balance=None):
        self.reader = None
        self.writer = None
        self.balance = balance if balance else DEFAULT_BALANCE
        self.owned_shares = 0
        self.account_info = {"balance": self.balance, "owned_shares" : self.owned_shares}
        self.id = str(uuid.uuid4().hex).encode('ascii')

    def __str__(self):
        return (f"Account Information\n"
                f"Balance: {self.balance}\n"
                f"Owned_shares: {self.owned_shares}\n")
        
    def account_information(self):
        return self.account_info
    
    def _update_account(self, cost_per_share, num_shares):
        """update the state of account"""
        self.balance += (cost_per_share * num_shares)
        self.owned_shares += num_shares

    def _can_afford(self, cost_per_share, num_shares):
        """Can client create the order with their current balance?
        Args:
            cost_per_share: an int representing the price per share
            num_shares: an int representing the quantity of shares to buy
        Returns:
            A bool that specifies whether the client has the funds to make a buy
            num_shares at cost_per_share
        """
        return self.balance >= (cost_per_share * num_shares)
    
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

    async def recver(self):
        """Listener to all broadcasts sent from the exchange server"""
        if self.reader is None:
            reader, writer = await asyncio.streams.open_connection(
            options.host, 
            options.port)
            self.reader = reader
            self.writer = writer
        while not self.reader.at_eof():
            response = await self.recv()
            # Order from client was accepted
            if response.message_type == OuchServerMessages.Accepted:
                print("Accepted order: ", response, " With price : ", response['price'])
            # Order book has new best bid or ask(offer)
            # Ex:(ignoring quantity) buy {$2, $1} sell {}, if a client made a sell order of $1 then
            # the order book will update to buy {$1} sell {}, which means the new best bid is $1 and best ask is 0 
            if response.message_type == OuchServerMessages.BestBidAndOffer:
                print("new best buy offer: ", response)
            if response.message_type == OuchServerMessages.Executed:
                print("Executed: ", response)
            await asyncio.sleep(0)
        

    def _valid_order_input(self, quantity=None, price=None, direction=None, order_token=None):
        """Determine if valid parameters were entered
        Args:
            quantity: an expected int 
            price: an expected int 
            direction an expected str
            order_token an expected int
        Returns:
            False, if args are invalid
            tuple containing args in their respective formats
        """
        try:
            if quantity is not None:
                quantity = int(quantity)
                if quantity < 0:
                    return False
            
            if price is not None:
                price = int(price)
                if price < 1:
                    return False

            if direction is not None:
                if direction not in {'B', 'S'}:
                    return False

            if order_token is not None:
                order_token = int(order_token)
                if order_token < 1:
                    return False

            return (quantity, price, direction, order_token)
        except ValueError:
            return False

    async def send(self, request):
        """Send Ouch message to server"""
        if not request:
            print("Invalid order")
            return
        self.writer.write(bytes(request))
        await self.writer.drain()

    def place_order(self, quantity, price, direction, order_token):
        """Make an Ouch Limit order
        Args:
            quantity: an int representing number of shares for the order
            price: an int representing price to buy shares at
            direction: str that specifies whether the order is a BUY or SELL
            order_token: int that represents a unique order id

        Returns:
            None if order contains improper arguments
            Else return OuchClientMessages.EnterOrder
        """
        res = self._valid_order_input(quantity, price, direction, order_token)
        if not res:
            return None
    
        quantity, price, direction, order_token = res
        if direction == 'B':
            if not self._can_afford(price, quantity):
                return None
            self._update_account(-price, quantity)

        order_request = OuchClientMessages.EnterOrder(
                order_token=f'{order_token:014d}'.encode('ascii'),
                buy_sell_indicator=b'B' if direction == 'B' else b'S',
                shares=quantity,
                stock=b'AMAZGOOG',
                price=price,
                time_in_force=options.time_in_force,
                firm=bytes(self.id),
                display=b'N',
                capacity=b'O',
                intermarket_sweep_eligibility=b'N',
                minimum_quantity=1,
                cross_type=b'N',
                customer_type=b' ',
                midpoint_peg=b' ')
        return order_request

    def cancel_order(self, order_token, quantity_removed):
        """Convert user input into cancel order 
        Args:
            order_token: an int representing order id
            quantity_removed: an int representing how many shares to remove from the order
        
        Returns:
            None if order contains improper arguments
            Else return OuchClientMessages.CancelOrder
        """
        res = self._valid_order_input(order_token=order_token, quantity=quantity_removed)
        if not res:
            return None
    
        quantity_removed, price, direction, order_token = res
        cancel_request = OuchClientMessages.CancelOrder(
            order_token=f'{order_token:014d}'.encode('ascii'), 
            shares=quantity_removed,
        )
        return cancel_request



    async def sender(self):
        """
        Currently, this is where all Client send operations are called
        """
        if self.reader is None:
            reader, writer = await asyncio.streams.open_connection(
            options.host, 
            options.port)
            self.reader = reader
            self.writer = writer
        while True:
            print(self)
            cmd = input("Make a command order(O) or cancel(C): ")
            if cmd == "O":
                user_quantity = input("Enter number of shares: ")
                user_price = input("Enter share price: ")
                user_direction = input("Buy(B) or Sell(S): ")
                user_order_token = input("Order id: ")
                await self.send(self.place_order(user_quantity, user_price, user_direction, user_order_token))

            elif cmd == "C":
                user_order_token = input("ID of order to cancel: ")
                user_shares_removed = input("How many shares to remove: ")
                await self.send(self.cancel_order(user_order_token, user_shares_removed))
            else:
                print(f"Invalid command {cmd}")
            # sleeping will allow the client.recver() method to process
            await asyncio.sleep(0.5)
        
def main():
    log.basicConfig(level=log.INFO if not options.debug else log.DEBUG)
    log.debug(options)

    # creates a client and connects to our server
    client = Client()
    loop = asyncio.new_event_loop()
    asyncio.ensure_future(client.sender(), loop=loop)
    asyncio.ensure_future(client.recver(), loop=loop)
    

    try:
        loop.run_forever()       
    finally:
        loop.close()


if __name__ == '__main__':   
    main()