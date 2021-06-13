from flask.globals import request
from app import app
from flask import json
from datetime import datetime, timedelta
from requests_futures.sessions import FuturesSession

VAT_COMPLY_URL = 'https://api.vatcomply.com'

@app.route("/rates")
def rates():    
    week = [datetime.now()]
    requestUrls = []
    rates = []

    for i in range(7):
        if (i < 6): week.append(week[i] - timedelta(days=1))
        week[i] = week[i].strftime('%Y-%m-%d')
        requestUrls.append(f'{VAT_COMPLY_URL}/rates?base=USD&date={week[i]}')

    session = FuturesSession()
    futures = [session.get(url) for url in requestUrls]
    for future in futures:
        response = future.result()
        rates.append(json.loads(response.content))

    return app.response_class(
        response=json.dumps(rates),
        status=200,
        mimetype='application/json',
    )