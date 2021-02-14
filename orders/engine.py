from collections import deque
from sortedcontainers import SortedList
from .models import Order,Trade
import threading
# from .signals import order_list

# class Order:

#     def __init__(self, id, order_type, side, price, quantity):
#         self.id = id
#         self.type = order_type
#         self.side = side.lower()
#         self.price = price
#         self.quantity = quantity

#     def __str__(self):
#         return "[" + str(self.price) + " for " + str(self.quantity) + " shares]"

# class Trade:

#     def __init__(self, buyer, seller, price, quantity):
#         self.buy_order_id = buyer
#         self.sell_order_id = seller
#         self.price = price
#         self.quantity = quantity

#     def show(self):
#         print("[", self.price, self.quantity, "]")

class OrderBook:

    def __init__(self, bids=[], asks=[]):
        self.bids = SortedList(bids, key = lambda order: -order.price)
        self.asks = SortedList(asks, key = lambda order: order.price)
        # self.lock = threading.Lock()

    def __len__(self):
        return len(self.bids) + len(self.asks)

    def best_bid(self):
        if len(self.bids) > 0:
            return self.bids[0].price
        else:
            return 1000000

    def best_ask(self):
        if len(self.asks) > 0:
            return self.asks[0].price
        else:
            return 0

    def add(self, order):
        if order.side == 'B':
            # index = self.bids.bisect_right(order)
            self.bids.add(order)
        elif order.side == 'S':
            # index = self.asks.bisect_right(order)
            self.asks.add(order)

    def remove(self, order):
        # with self.lock:
        # with threading.Lock():
        if order.side == 'B':
            # self.lock.acquire()
            self.bids.remove(order)
            # self.lock.release()
        elif order.side == 'S':
            # self.lock.acquire()
            self.asks.remove(order)
            # self.lock.release()

class MatchingEngine:

    def __init__(self, threaded=True):
        self.queue = deque()
        self.orderbook = OrderBook()
        self.trades = deque()
        self.threaded = threaded
        
        if self.threaded:
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def process(self, order):
        if self.threaded:
            self.queue.append(order)
        else:
            self.match_limit_order(order)

    def get_trades(self):
        trades = list(self.trades)
        return trades

    def match_limit_order(self, order):
        print('Inside match limit order func')
        if order.side == 'B' and order.price >= self.orderbook.best_ask():
            print('Inside B if')
            # Buy order crossed the spread
            filled = 0
            consumed_asks = []
            for i in range(len(self.orderbook.asks)):
                ask = self.orderbook.asks[i]

                if ask.price > order.price:
                    break # Price of ask is too high, stop filling order
                elif filled == order.quantity:
                    break # Order was filled

                if filled + ask.quantity <= order.quantity: # order not yet filled, ask will be consumed whole
                    filled += ask.quantity
                    # Trade(order.id, ask.id, ask.price, ask.quantity)
                    trade = Trade.objects.create(buyer=order.user,seller=ask.user,type=ask.type,price=order.price,quantity=ask.quantity,stock_code=order.stock_code)
                    self.trades.append(trade)
                    consumed_asks.append(ask)
                    if filled == order.quantity:
                        order.delete()

                elif filled + ask.quantity > order.quantity: # order is filled, ask will be consumed partially
                    volume = order.quantity-filled
                    filled += volume
                    trade = Trade.objects.create(buyer=order.user,seller=ask.user,type=ask.type,price=order.price,quantity=volume,stock_code=order.stock_code)
                    self.trades.append(trade)
                    ask.quantity -= volume
                    ask.save()
                    order.delete()

            for ask in consumed_asks:
                # with self.lock:
                # with threading.Lock():
                # self.lock.acquire()
                self.orderbook.remove(ask)
                ask.delete()
                # self.lock.release()

            if order:
                if filled < order.quantity:
                    # Order(order.id, "limit", order.side, order.price, order.quantity - filled)
                    order.quantity = order.quantity - filled
                    order.save()
                    self.orderbook.add(order)

        elif order.side == 'S' and order.price <= self.orderbook.best_bid():
            print('Inside S elif')
            # Sell order crossed the spread
            filled = 0
            consumed_bids = []
            for i in range(len(self.orderbook.bids)):
                bid = self.orderbook.bids[i]

                if bid.price < order.price:
                    break # Price of bid is too low, stop filling order
                if filled == order.quantity:
                    break # Order was filled

                if filled + bid.quantity <= order.quantity: # order not yet filled, bid will be consumed whole
                    filled += bid.quantity
                    trade = Trade.objects.create(buyer=bid.user,seller=order.user,type=bid.type,price=order.price,quantity=bid.quantity,stock_code=order.stock_code)
                    self.trades.append(trade)
                    consumed_bids.append(bid)
                    if filled == order.quantity:
                        order.delete()

                elif filled + bid.quantity > order.quantity: # order is filled, bid will be consumed partially
                    volume = order.quantity-filled
                    filled += volume
                    trade = Trade.objects.create(buyer=bid.user,seller=order.user,type=bid.type,price=order.price,quantity=volume,stock_code=order.stock_code)
                    self.trades.append(trade)
                    bid.quantity -= volume
                    bid.save()
                    order.delete()

            for bid in consumed_bids:
                # with self.lock:
                # with threading.Lock():
                # self.lock.acquire()
                self.orderbook.remove(bid)
                bid.delete()
                # self.lock.release()

            if order:
                if filled < order.quantity:
                    # Order(order.id, "limit", order.side, order.price, order.quantity-filled)
                    order.quantity = order.quantity - filled
                    order.save()
                    self.orderbook.add(order)

        else:
            print('Inside Else')
            # Order did not cross the spread, place in order book
            self.orderbook.add(order)

    def cancel_order(self, cancel):
        pass

    def run(self):
        while True:
            if len(self.queue) > 0:
                order = self.queue.popleft()
                self.match_limit_order(order)
                