from backtester.strategy import Strategy

class BuyAndHold(Strategy): 
    def generate_signal(self, data_so_far):
        return 1