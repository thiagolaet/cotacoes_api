from datetime import datetime, timedelta

def formatRates(rates):

    # Ordenando por data
    rates.sort(key=lambda rate: datetime.strptime(rate['date'], "%Y-%m-%d"))

    # Removendo os dias duplicados
    rates = filterDuplicates(rates)

    # Arredondando os valores para três decimais
    threeDecimalsRates(rates)

    return rates

def filterDuplicates(rates):
    filteredRates = [rates[0]]

    for i in range(1, len(rates)):
        if (rates[i-1]['date'] != rates[i]['date']): 
            filteredRates.append(rates[i])

    return filteredRates

def threeDecimalsRates(rates):
    for rate in rates:
        for currency in rate['rates'].keys():
            rate['rates'][currency] = round(rate['rates'][currency], 3)