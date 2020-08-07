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

backlog = 1800
sum = 0
stk = get_prices('AMZN')
for x in range(0,backlog-1):
    sum += ((stk[x+1] - stk[x])/stk[x]*100)

cash = 1000
num_stk = 0
stocks = 0
sellout_g = .02
sellout_l = -.05


for x in range(backlog+1,len(stk)):
    if(bool(num_stk) == True):
        if (((stk[x] - stocks) / stocks) >= sellout_g):
            #sell()
            cash += num_stk * stk[x]
            num_stk = 0
            print('gains ', cash)

        elif (((stk[x] - stocks) / stocks) <= sellout_l):
            #sell()
            cash += num_stk * stk[x]
            num_stk = 0
            print('loss ', cash)

    else: 
        if(((stk[x] - stk[x-1])/stk[x-1]*100) < 0):
            #buy()
            
            stocks = stk[x]
            num_stk = cash/stk[x] 
            cash = 0
            print('bought ', num_stk, ' at ', stocks)
        #else:

    sum += ((stk[x] - stk[x-1])/stk[x]*100)

cash += num_stk * stocks
print(cash)

# if(sum/backlog > 0):
#     
        
# else:
    # sum += ((stk[backlog+1] - stk[backlog])/stk[backlog]*100)
    # backlog += 1