import requests

TW_TODAY_BRIEF = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=open_dat"

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
