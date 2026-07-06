"""
    It receives a reference price and a size of order, and return the original price for which 
"""
class ExecutionModel: 
    def __init__(self,comission_rate:float, slippage_rate: float): 
        self.comission_rate = comission_rate
        self.slippage_rate = slippage_rate
    
    def execute(self,order_size: int, reference_price: float): 
        direction = 1 if order_size > 0 else -1 
        slipped_price = reference_price * (1 + direction * self.slippage_rate) #To apply the slippage so it does not benefit you never
        return slipped_price
    
    def commission_cost(self,order_size:int, fill_price:float) -> float: 
        notional = abs(order_size) * fill_price 
        return notional * self.comission_rate

    
