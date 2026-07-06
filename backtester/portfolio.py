""" 
It acts like the memory of the backtest. It does not decide anything, it does not calculate any prices. 
1. How much cash do you have. 
2. How many units of an active do you have. 
3. How much value everything in each moment
"""

class Portfolio: 
    def __init__(self,initial_cash:float): 
        self.cash = initial_cash
        self.position = 0 
        self.avg_entry_price = 0.0 
    
    def current_position(self): 
        """It just return the actual position"""
        return self.position
    
    def update_position(self,order_size:int,fill_price:float): 
        cost = order_size * fill_price
        self.cash -= cost 
        self.position += order_size
    
    def total_value(self, current_price:float) -> float: 
        market_value = self.position * current_price
        return self.cash + market_value
