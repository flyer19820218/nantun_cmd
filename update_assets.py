import yfinance as yf
import datetime

# --- 南屯指揮部核心參數校正 ---
COST_AVG = 64.65
SHARES = 212000
STOCK_LOAN = 5000000
REALIZED_PROFIT = 285050 
CASH = 900000
MONTHLY_BURN = -20000

REAL_PRINCIPAL = 8900000 

START_DATE = datetime.datetime(2026, 1, 1)
TARGET_DATE = datetime.datetime(2036, 1, 1) 
TARGET_CAPITAL = 100000000 

# 三地產堡壘 
HOUSE_MARKET_VALUE = 28500000 + 29330000 + 24320000
HOUSE_LOAN = HOUSE_MARKET_VALUE * 0.8

# --- 修正後的物理數據捕捉邏輯 ---
try:
    # 分別抓取兩檔 ETF
    ticker_50 = yf.Ticker("0050.TW")
    ticker_l2 = yf.Ticker("00631L.TW")
    
    price_50 = ticker_50.fast_info.last_price
    price_l2 = ticker_l2.fast_info.last_price
    
    # 假設您現在持有 18 張 0050 與 300 張正二
    shares_50 = 18000
    shares_l2 = 300000
    
    # 計算總市值與獲利
    stock_market_value = (shares_50 * price_50) + (shares_l2 * price_l2)
    
except:
    # 若抓取失敗的備援數值 (建議設為您當日的最新參考價)
    price_50 = 111.0
    price_l2 = 60.0 # 請填入正二實際市價
    stock_market_value = (18000 * price_50) + (300000 * price_l2)

# --- 能階運算 ---
stock_market_value = SHARES * current_price
stock_equity = stock_market_value - STOCK_LOAN 

total_assets = stock_market_value + HOUSE_MARKET_VALUE + CASH
total_liabilities = STOCK_LOAN + HOUSE_LOAN
net_worth = total_assets - total_liabilities

# 計算非股票的「固定淨值」給模擬器使用 (單位：元)
fixed_net_worth = HOUSE_MARKET_VALUE + CASH - total_liabilities

stock_profit = (current_price - COST_AVG) * SHARES + REALIZED_PROFIT
stock_roi = (stock_profit / REAL_PRINCIPAL) * 100  
maintenance_ratio = (stock_market_value / STOCK_LOAN) * 100

progress_percent = (net_worth / TARGET_CAPITAL) * 100
days_left = (TARGET_DATE - now).days
countdown_bar = ((now - START_DATE).days / (TARGET_DATE - START_DATE).days) * 100

# --- 生成 index.html ---
with open('template.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    '{{total_assets}}': f"{total_assets/10000:,.1f}",
    '{{total_liabilities}}': f"{total_liabilities/10000:,.1f}",
    '{{net_worth}}': f"{net_worth/10000:,.1f}",
    '{{stock_profit}}': f"{stock_profit/10000:,.1f}",
    '{{stock_roi}}': f"{stock_roi:.1f}",
    '{{stock_market_value_wan}}': f"{stock_market_value/10000:,.1f}",
    '{{stock_equity_wan}}': f"{stock_equity/10000:,.1f}",
    '{{maintenance_ratio}}': f"{maintenance_ratio:.1f}",
    '{{price}}': f"{current_price:.2f}",
    '{{progress_bar_width}}': f"{progress_percent:.2f}",
    '{{progress_text}}': f"{progress_percent:.1f}",
    '{{days_left}}': f"{days_left:,}",
    '{{countdown_bar_width}}': f"{countdown_bar:.2f}",
    '{{current_date}}': now.strftime('%Y-%m-%d'),
    '{{update_time}}': now.strftime('%Y-%m-%d %H:%M:%S'),
    '{{shares}}': str(SHARES),
    '{{fixed_net_worth}}': str(fixed_net_worth)
}

for key, value in replacements.items():
    content = content.replace(key, value)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
