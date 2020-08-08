import yfinance as yf
def get_prices(ticket):
    data = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers = ticket,

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            period = "30d",

            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval = "2m",

            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by = 'ticker',

            # adjust all OHLC automatically
            # (optional, default is False)
            auto_adjust = True,

            # download pre/post regular market hours data
            # (optional, default is False)
            prepost = False,

            # use threads for mass downloading? (True/False/Integer)
            # (optional, default is True)
            threads = True,

            # proxy URL scheme use use when downloading?
            # (optional, default is None)
            proxy = None
        )

    x=0
    prc = []
    while len(data.index) > x:
        prc.append(data.iloc[x,0])
        x += 1
    return prc



def simmer(stk): #base trade function
    cash = 100
    num_stk = 0
    dl = False

    sellout_g = .02
    sellout_l = -.02

    for x in range(0,len(stk)):
        if(bool(num_stk) == True):
            # first condition is if gains and second controls losses
            if (((stk[x] - stocks) / stocks) >= sellout_g or ((stk[x] - stocks) / stocks) <= sellout_l): 
                #sell()
                cash += num_stk * stk[x]
                num_stk = 0

        else: 
            if(((stk[x] - stk[x-1])/stk[x-1]*100) < 0):
                dl = True
            if(dl == True & (((stk[x] - stk[x-1])/stk[x-1]*100) >= 0)):
                stocks = stk[x]
                num_stk = cash/stk[x] 
                cash = 0
                dl = False

    cash += num_stk * stocks

    return cash-100 #because init cash is 100 the percent return can be simplified to cash-100, instead of cash-init_cash/init_cash*100

def perfect_simmer(stk): #highest possible gains
    
    for x in range(0, len(stk)):
        cash = 100
        num_stk = 0
        stocks = 0

        if(x+1 < len(stk)):
            if(bool(num_stk)):        
                if(stk[x] > stk[x+1] or x == len(stk)-1):
                    cash = num_stk * stk[x]
                    num_stk = 0
            else:
                if(stk[x] < stk[x+1]):
                    num_stk = cash / stk[x]
                    stocks = stk[x]
                    cash = 0

    return cash-100 #because init cash is 100 the percent return can be simplified to cash-100, instead of cash-init_cash/init_cash*100

def presentation(tickets): #list of tickets
    print('tickets | returned gains | perfect gains')
    sum = 0
    for x in tickets:
        stk = get_prices(x)
        temp = simmer(stk)
        print(x,':   ',temp,'  |  ',perfect_simmer(stk))
        sum += temp
    print('avg return: ',sum/len(tickets))

tickets = ['AMZN','NKE','FB','SNE','TSLA','MSFT']

presentation(tickets)