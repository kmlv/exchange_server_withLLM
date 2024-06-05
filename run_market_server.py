"""
Continuous Double Auction Server that handles clients' 
buy/sell and cancel orders
"""
import asyncio
import configargparse
import logging as log
from OuchServer.ouch_server import ProtocolMessageServer
from OuchServer.ouch_messages import OuchClientMessages, OuchServerMessages
from exchange.order_books.cda_book import CDABook
from exchange.order_books.fba_book import FBABook
from exchange.order_books.iex_book import IEXBook
from exchange.exchange import Exchange
from exchange.fba_exchange import FBAExchange
from exchange.iex_exchange import IEXExchange

p = configargparse.getArgParser()
# Used to set port and bind address for exchange
p.add('--port', default=8090)
p.add('--host', default='0.0.0.0', help="Address to bind to / listen on")
# Unused
p.add('--debug', action='store_true')
p.add('--logfile', default=None, type=str)
p.add('--inputlogfile', default=None, type=str)
p.add('--outputlogfile', default=None, type=str)
p.add('--book_log', default=None)
p.add('--mechanism', choices=['cda', 'fba', 'iex'], default = 'cda')
p.add('--interval', default = None, type=float, help="(FBA) Interval between batch auctions in seconds")
p.add('--delay', default = None, type=float, help="(IEX) 'speed bump' time that orders are delayed before being entered")
options, args = p.parse_known_args()


async def main():
    log.basicConfig(level=log.DEBUG if options.debug else log.INFO,
        format = "[%(asctime)s.%(msecs)03d] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt = '%H:%M:%S',
        filename = options.logfile)

    loop = asyncio.get_event_loop()
    server = ProtocolMessageServer(OuchClientMessages, options.host, options.port)
    
    if options.mechanism == 'cda':        
        book = CDABook()
        exchange = Exchange(order_book = book,
                            order_reply = server.send_server_response,
                            message_broadcast = server.broadcast_server_message,
                            loop = loop)
        
    # untested by 115b/c team
    elif options.mechanism == 'fba':
        book = FBABook()
        exchange = FBAExchange(order_book = book,
                            order_reply = server.send_server_response,
                            message_broadcast = server.broadcast_server_message,
                            loop = loop, 
                            interval = options.interval)
        exchange.start()
    # untested by 115b/c team
    elif options.mechanism == 'iex':
        book = IEXBook()
        exchange = IEXExchange(order_book = book,
                            order_reply = server.send_server_response,
                            message_broadcast = server.broadcast_server_message,
                            loop = loop,
                            delay = options.delay)
    
    server.register_listener(exchange.process_message)
    await server.start()

    try:
        await asyncio.get_running_loop().create_future()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    asyncio.run(main())
