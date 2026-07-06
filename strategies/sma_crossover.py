from backtester.strategy import Strategy

class SMACrossover(Strategy): 
    def __init__(self, fast: int, slow:int): 
        self.fast = fast 
        self.slow = slow
    
    def generate_signal(self,data_so_far) -> int: 

        if len(data_so_far) < self.slow: 
            return 0 
        closes = data_so_far["Close"]

        fast_ma = closes.tail(self.fast).mean()
        slow_ma = closes.tail(self.slow).mean()

        if fast_ma > slow_ma: #Bullish tendency because the short mean have crossed the slow one indicating to buy. 
            return 1 
        else: 
            return 0 

