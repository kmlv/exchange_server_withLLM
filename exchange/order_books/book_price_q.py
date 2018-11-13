import logging as log
from collections import OrderedDict
import pdb



class BookPriceQ:
	def __init__(self, price):
		self.interest = 0 	#sum of interest at this price
		self.order_q = OrderedDict()
		self.price = price
	
	def __str__(self):
		return '${} Interest: {}, Orders: {}'.format(self.price, self.interest, ', '.join(['{}: {}'.format(id, volume) for (id, volume) in self.order_q.items()]))

	def add_order(self, order_id, volume):
		self.interest += volume
		self.order_q[order_id] = volume

	def cancel_order(self, order_id):
		self.interest -= self.order_q[order_id]
		del self.order_q[order_id]

	def reduce_order(self, order_id, new_volume):
		volume = self.order_q[order_id]
		assert new_volume < volume
		self.order_q[order_id] = new_volume
		self.interest -= (volume - new_volume)

	def fill_order(self, volume):
		'''
		For a given order volume to fill, dequeue's the oldest orders 
		at this price point to be used to fill the order. 

		Returns a tuple giving the volume filled at this price, and a list of (order_id, order_volume) pairs giving the order volume amount filled from each order in the book.
		'''
		volume_to_fill = volume
		fulfilling_orders = []
		while volume_to_fill > 0 and len(self.order_q)>0:
			log.debug('  fill_order: volume_to_fill = %s', volume_to_fill)
			next_order_id = next(iter(self.order_q))
			next_order_volume = self.order_q[next_order_id]
			if next_order_volume > volume_to_fill:
				assert self.order_q[next_order_id] ==next_order_volume
				self.order_q[next_order_id] = next_order_volume-volume_to_fill
				fulfilling_orders.append((next_order_id, volume_to_fill))
				self.interest -= volume_to_fill	
				volume_to_fill = 0			
			else:
				volume_to_fill -= next_order_volume
				fulfilling_orders.append(self.order_q.popitem(last=False))
				self.interest -= next_order_volume
		return (volume - volume_to_fill, fulfilling_orders)

class IEXBookPriceQ(BookPriceQ):
	def __init__(self, price, buy_sell_indicator, lit=False):
		super().__init__(price)
		self.side = buy_sell_indicator
		self.lit = lit

	def add_order(self, order_id, volume):
		self.interest += volume
		self.order_q[order_id] = volume

	def cancel_order(self, order_id):
		self.interest -= self.order_q[order_id]
		del self.order_q[order_id]

	def fill_order(self, volume):
		'''
		I have to know whether all volume on 
		order id is drained, so I can remove from pegs.
		'''
		volume_to_fill = volume
		fulfilling_orders = []
		drained_orders = []
		while volume_to_fill > 0 and len(self.order_q)>0:
			log.debug('  fill_order: volume_to_fill = %s', volume_to_fill)
			next_order_id = next(iter(self.order_q))
			next_order_volume = self.order_q[next_order_id]
			if next_order_volume > volume_to_fill:
				assert self.order_q[next_order_id] ==next_order_volume
				self.order_q[next_order_id] = next_order_volume-volume_to_fill
				fulfilling_orders.append((next_order_id, volume_to_fill))
				self.interest -= volume_to_fill	
				volume_to_fill = 0			
			else:
				volume_to_fill -= next_order_volume
				drained_order_id = self.order_q.popitem(last=False)
				fulfilling_orders.append(drained_order_id)
				drained_orders.append(drained_order_id) 
				self.interest -= next_order_volume
		return (volume - volume_to_fill, fulfilling_orders, drained_orders) 
	
	def __str__(self):
		return '	${} Interest: {}, Lit: {}, Orders: {}'.format(self.price, 
			self.interest, self.lit, ', '.join([
				'{}: {}'.format(id, volume) for (id, volume) in self.order_q.items()]
				))
