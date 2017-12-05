from django.shortcuts import render
import requests
from .models import Ticker
import datetime as dt
from .forms import TickerForm


def index(request):

    ticker_list = Ticker.objects.all()

    for i in range(0,len(ticker_list)):
        ticker = ticker_list[i].symbol
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+ticker+'&interval=1min&apikey=87H23GSB7GLYF4D8'
        r= requests.get(url)
        response_dict=r.json()
        pricedata = response_dict['Time Series (1min)']
        mostrecent = max(pricedata.keys())
        price = pricedata[mostrecent]
        price = price['4. close'].split('.')
        ticker_list[i].price = price[0]+'.'+price[1][:2]

    now = dt.datetime.now()
    last_update = str(now)


    if request.method != 'POST':
        form = TickerForm()
    else:
        form = TickerForm(data=request.POST)
        if form.is_valid():
            form.save()

    context = {
    'ticker_list': ticker_list,
    'last_update': last_update,
    'form':form,
    }

    return render(request, 'marketdata/index.html', context)
