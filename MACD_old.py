class StrategyMACD_old(SignalStrategy):
    #optimize parameter
    
    #15min 24,20
    RSIperiod = 24
    RSICloseUpTrigger = 70
    RSICloseDownTrigger = 20
    RSIOpenTrigger = 50
    
    
    def init(self):
        super().init()
        
        #get strategy data
        df = self.getDf()
        # cache to class for signal
        self.high = df['high']
        self.low = df['low']
        self.open = df['open']
        self.close = df['close']
        df['preClose'] = df['close'].shift(periods=1)
        
        #EMA
        df['EMA5'] = talib.EMA(self.close, timeperiod=5)
        df['EMA10'] = talib.EMA(self.close, timeperiod=10)
        df['EMA20'] = talib.EMA(self.close, timeperiod=20)
        df['EMA60'] = talib.EMA(self.close, timeperiod=60)
        df['EMA200'] = talib.EMA(self.close, timeperiod=200)
        #MACD
        macdFast, macdSlow, histogram = self.I(talib.MACD,self.close,fastperiod=12, slowperiod=26, signalperiod=9)
        df['MACD_DIF'] = macdFast
        df['MACD_DIM'] = macdSlow
        df['MACD_HIS'] = histogram
        #RSI
        df['RSI'] = talib.RSI(self.close, timeperiod=self.RSIperiod)
        #print(df['RSI'])
        signal_long = (self.close > df['EMA5']) & (df['EMA5'] > df['EMA10']) & (df['EMA10'] > df['EMA20']) & (df['EMA20'] > df['EMA60'])\
        & (df['EMA60'] > df['EMA200']) & (df['preClose'] < df['EMA5']) & (df["MACD_DIF"] > df["MACD_DIM"]) 
        #print(signal_long)
        
        signal_closePosition = (self.close < df['EMA5']) &  (df["RSI"] < self.RSICloseDownTrigger)
        #signal = signal_long
        #signal[signal_short] = -1
        self.set_signal(signal_long, signal_closePosition)
        
    def getDf(self):
        df = pd.DataFrame(columns=['open','high', 'low', 'close','volume'])
        df['open'] = pd.Series(self.data.Open)
        df['close'] = pd.Series(self.data.Close)
        df['high'] = pd.Series(self.data.High)
        df['low'] = pd.Series(self.data.Low)
        return df
        
    def next(self):
        #if(self.position.pl_pct > 0.3):
        #   self.position.close()
        #if(self.position.pl_pct < -0.05):
        #    self.position.close()
            
        super().next()