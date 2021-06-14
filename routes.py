from app import app
from helpers import formatRates
from flask import json
from datetime import datetime, timedelta
from requests_futures.sessions import FuturesSession


VAT_COMPLY_URL = 'https://api.vatcomply.com'

@app.route("/rates")
def rates():    
    week = [datetime.now()]
    requestUrls = []
    rates = []

    # Checando se já passou das 16 horas UTC (hora que ocorre a inserção dos dados referentes ao dia atual)
    nDays = 7
    if (datetime.utcnow().hour < 16): 
        nDays = 8 
   
    # Criando arrays com as datas dos últimos 7 dias e os links das requisições
    for i in range(nDays):
        if (i < nDays - 1): week.append(week[i] - timedelta(days=1))
        week[i] = week[i].strftime('%Y-%m-%d')
        requestUrls.append(f'{VAT_COMPLY_URL}/rates?base=USD&date={week[i]}')

    print(week)

    # Realizando as requisições de maneira simultânea
    session = FuturesSession()
    futures = [session.get(url) for url in requestUrls]
    for future in futures:
        response = future.result()
        rates.append(json.loads(response.content))

    rates = formatRates(rates)

    return app.response_class(
        response=json.dumps(rates),
        status=200,
        mimetype='application/json',
    )