import yfinance as yf
import datetime

# --- 南屯指揮部核心參數校正 ---
COST_AVG = 64.65
SHARES = 212000
STOCK_LOAN = 5000000
REALIZED_PROFIT = 285050 # 賣3張利潤 + 股利 (能量守恆)
CASH = 900000
MONTHLY_BURN = -20000

# 2035 破億計畫
START_DATE = datetime.datetime(2026, 1, 1)
TARGET_DATE = datetime.datetime(2035, 1, 1)
TARGET_CAPITAL = 100000000 

# 三地產堡壘 (市值總和與負債)
HOUSE_MARKET_VALUE = 28500000 + 29330000 + 24320000
HOUSE_LOAN = HOUSE_MARKET_VALUE * 0.8

# --- 物理數據捕捉 ---
now = datetime.datetime.now() + datetime.timedelta(hours=8)
try:
    ticker = yf.Ticker("0050.TW")
    current_price = ticker.fast_info.last_price
    if not current_price: current_price = 98.35
except:
    current_price = 98.35

# --- 能階運算 ---
stock_market_value = SHARES * current_price
total_assets = stock_market_value + HOUSE_MARKET_VALUE + CASH
total_liabilities = STOCK_LOAN + HOUSE_LOAN
net_worth = total_assets - total_liabilities

stock_profit = (current_price - COST_AVG) * SHARES + REALIZED_PROFIT
maintenance_ratio = (stock_market_value / STOCK_LOAN) * 100

# 進度運算
progress_percent = (net_worth / TARGET_CAPITAL) * 100
days_left = (TARGET_DATE - now).days
countdown_bar = ((now - START_DATE).days / (TARGET_DATE - START_DATE).days) * 100

# --- 生成 index.html (成品) ---
with open('template.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    '{{total_assets}}': f"{total_assets/10000:,.1f}",
    '{{total_liabilities}}': f"{total_liabilities/10000:,.1f}",
    '{{net_worth}}': f"{net_worth/10000:,.1f}",
    '{{stock_profit}}': f"{stock_profit/10000:,.1f}",
    '{{stock_market_value_wan}}': f"{stock_market_value/10000:,.1f}",
    '{{maintenance_ratio}}': f"{maintenance_ratio:.1f}",
    '{{price}}': f"{current_price:.2f}",
    '{{progress_bar_width}}': f"{progress_percent:.2f}",
    '{{progress_text}}': f"{progress_percent:.1f}",
    '{{days_left}}': f"{days_left:,}",
    '{{countdown_bar_width}}': f"{countdown_bar:.2f}",
    '{{current_date}}': now.strftime('%Y-%m-%d'),
    '{{update_time}}': now.strftime('%Y-%m-%d %H:%M:%S')
}

for key, value in replacements.items():
    content = content.replace(key, value)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
