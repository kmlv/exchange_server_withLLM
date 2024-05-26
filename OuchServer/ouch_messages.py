# https://nasdaqtrader.com/content/technicalsupport/specifications/TradingProducts/OUCH4.2.pdf
from .protocol_message_primitives import *
#https://www.borsaistanbul.com/files/bistech-itch-protocol-specification.pdf
#https://nasdaqtrader.com/content/technicalsupport/specifications/TradingProducts/OUCH4.2.pdf
class OuchFields(ProtocolFieldEnum):
    """Fields for OuchMessages
    Tuples have the meaning
    <field_name> = (datatype, description)
    datatype:
        'c': 1 character
        'I': Integer
        '8s': string with 8 bits
        '4s': string with 4 bits

    Notes: Ouch messages can only contain these information fields.
        So if you want to add new fields, follow the aformentioned style.
    """
    msg_type = ('c', 'Identifies the type of this message')
    order_token = ('32s', 'todo')
    buy_sell_indicator = ('c', 'todo')
    shares = ('I', 'todo')
    stock = ('8s', 'todo')
    price = ('I', 'todo')
    time_in_force = ('I', 'todo')
    firm = ('4s', 'todo')
    display = ('c', 'todo')
    capacity= ('c', 'todo')
    intermarket_sweep_eligibility = ('c', 'todo')
    minimum_quantity = ('I', 'todo')
    cross_type = ('c', 'todo')
    replacement_order_token = ('14s', 'todo')
    # client message only
    customer_type = ('c', 'todo')
    existing_order_token = ('14s', 'todo')
    # server messages only
    timestamp = ('Q', 'todo')
    event_code = ('c', 'todo')
    order_reference_number = ('Q', 'todo')
    order_state = ('c', 'todo')
    bbo_weight_indicator = ('c', 'todo')
    previous_order_token = ('14s', 'todo')
    decrement_shares = ('I', 'todo')
    reason = ('8s', 'todo')
    quantity_prevented_from_trading = ('I', 'todo')
    execution_price = ('I', 'todo')
    liquidity_flag = ('c', 'todo')
    executed_shares = ('I', 'todo')
    match_number = ('Q', 'todo')
    reference_price = ('I', 'todo')
    reference_price_type = ('c', 'todo')
    leeps_timestamp = ('16s', 'todo')
    # custom quotation message fields
    best_bid = ('I', 'the best bid')
    best_ask = ('I', 'the best ask')
    volume_at_best_bid = ('I', 'todo')
    volume_at_best_ask = ('I', 'todo')
    next_bid = ('I', 'todo')
    next_ask = ('I', 'todo')
    # fields for fb auction post batch msg
    clearing_price = ('I', 'todo')
    transacted_volume = ('I', 'todo')
    # external best bid and offer, for midpoint peg updates
    e_best_bid = ('I', 'todo')
    e_best_offer = ('I', 'todo')
    # boolean for pegged orders
    midpoint_peg = ('?', 'todo')
    # fields for peg state update message
    peg_state = ('i', 'todo')
    peg_price = ('I', 'todo')


class OuchHeader(NamedFieldSequence):
    __slots__ = ('msg_type',)
    _protocol_fields = OuchFields
    
    def __str__(self):
        return self.msg_type.decode('ASCII')


class OuchPayloadBase(NamedFieldSequence):
    __slots__ = ()
    _protocol_fields = OuchFields
    _display_fmt = None

    def __str__(self):
        if self._display_fmt is None:
            return super().__str__()
        else:
            return self._display_fmt.format_map(
                {k: (s.decode('ASCII') if isinstance(s, bytes) else s)
                 for (k, s) in self.iteritems()}
            )

class OuchMessage(ProtocolMessage):
    _HeaderCls = OuchHeader
    _PayloadBaseCls = OuchPayloadBase
    
class OuchMessageTypeSpec(MessageTypeSpec):
    _MessageCls = OuchMessage
 
    def __init__(self, display_fmt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if display_fmt is not None:
            self._PayloadCls._display_fmt = display_fmt

LookupByHeaderBytesMixin = create_attr_lookup_mixin(
    'LookupByHeaderBytesMixin_ClientMsgs', 'header_bytes')
class OuchClientMessages(LookupByHeaderBytesMixin, OuchMessageTypeSpec,
                         DuplicateFreeEnum):
    """Datatype representing messages sent from clients"""
    EnterOrder = ('{order_token}:{buy_sell_indicator}{shares}x{stock}@{price}',
            {'msg_type': b'O'},
            ['order_token', 'buy_sell_indicator', 'shares', 'stock',
             'price', 'time_in_force', 'firm', 'display', 'capacity',
             'intermarket_sweep_eligibility', 'minimum_quantity',
             'cross_type', 'customer_type', 'midpoint_peg']
        )
    ReplaceOrder = ('{existing_order_token}->{replacement_order_token}:{shares}@{price}',
            {'msg_type': b'U'},
            ['existing_order_token', 'replacement_order_token',
             'shares', 'price', 'time_in_force', 'display',
             'intermarket_sweep_eligibility', 'minimum_quantity']
        )
    CancelOrder = ('{order_token}:{shares}',
            {'msg_type': b'X'},
            ['order_token', 'shares']
        )
    # used in exchange.py but not fully implemented
    ModifyOrder = ('{order_token}:{buy_sell_indicator}x{shares}',
            {'msg_type': b'M'},
            ['order_token', 'buy_sell_indicator', 'shares']
        )
    # unused
    TradeNow = ('{order_token}',
            {'msg_type': b'N'},
            ['order_token']
        )
    SystemStart = ('{timestamp}:{event_code}',          #jason
            {'msg_type': b'H'},
            ['timestamp', 'event_code']
        )
    # used in iex_exchange
    ExternalFeedChange = ('{e_best_bid}:{e_best_offer}',
            {'msg_type': b'K'},
            ['e_best_bid', 'e_best_offer']
        )


LookupByHeaderBytesMixin = create_attr_lookup_mixin(
    'LookupByHeaderBytesMixin_ServerMsgs', 'header_bytes')
class OuchServerMessages(LookupByHeaderBytesMixin, OuchMessageTypeSpec,
                         DuplicateFreeEnum):
    """Datatype representing messages sent from an Exchange"""
    SystemEvent = ('{timestamp}:{event_code}',
            {'msg_type': b'S'},
            ['timestamp', 'event_code']
        )
    Accepted = ('{timestamp}:{order_token}({order_reference_number}):{buy_sell_indicator}{shares}x{stock}@{price}',
            {'msg_type': b'A'},
            ['timestamp', 'order_token', 'buy_sell_indicator', 'shares',
             'stock', 'price', 'time_in_force', 'firm', 'display',
             'order_reference_number', 'capacity',
             'intermarket_sweep_eligibility', 'minimum_quantity',
             'cross_type', 'order_state', 'bbo_weight_indicator', 'midpoint_peg']
        )
    Replaced = ('{timestamp}:{replacement_order_token}({order_reference_number}):{buy_sell_indicator}{shares}x{stock}@{price}',
            {'msg_type': b'U'},
            ['timestamp', 'replacement_order_token',
             'buy_sell_indicator', 'shares', 'stock', 'price',
             'time_in_force', 'firm', 'display', 'order_reference_number',
             'capacity', 'intermarket_sweep_eligibility',
             'minimum_quantity', 'cross_type', 'order_state',
             'previous_order_token', 'bbo_weight_indicator', 'midpoint_peg']
        )
    Canceled = ('{timestamp}:{order_token}:-{decrement_shares}({reason})',
            {'msg_type': b'C'},
            ['timestamp', 'order_token', 'decrement_shares', 'reason', 'midpoint_peg', 'price', 'buy_sell_indicator']
        )
    # unused
    AIQCanceled = ('{timestamp}:{order_token}:-{decrement_shares}({reason})',
            {'msg_type': b'D'},
            ['timestamp', 'order_token', 'decrement_shares', 'reason',
             'quantity_prevented_from_trading', 'execution_price',
             'liquidity_flag']
        )
    Executed = ('{timestamp}:{order_token}m{match_number}:{executed_shares}@{execution_price}',
            {'msg_type': b'E'},
            ['timestamp', 'order_token', 'executed_shares',
             'execution_price', 'liquidity_flag', 'match_number', 'midpoint_peg']
        )

    BestBidAndOffer = ('{timestamp}:{stock}:bid:{volume_at_best_bid}@{best_bid}:ask:{volume_at_best_ask}@{best_ask}',
            {'msg_type': b'Q'},
            ['timestamp', 'stock', 'best_bid', 'volume_at_best_bid', 'best_ask', 
             'volume_at_best_ask', 'next_bid', 'next_ask']
        )
    # used in fba_exchange.py
    PostBatch = ('{timestamp}:{stock}:{clearing_price}:{transacted_volume}:\
{best_bid}:{volume_at_best_bid}:{best_ask}:{volume_at_best_ask}:{next_bid}:{next_ask}',
            {'msg_type': b'Z'},
            ['timestamp', 'stock', 'clearing_price', 'transacted_volume',
             'best_bid', 'volume_at_best_bid', 'volume_at_best_ask', 'best_ask', 
             'next_bid', 'next_ask']
        )
    # used in iex_exchange.py
    PegStateUpdate = ('{timestamp}:{peg_state}:{peg_price}',
            {'msg_type': b'L'},
            ['timestamp', 'peg_state', 'peg_price']
        )
    # unused
    BrokenTrade = ('{timestamp}:XX{order_token}m{match_number}({reason})',
            {'msg_type': b'B'},
            ['timestamp', 'order_token', 'match_number', 'reason']
        )
    # unused
    ExecutedWithReferencePrice = ('{timestamp}:{order_token}m{match_number}:{executed_shares}@{execution_price}',
            {'msg_type': b'G'},
            ['timestamp', 'order_token', 'executed_shares',
             'execution_price', 'liquidity_flag', 'match_number',
             'reference_price', 'reference_price_type']
        )
    # unused
    TradeCorrection = ('{timestamp}:{order_token}m{match_number}:{executed_shares}@{execution_price}({reason})',
            {'msg_type': b'F'},
            ['timestamp', 'order_token', 'executed_shares',
             'execution_price', 'liquidity_flag', 'match_number',
             'reason']
        )
    Rejected = ('{timestamp}:{order_token}({reason})',
            {'msg_type': b'J'},
            ['timestamp', 'order_token', 'reason', 'shares', 'price']
        )
    # unused
    CancelPending = ('{timestamp}:{order_token}',
            {'msg_type': b'P'},
            ['timestamp', 'order_token']
        )
    # unused
    CancelReject = ('{timestamp}:{order_token}',
            {'msg_type': b'I'},
            ['timestamp', 'order_token']
        )
    # unused
    OrderPriorityUpdate = ('{timestamp}:{order_token}({order_reference_number}):{price}',
            {'msg_type': b'T'},
            ['timestamp', 'order_token', 'price', 'display',
             'order_reference_number']
        )
    # unused
    OrderModified = ('{timestamp}:{order_token}:{buy_sell_indicator}{shares}',
            {'msg_type': b'M'},
            ['timestamp', 'order_token', 'buy_sell_indicator', 'shares']
        )
    # unused
    TradeNow = ('{timestamp}:{order_token}',
            {'msg_type': b'N'},
            ['timestamp', 'order_token']
        )
