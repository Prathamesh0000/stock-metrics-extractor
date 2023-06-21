import requests
from bs4 import BeautifulSoup
import csv

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'}
def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def getNasdaq100Tickers():
    url = "https://en.wikipedia.org/wiki/NASDAQ-100"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table with the tickers
    table = soup.find('table', {'id': 'constituents'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        tickerData = row.findAll('td')
        ticker = []
        for each in tickerData:
            ticker.append(each.text.strip())
        tickers.append(ticker)

    return tickers

def createCSVForTickers(csv_file, tickers):
    # Get metric names
    metric_names = set()
    fetched_metrics = {}

    for tickerData in tickers:
        ticker = tickerData[1]
        # fetched_metrics[ticker] = Merge(fetchStockMetricsFromYahooFinance(ticker), fetchStockMetricsFromMarketWatch(ticker))
        fetched_metrics[ticker] = fetchStockMetricsFromMarketWatch(ticker)
        print(f'Fetched metrics for {ticker}')

    for tickerData in tickers:
        ticker = tickerData[1]
        stock_metrics = fetched_metrics[ticker]
        metric_names.update(stock_metrics.keys())

    metric_names = list(metric_names)

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Ticker'] + metric_names)  # Write header row

        # Write metrics for each ticker
        for tickerData in tickers:
            ticker = tickerData[1]
            stock_metrics = fetched_metrics[ticker]
            row = tickerData
            for metric_name in metric_names:
                metric_value = stock_metrics.get(metric_name, 'N/A')
                row.append(metric_value)
            writer.writerow(row)

def fetchStockMetricsFromMarketWatch(symbol): 
    url = f'https://www.marketwatch.com/investing/stock/{symbol}/company-profile?mod=mw_quote_tab'
    # Send a GET request to the Yahoo Finance page
    response = requests.get(url, headers=headers)

    # Create a Beautiful Soup object to pars4e the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the metrics
    tables = soup.find_all('table', {'class': 'table value-pairs no-heading'})
    # Create a dictionary to store the metrics
    metrics = {}

    for table in tables: 
        # Fetch all the table rows
        rows = table.find_all('tr')
        # Iterate over each row
        for row in rows:
            # Fetch the columns for each row
            columns = row.find_all('td')

            # Extract the metric name and value
            if len(columns) == 2:
                metric = columns[0].text.strip()
                value = columns[1].text.strip()
                metrics[metric] = value
    return metrics
def fetchStockMetricsFromYahooFinance(symbol):
    url = f'https://finance.yahoo.com/quote/{symbol}/key-statistics'
    # Send a GET request to the Yahoo Finance page
    response = requests.get(url, headers=headers)

    # Create a Beautiful Soup object to pars4e the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the metrics
    tables = soup.find_all('table', {'class': 'W(100%) Bdcl(c)'})
    # Create a dictionary to store the metrics
    metrics = {}

    for table in tables: 
        # Fetch all the table rows
        rows = table.find_all('tr')
        # Iterate over each row
        for row in rows:
            # Fetch the columns for each row
            columns = row.find_all('td')

            # Extract the metric name and value
            if len(columns) == 2:
                metric = columns[0].text.strip()
                value = columns[1].text.strip()
                metrics[metric] = value
    return metrics

# List of tickers
tickers = getNasdaq100Tickers()
print(tickers)
createCSVForTickers('stock_metrics.csv', tickers)
# TODO: Add historic data for 5 to 10 years
