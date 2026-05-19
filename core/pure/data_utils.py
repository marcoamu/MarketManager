"""Pure data utility functions from MarketManager."""

import time


def addmessages(self, message, results):
    messages = ""
    if Constants.MESSAGES in results:
        messages = results[Constants.MESSAGES]
        messages = messages + "\n"
        messages = messages + message
    else:
        messages = message
    results[Constants.MESSAGES] = messages

# @mide_tiempo


def updateMinMaxValues(self, results):
    currentValue = results[Constants.VALUE]
    results[Constants.ACTION_MIN] = currentValue
    results[Constants.ACTION_MIN_DIST] = 0
    results[Constants.ACTION_MAX] = currentValue
    results[Constants.ACTION_MAX_DIST] = 0
    results[Constants.ACTION_COUNT] = 0
    if results[Constants.CHANGE_ACTION] == 1:
        results[Constants.ACTION_ACUM] = 0



def printValues(self, results):
    print(f' IMPRIMIR Valor '
          f'ACTIVO : {results[Constants.NAME]} Valor: {results[Constants.VALUE]} '
          f'Acumulado: {results[Constants.ACUMULADO]} '
          f'Tendencia: {results[Constants.FLUJO]} '
          f'INDICADOR: {results[Constants.INDICATOR]} '
          f'ACTION_DISTANCE: {results[Constants.ACTION_DISTANCE]} '
          f'tendencia count: {results[Constants.FLUJO_COUNT]}'
          f'DATE: {results[Constants.DATE].values[0]}')



def reviewControls(self, data, active):
    ids = list()
    try:
        algo = ""
    except Exception as e:
        print(f"ERROR reviewControls {str(e)}")



def search_pricesYahoo(self, active):
    data = None
    try:
        nada = ""
        # data = yf.download(tickers=active.parameters.name, period='2d', interval='15m')

    except Exception as e:

        print(f"ERROR search_pricesYahoo {str(e)}")

    return data



def findActiveInDB(self, dbactives, value):
    for active in dbactives:
        if value == active['active']:
            return True
    return False



