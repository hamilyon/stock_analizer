"""
Agent is a class which allows to interact with a trading platform.
Agent can support any of following duck protocols.
Parameters like host, version, folder of a creating agent
get in __init__ method.


Authorization:
    login(user, password) : None or Exception
    logout() : None or Exception
    isconnected : bool

Market data:
    quotes(ticker) : tuple of tuples
    last(ticker) : Deal
    specification(ticker) : dict
    
Aggregated data:
g   daily(hid, start, end) : Bars generator
g   intraday(hid, start, end) : Bars generator
g   ticks(hid, start, end) : Deals generator
# Included FULL BARS ONLY in interval from start to end
    
Accounting and trading:
    place(account, order) : Order
    status(order) : str

Is not final ---
    accounts - read-only property  
    funds(account) - snapshot of funds
    portfolio(ticker) - read-only property
*   orders(accounts)
*   deals(accounts) - deals
Is not final ---

- - - - - - - - - - - - - - - - - - - - - - - - -
*   - request object. Can become to be more accurately.
g   - generator


IMMUTABLE OBJECTS: Bar, Deal, Account, Order, 
Order returns not real Order! It returns PartialOrderBuilder ;)
Real Order is immutable.

class PartialOrderBuilder():
    def __init__(self, ... like in Order ...):
        self.order = None # When order will set object will be locked!
    def associate(self, order):
        self.order = order
    def __getattr__(self, attr):
        if self.order:
            return getattr(self.order, attr)
        return super().__getattr__(self, attr)


Order prototype:

Order is IMMUTABLE!!! Status stores and changes in agent!
class Order(object):
    def __init__(ticker, quantity, price=None, executewhen=None, cancelwhen=None)
        #executewhen or cancelwhen: grather, lesser, timeout # One or tuple
        pass



Usage sample:
ag = Agent()
agent.login("user", "pass")
acc = agent.accounts[0]

if funds(acc).available > 1000:
    ord = agent.place(acc, Order(ticker, 10))

while ord.isactive:
    pass # Wait while order is active


"""

