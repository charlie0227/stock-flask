import requests
import datetime
from models.enums import StockType

TW_TODAY_BRIEF = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=open_dat"

def stock_string_to_int(string):
    string = string.replace(",", "")
    return int(string)

def stock_string_to_float(string):
    string = string.replace(",", "")
    return float(string)


def get_tw_stock_list():
    """
    fields from API: ["證券代號","證券名稱","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"]
    """
    res = requests.get(TW_TODAY_BRIEF)
    result = []
    if 200 <= res.status_code < 300:
        data = res.json()
        for stock in data.get("data", []):
            if type(stock) == list and len(stock) > 1:
                result.append({
                    "number": stock[0],
                    "name": stock[1]
                })
    return result

def get_today_tw_stock_5():
    res = requests.get(TW_TODAY_BRIEF)
    result = []
    if 200 <= res.status_code < 300:
        data = res.json()
        date_time_obj = datetime.datetime.strptime(data.get("date"), '%Y%m%d').strftime('%Y-%m-%d %H:%M:%S')
        for stock in data.get("data", []):
            if type(stock) == list and len(stock) > 9:
                result.append({
                    "date": date_time_obj,
                    "price_type": StockType.daily.name,
                    "stock_number": stock[0],
                    "transactions_number": stock_string_to_int(stock[2]),
                    "transactions_price": stock_string_to_int(stock[3]),
                    "opening_price": stock_string_to_float(stock[4]),
                    "high_price": stock_string_to_float(stock[5]),
                    "low_price": stock_string_to_float(stock[6]),
                    "closing_price": stock_string_to_float(stock[7]),
                })
    return result