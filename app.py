# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import requests
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import pytz # Library for timezone correction

# Configuration
bot_token = "7657983245:AAEx45-05EZOKANiaEnJV9M4V1zeKqaSgBM"
chat_id = "-4913116305df"

# Lot sizes embedded from fno_lot_sizes.csv
lot_sizes = {
    '360ONE': 500, 'AARTIIND': 1325, 'ABB': 125, 'ABCAPITAL': 3100, 'ABFRL': 2600, 'ACC': 300, 'ADANIENSOL': 675,
    'ADANIENT': 300, 'ADANIGREEN': 600, 'ADANIPORTS': 475, 'ALKEM': 125, 'AMBER': 100, 'AMBUJACEM': 1050,
    'ANGELONE': 250, 'APLAPOLLO': 350, 'APOLLOHOSP': 125, 'ASHOKLEY': 2500, 'ASIANPAINT': 250, 'ASTRAL': 425,
    'ATGL': 875, 'AUBANK': 1000, 'AUROPHARMA': 550, 'AXISBANK': 625, 'BAJAJ-AUTO': 75, 'BAJAJFINSV': 500,
    'BAJFINANCE': 750, 'BALKRISIND': 300, 'BANDHANBNK': 3600, 'BANKBARODA': 2925, 'BANKINDIA': 5200, 'BDL': 325,
    'BEL': 2850, 'BHARATFORG': 500, 'BHARTIARTL': 475, 'BHEL': 2625, 'BIOCON': 2500, 'BLUESTARCO': 325,
    'BOSCHLTD': 25, 'BPCL': 1975, 'BRITANNIA': 125, 'BSE': 375, 'BSOFT': 1300, 'CAMS': 150, 'CANBK': 6750,
    'CDSL': 475, 'CESC': 3625, 'CGPOWER': 850, 'CHAMBLFERT': 950, 'CHOLAFIN': 625, 'CIPLA': 375, 'COALINDIA': 1350,
    'COFORGE': 375, 'COLPAL': 225, 'CONCOR': 1000, 'CROMPTON': 1800, 'CUMMINSIND': 200, 'CYIENT': 425, 'DABUR': 1250,
    'DALBHARAT': 325, 'DELHIVERY': 2075, 'DIVISLAB': 100, 'DIXON': 50, 'DLF': 825, 'DMART': 150, 'DRREDDY': 625,
    'EICHERMOT': 175, 'ETERNAL': 2425, 'EXIDEIND': 1800, 'FEDERALBNK': 5000, 'FORTIS': 775, 'GAIL': 3150,
    'GLENMARK': 375, 'GMRAIRPORT': 6975, 'GODREJCP': 500, 'GODREJPROP': 275, 'GRANULES': 1075, 'GRASIM': 250,
    'HAL': 150, 'HAVELLS': 500, 'HCLTECH': 350, 'HDFCAMC': 150, 'HDFCBANK': 550, 'HDFCLIFE': 1100, 'HEROMOTOCO': 150,
    'HFCL': 6450, 'HINDALCO': 1400, 'HINDCOPPER': 2650, 'HINDPETRO': 2025, 'HINDUNILVR': 300, 'HINDZINC': 1225,
    'HUDCO': 2775, 'ICICIBANK': 700, 'ICICIGI': 325, 'ICICIPRULI': 925, 'IDEA': 71475, 'IDFCFIRSTB': 9275,
    'IEX': 3750, 'IGL': 2750, 'IIFL': 1650, 'INDHOTEL': 1000, 'INDIANB': 1000, 'INDIGO': 150, 'INDUSINDBK': 700,
    'INDUSTOWER': 1700, 'INFY': 400, 'INOXWIND': 3225, 'IOC': 4875, 'IRB': 11675, 'IRCTC': 875, 'IREDA': 3450,
    'IRFC': 4250, 'ITC': 1600, 'JINDALSTEL': 625, 'JIOFIN': 2350, 'JSL': 850, 'JSWENERGY': 1000, 'JSWSTEEL': 675,
    'JUBLFOOD': 1250, 'KALYANKJIL': 1175, 'KAYNES': 100, 'KEI': 175, 'KFINTECH': 450, 'KOTAKBANK': 400,
    'KPITTECH': 400, 'LAURUSLABS': 1700, 'LICHSGFIN': 1000, 'LICI': 700, 'LODHA': 450, 'LT': 175, 'LTF': 4462,
    'LTIM': 150, 'LUPIN': 425, 'M&M': 200, 'M&MFIN': 2056, 'MANAPPURAM': 3000, 'MANKIND': 225, 'MARICO': 1200,
    'MARUTI': 50, 'MAXHEALTH': 525, 'MAZDOCK': 175, 'MCX': 125, 'MFSL': 800, 'MGL': 400, 'MOTHERSON': 4100,
    'MPHASIS': 275, 'MUTHOOTFIN': 275, 'NATIONALUM': 3750, 'NAUKRI': 375, 'NBCC': 6500, 'NCC': 2700, 'NESTLEIND': 250,
    'NHPC': 6400, 'NMDC': 13500, 'NTPC': 1500, 'NYKAA': 3125, 'OBEROIRLTY': 350, 'OFSS': 75, 'OIL': 1400,
    'ONGC': 2250, 'PAGEIND': 15, 'PATANJALI': 300, 'PAYTM': 725, 'PEL': 750, 'PERSISTENT': 100, 'PETRONET': 1800,
    'PFC': 1300, 'PGEL': 700, 'PHOENIXLTD': 350, 'PIDILITIND': 250, 'PIIND': 175, 'PNB': 8000, 'PNBHOUSING': 650,
    'POLICYBZR': 350, 'POLYCAB': 125, 'POONAWALLA': 1700, 'POWERGRID': 1900, 'PPLPHARMA': 2500, 'PRESTIGE': 450,
    'RBLBANK': 3175, 'RECLTD': 1275, 'RELIANCE': 500, 'RVNL': 1375, 'SAIL': 4700, 'SBICARD': 800, 'SBILIFE': 375,
    'SBIN': 750, 'SHREECEM': 25, 'SHRIRAMFIN': 825, 'SIEMENS': 125, 'SJVN': 5875, 'SOLARINDS': 75, 'SONACOMS': 1050,
    'SRF': 200, 'SUNPHARMA': 350, 'SUPREMEIND': 175, 'SYNGENE': 1000, 'TATACHEM': 650, 'TATACOMM': 350,
    'TATACONSUM': 550, 'TATAELXSI': 100, 'TATAMOTORS': 800, 'TATAPOWER': 1450, 'TATASTEEL': 5500, 'TATATECH': 800,
    'TCS': 175, 'TECHM': 600, 'TIINDIA': 200, 'TITAGARH': 725, 'TITAN': 175, 'TORNTPHARM': 250, 'TORNTPOWER': 375,
    'TRENT': 100, 'TVSMOTOR': 350, 'ULTRACEMCO': 50, 'UNIONBANK': 4425, 'UNITDSPR': 400, 'UNOMINDA': 550,
    'UPL': 1355, 'VBL': 1025, 'VEDL': 1150, 'VOLTAS': 375, 'WIPRO': 3000, 'YESBANK': 31100, 'ZYDUSLIFE': 900
}

# --- Global variables ---
SCAN_INTERVAL = 60
SCAN_MODE = "Intraday"
interval_lock = threading.Lock()
mode_lock = threading.Lock()
watchlist_lock = threading.Lock()
fmi_data_lock = threading.Lock()
FMI_SCAN_INTERVAL = 300
fmi_data = { "long_pct": 0, "short_pct": 0, "nifty_signal": "Neutral", "nifty_reason": "Initializing...", "last_update": None }
error_status_lock = threading.Lock()
error_status = { "data_fetch_error": False, "internet_error": False, "last_error_time": None, "error_message": "" }

# --- FMI (Fund Momentum Indicator) Integration ---
FMI_DATA_PERIOD = "7d"
FMI_DATA_INTERVAL = "30m"
FMI_MOMENTUM_WINDOW = 10
FMI_NIFTY_CACHE_FILE = "fmi_nifty_cache.json"

def update_error_status(has_error, error_type="", message=""):
    with error_status_lock:
        global error_status
        error_status = {
            "data_fetch_error": has_error and error_type == "data",
            "internet_error": has_error and error_type == "internet",
            "last_error_time": datetime.now(pytz.timezone('Asia/Kolkata')).isoformat() if has_error else None,
            "error_message": message if has_error else ""
        }

def get_momentum_signal_pv(ticker_data, window=FMI_MOMENTUM_WINDOW):
    if ticker_data.empty or len(ticker_data) < (window + 1):
        return 0, "Insufficient data"
    close_prices = ticker_data['Close'].squeeze()
    volume_data = ticker_data['Volume'].squeeze()
    price_change_pct = close_prices.pct_change()
    vwpc = price_change_pct * volume_data
    rolling_vwpc_sum = vwpc.rolling(window=window).sum()
    latest_rolling_vwpc = rolling_vwpc_sum.iloc[-1]
    if pd.isna(latest_rolling_vwpc):
        return 0, "Indicator not formed (NaN)"
    if latest_rolling_vwpc > 0:
        return 1, f"Bullish (VWPC Sum: {latest_rolling_vwpc:,.0f})"
    elif latest_rolling_vwpc < 0:
        return -1, f"Bearish (VWPC Sum: {latest_rolling_vwpc:,.0f})"
    else:
        return 0, "Neutral"

def run_fmi_scan():
    try:
        now_ist = datetime.now(pytz.timezone('Asia/Kolkata'))
        print(f"\n🔄 [{now_ist.strftime('%I:%M:%S %p')}] Starting FMI calculation...")
        bullish_count, bearish_count = 0, 0
        tickers_to_analyze = [f"{stock}.NS" for stock in fno_stocks]
        for i, ticker in enumerate(tickers_to_analyze):
            try:
                data = yf.download(ticker, period=FMI_DATA_PERIOD, interval=FMI_DATA_INTERVAL, progress=False, auto_adjust=True)
                signal, _ = get_momentum_signal_pv(data)
                if signal == 1:
                    bullish_count += 1
                elif signal == -1:
                    bearish_count += 1
                print(f"  FMI Scan: {ticker} ({i+1}/{len(tickers_to_analyze)})", end='\r')
            except Exception as e:
                print(f"Error processing {ticker}: {e}")
                continue
        nifty_signal_val, nifty_reason_val = 0, "Error"
        try:
            nifty_df = yf.download("^NSEI", period=FMI_DATA_PERIOD, interval=FMI_DATA_INTERVAL, progress=False, auto_adjust=True)
            nifty_signal_val, nifty_reason_val = get_momentum_signal_pv(nifty_df)
        except Exception as e:
            nifty_reason_val = f"Error fetching Nifty data: {e}"
            update_error_status(True, "data", f"FMI Nifty fetch error: {e}")
        nifty_signal_str = "Bullish" if nifty_signal_val == 1 else ("Bearish" if nifty_signal_val == -1 else "Neutral")
        total_actionable = bullish_count + bearish_count
        long_p = (bullish_count / total_actionable) * 100 if total_actionable > 0 else 0
        short_p = (bearish_count / total_actionable) * 100 if total_actionable > 0 else 0
        with fmi_data_lock:
            global fmi_data
            fmi_data = {
                "long_pct": long_p,
                "short_pct": short_p,
                "nifty_signal": nifty_signal_str,
                "nifty_reason": nifty_reason_val,
                "last_update": datetime.now(pytz.timezone('Asia/Kolkata')).isoformat()
            }
        print(f"\n✅ [{datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M:%S %p')}] FMI Calculation Complete. Long: {long_p:.2f}%, Short: {short_p:.2f}%")
        update_error_status(False)
    except Exception as e:
        print(f"❌ FMI Update Error: {e}")
        update_error_status(True, "internet", f"FMI update failed: {e}")

def load_fmi_nifty_cache():
    try:
        if os.path.exists(FMI_NIFTY_CACHE_FILE):
            with open(FMI_NIFTY_CACHE_FILE, 'r') as f:
                return json.load(f)
        return {"last_nifty": None}
    except Exception:
        return {"last_nifty": None}

def save_fmi_nifty_cache(nifty_price):
    try:
        with open(FMI_NIFTY_CACHE_FILE, 'w') as f:
            json.dump({"last_nifty": nifty_price}, f)
    except Exception as e:
        print(f"Error saving FMI NIFTY cache: {e}")

def update_fmi_data_periodically():
    last_scan_time = time.time() - FMI_SCAN_INTERVAL
    while True:
        try:
            current_time = time.time()
            if (current_time - last_scan_time) >= FMI_SCAN_INTERVAL:
                nifty = yf.Ticker("^NSEI")
                current_nifty = nifty.history(period="1d", interval="1m")['Close'].iloc[-1]
                cache = load_fmi_nifty_cache()
                last_nifty = cache.get("last_nifty")
                nifty_changed = last_nifty is None or abs(current_nifty - last_nifty) > 0.01
                if nifty_changed:
                    print(f"   FMI Trigger: NIFTY price changed from {last_nifty} to {current_nifty}.")
                    run_fmi_scan()
                    save_fmi_nifty_cache(current_nifty)
                    last_scan_time = current_time
                else:
                    print(f"   FMI: No significant NIFTY change, skipping scan. (Current: {current_nifty:.2f})")
                    last_scan_time = current_time
            else:
                remaining_time = FMI_SCAN_INTERVAL - (current_time - last_scan_time)
                print(f"   FMI: Next check in {remaining_time:.0f} seconds...", end='\r')
        except Exception as e:
            print(f"❌ Error in FMI update loop: {e}")
            update_error_status(True, "internet", f"FMI update loop failed: {e}")
        time.sleep(30)

# Watchlist functionality
WATCHLIST_FILE = "watchlist.json"
NIFTY_CACHE_FILE = "nifty_cache.json"
HISTORICAL_DATA_FILE = "historical_scan_data.json"
INTRADAY_ALERTS_FILE = "intraday_alerts_cache.json"

def load_nifty_cache():
    try:
        if os.path.exists(NIFTY_CACHE_FILE):
            with open(NIFTY_CACHE_FILE, 'r') as f:
                return json.load(f)
        return {"last_nifty": None, "last_scan_time": None}
    except Exception as e:
        print(f"Error loading NIFTY cache: {e}")
        return {"last_nifty": None, "last_scan_time": None}

def save_nifty_cache(nifty_price):
    try:
        cache_data = {
            "last_nifty": nifty_price,
            "last_scan_time": datetime.now(pytz.timezone('Asia/Kolkata')).isoformat()
        }
        with open(NIFTY_CACHE_FILE, 'w') as f:
            json.dump(cache_data, f)
        return True
    except Exception as e:
        print(f"Error saving NIFTY cache: {e}")
        return False

def load_historical_data():
    try:
        if os.path.exists(HISTORICAL_DATA_FILE):
            with open(HISTORICAL_DATA_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading historical data: {e}")
        return {}

def save_historical_data(scan_data, scan_mode):
    try:
        today_str = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d')
        historical_data = load_historical_data()
        historical_data[today_str] = {
            "mode": scan_mode,
            "supply_zones": scan_data.get("supply_zones", []),
            "demand_zones": scan_data.get("demand_zones", [])
        }
        max_days = 10
        sorted_dates = sorted(historical_data.keys(), reverse=True)
        if len(sorted_dates) > max_days:
            for old_date in sorted_dates[max_days:]:
                del historical_data[old_date]
        with open(HISTORICAL_DATA_FILE, 'w') as f:
            json.dump(historical_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving historical data: {e}")
        return False

def load_intraday_alerts():
    try:
        if os.path.exists(INTRADAY_ALERTS_FILE):
            with open(INTRADAY_ALERTS_FILE, 'r') as f:
                data = json.load(f)
                if data.get("date") == datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d'):
                    return data.get("alerts", [])
        return []
    except Exception as e:
        print(f"Error loading intraday alerts: {e}")
        return []

def save_intraday_alerts(alerts):
    try:
        today_str = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d')
        cache_data = { "date": today_str, "alerts": alerts }
        with open(INTRADAY_ALERTS_FILE, 'w') as f:
            json.dump(cache_data, f)
        return True
    except Exception as e:
        print(f"Error saving intraday alerts: {e}")
        return False

def is_fresh_breakout(stock, zone_type, historical_data):
    try:
        now_ist = datetime.now(pytz.timezone('Asia/Kolkata'))
        yesterday_str = (now_ist - timedelta(days=1)).strftime('%Y-%m-%d')
        if yesterday_str in historical_data:
            yesterday_zones = historical_data[yesterday_str].get("supply_zones" if zone_type == "supply" else "demand_zones", [])
            if any(zone.get("Stock") == stock for zone in yesterday_zones):
                return False
        day_before_str = (now_ist - timedelta(days=2)).strftime('%Y-%m-%d')
        if day_before_str in historical_data:
            day_before_zones = historical_data[day_before_str].get("supply_zones" if zone_type == "supply" else "demand_zones", [])
            if any(zone.get("Stock") == stock for zone in day_before_zones):
                return False
        return True
    except Exception as e:
        print(f"Error checking fresh breakout for {stock}: {e}")
        return True

def should_trigger_scan():
    try:
        nifty = yf.Ticker("^NSEI")
        nifty_data = nifty.history(period="1d", interval="1m")
        if nifty_data.empty:
            return False, None
        current_nifty = nifty_data['Close'].iloc[-1]
        cache = load_nifty_cache()
        last_nifty = cache.get("last_nifty")
        if last_nifty is None or abs(current_nifty - last_nifty) > 0.01:
            return True, current_nifty
        return False, current_nifty
    except Exception as e:
        print(f"Error checking NIFTY price: {e}")
        update_error_status(True, "data", f"NIFTY price check failed: {e}")
        return True, None

def load_watchlist():
    try:
        if os.path.exists(WATCHLIST_FILE):
            with open(WATCHLIST_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading watchlist: {e}")
        return []

def save_watchlist(watchlist):
    try:
        with open(WATCHLIST_FILE, 'w') as f:
            json.dump(watchlist, f)
        return True
    except Exception as e:
        print(f"Error saving watchlist: {e}")
        return False

class ZoneScannerWebUI(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.serve_main_dashboard()
        elif self.path == '/api/zones':
            self.serve_zone_data()
        elif self.path == '/api/alerts':
            self.serve_alerts()
        elif self.path == '/api/watchlist':
            self.serve_watchlist()
        elif self.path == '/api/fmi':
            self.serve_fmi_data()
        elif self.path == '/api/fmi/refresh':
            self.trigger_fmi_refresh()
        elif self.path == '/api/error-status':
            self.serve_error_status()
        elif self.path == '/scan':
            self.trigger_new_scan()
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/set-interval':
            self.set_scan_interval()
        elif self.path == '/api/set-mode':
            self.set_scan_mode()
        elif self.path == '/api/watchlist/add':
            self.add_to_watchlist()
        elif self.path == '/api/watchlist/remove':
            self.remove_from_watchlist()
        else:
            self.send_error(404)

    def trigger_fmi_refresh(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        threading.Thread(target=run_fmi_scan, daemon=True).start()
        self.wfile.write(json.dumps({'success': True, 'message': 'FMI refresh triggered.'}).encode())

    def serve_error_status(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        with error_status_lock:
            self.wfile.write(json.dumps(error_status).encode())

    def serve_fmi_data(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        with fmi_data_lock:
            self.wfile.write(json.dumps(fmi_data).encode())

    def serve_watchlist(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        watchlist = load_watchlist()
        watchlist_data = []
        for stock in watchlist:
            try:
                ticker = yf.Ticker(stock + ".NS")
                current_price = ticker.fast_info['last_price']
                lot_size = lot_sizes.get(stock, '-')
                watchlist_data.append({ 'stock': stock, 'price': current_price, 'lot_size': lot_size })
            except Exception as e:
                print(f"Error fetching data for watchlist stock {stock}: {e}")
                update_error_status(True, "data", f"Watchlist data fetch error for {stock}")
        self.wfile.write(json.dumps(watchlist_data).encode())

    def add_to_watchlist(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            stock = data.get('stock', '').upper()
            if stock and stock in fno_stocks:
                with watchlist_lock:
                    watchlist = load_watchlist()
                    if stock not in watchlist:
                        watchlist.append(stock)
                        if save_watchlist(watchlist):
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps({'success': True, 'message': f'{stock} added to watchlist'}).encode())
                        else:
                            self.send_error(500, "Failed to save watchlist")
                    else:
                        self.send_error(400, "Stock already in watchlist")
            else:
                self.send_error(400, "Invalid stock symbol")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")

    def remove_from_watchlist(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            stock = data.get('stock', '').upper()
            with watchlist_lock:
                watchlist = load_watchlist()
                if stock in watchlist:
                    watchlist.remove(stock)
                    if save_watchlist(watchlist):
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({'success': True, 'message': f'{stock} removed from watchlist'}).encode())
                    else:
                        self.send_error(500, "Failed to save watchlist")
                else:
                    self.send_error(400, "Stock not in watchlist")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")

    def set_scan_interval(self):
        global SCAN_INTERVAL
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            new_interval = int(data.get('interval'))
            if new_interval in [0, 60, 120, 180, 300, 600, 900, 1800, 3600]:
                with interval_lock:
                    SCAN_INTERVAL = new_interval
                message = f"Interval set to {SCAN_INTERVAL}s" if SCAN_INTERVAL > 0 else "Auto-scan turned off. The current scan will finish."
                print(f"✅ {message}")
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'message': message}).encode())
            else:
                self.send_error(400, "Invalid interval value")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")

    def set_scan_mode(self):
        global SCAN_MODE
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            new_mode = data.get('mode')
            valid_modes = ["Intraday", "2 Days"]
            if new_mode in valid_modes:
                with mode_lock:
                    SCAN_MODE = new_mode
                message = f"Scan mode set to {SCAN_MODE}"
                print(f"✅ {message}")
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'message': message}).encode())
            else:
                self.send_error(400, "Invalid scan mode")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")

    def trigger_new_scan(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        threading.Thread(target=run_zone_scan, kwargs={'scan_type': 'MANUAL'}, daemon=True).start()
        self.wfile.write(b"Manual scan initiated")

    def serve_main_dashboard(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        fno_options_html = ''.join([f'<option value="{stock}">' for stock in fno_stocks])
        html_content = fr"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>FiFTO Dashboard</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
                
                :root {{
                    --bg-color: #02040a;
                    --card-color: rgba(26, 27, 35, 0.85);
                    --text-color: #e8eaf0;
                    --subtle-text-color: #9ca3af;
                    --border-color: #2d3748;
                    --shadow-color: rgba(0,0,0,0.3);
                    --green-color: #10b981;
                    --red-color: #ef4444;
                    --blue-color: #3b82f6;
                    --blue-glow: rgba(59, 130, 246, 0.5);
                    --red-glow: rgba(239, 68, 68, 0.5);
                    --purple-color: #8b5cf6;
                    --orange-color: #f59e0b;
                    --hover-color: #252730;
                    --header-gradient: linear-gradient(135deg, rgba(102, 126, 234, 0.5) 0%, rgba(118, 75, 162, 0.5) 100%);
                    --error-color: #dc2626;
                    --warning-color: #f59e0b;
                    --highlight-color: rgba(255, 215, 0, 0.15);
                }}
                
                body.light-theme {{
                    --bg-color: #f8fafc;
                    --card-color: #ffffff;
                    --text-color: #1e293b;
                    --subtle-text-color: #64748b;
                    --border-color: #e2e8f0;
                    --shadow-color: rgba(0, 0, 0, 0.1);
                    --hover-color: #f1f5f9;
                    --header-gradient: linear-gradient(125deg, #31418b 0%, #752895 100%);
                    --highlight-color: rgba(255, 215, 0, 0.25);
                }}
                
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                
                body {{
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: var(--bg-color);
                    color: var(--text-color);
                    transition: all 0.3s ease;
                    min-height: 100vh;
                }}
                
                /* Animated Background */
                .background-dots {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: -1;
                    overflow: hidden;
                }}

                .dot {{
                    position: absolute;
                    background-color: rgba(139, 92, 246, 0.3);
                    border-radius: 50%;
                    animation: animateDots 20s linear infinite;
                }}

                @keyframes animateDots {{
                    0% {{
                        transform: translateY(100vh) scale(1);
                        opacity: 1;
                    }}
                    100% {{
                        transform: translateY(-10vh) scale(0);
                        opacity: 0;
                    }}
                }}
                
                .container {{ 
                    max-width: 1400px; 
                    margin: 0 auto; 
                    padding: 20px; 
                }}
                
                /* Enhanced Header with Background and Animation */
                .header {{
                    background: var(--header-gradient);
                    backdrop-filter: blur(10px);
                    -webkit-backdrop-filter: blur(10px);
                    padding: 30px 40px;
                    border-radius: 20px;
                    margin-bottom: 25px;
                    text-align: center;
                    position: relative;
                    overflow: hidden;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
                }}
                
                .header h1 {{
                    margin-bottom: 10px;
                    font-size: 4em;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-family: 'Orbitron', monospace;
                    font-weight: 900;
                    position: relative;
                    z-index: 1;
                    
                    color: #ADFF2F; /* Lime Green */
                    text-shadow: 2px 2px 8px rgba(0,0,0,0.9);
                }}
                
                /* Candlestick Animation */
                .candlestick-icon {{
                    margin-right: 15px;
                    display: inline-block;
                    animation: candlestickPulse 2s ease-in-out infinite;
                }}
                
                @keyframes candlestickPulse {{
                    0%, 100% {{ transform: scale(1); opacity: 1; }}
                    50% {{ transform: scale(1.1); opacity: 0.8; }}
                }}
                
                .header .subtitle {{ 
                    color: rgba(255,255,255,0.9); 
                    font-size: 1.3em; 
                    margin-top: 5px; 
                    font-weight: 500;
                    position: relative;
                    z-index: 1;
                }}
                
                .error-indicator {{
                    position: fixed;
                    bottom: 25px;
                    right: 25px;
                    background: var(--error-color);
                    color: white;
                    padding: 12px 20px;
                    border-radius: 8px;
                    font-weight: 600;
                    box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
                    z-index: 1000;
                    display: none;
                    animation: slideInRight 0.3s ease;
                    max-width: 300px;
                    word-wrap: break-word;
                }}
                
                .error-indicator.internet {{
                    background: var(--warning-color);
                }}
                
                .error-indicator.show {{
                    display: block;
                }}
                
                @keyframes slideInRight {{
                    from {{ transform: translateX(100%); opacity: 0; }}
                    to {{ transform: translateX(0); opacity: 1; }}
                }}
                
                .controls {{
                    background: var(--card-color);
                    backdrop-filter: blur(10px);
                    -webkit-backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    padding: 20px 25px;
                    border-radius: 15px;
                    margin-bottom: 25px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 20px;
                    box-shadow: 0 4px 6px var(--shadow-color);
                }}
                
                .left-controls {{ display: flex; align-items: center; gap: 15px; }}
                .right-controls {{ display: flex; align-items: center; gap: 20px; color: var(--subtle-text-color); }}
                
                #live-clock-container {{ 
                    font-weight: 600; 
                    font-size: 1.1em; 
                    background: var(--header-gradient);
                    color: white;
                    padding: 8px 16px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                }}
                
                .control-group {{ display: flex; align-items: center; gap: 10px; }}
                
                #scan-interval, #scan-mode {{
                    background: var(--bg-color);
                    color: var(--text-color);
                    border: 1px solid var(--border-color);
                    border-radius: 8px;
                    padding: 10px 12px;
                    font-weight: 500;
                    transition: all 0.2s ease;
                }}
                
                #scan-interval:focus, #scan-mode:focus {{
                    outline: none;
                    border-color: var(--blue-color);
                    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
                }}
                
                .btn {{
                    background: linear-gradient(135deg, #4f46e5, #7c3aed);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 10px;
                    cursor: pointer;
                    font-size: 1em;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    text-decoration: none;
                    display: inline-block;
                    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
                }}
                
                .btn:hover {{ 
                    transform: translateY(-2px); 
                    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
                }}
                
                .btn.success {{ 
                    background: linear-gradient(135deg, var(--green-color), #059669);
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
                }}
                
                .btn.success:hover {{
                    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
                }}
                
                .btn:disabled {{
                    background: #6b7280;
                    cursor: not-allowed;
                    transform: none;
                    opacity: 0.6;
                    box-shadow: none;
                }}
                
                .btn.small {{ padding: 8px 16px; font-size: 0.9em; }}
                
                .btn.icon-btn {{
                    padding: 0;
                    width: 44px;
                    height: 44px;
                    font-size: 1.5em;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                
                .fmi-section, .stat-card, .tabs {{
                    background: var(--card-color);
                    backdrop-filter: blur(10px);
                    -webkit-backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    padding: 25px;
                    border-radius: 15px;
                    margin-bottom: 25px;
                    box-shadow: 0 4px 6px var(--shadow-color);
                }}
                
                .fmi-header {{ 
                    display: flex; 
                    justify-content: space-between; 
                    align-items: center; 
                    margin-bottom: 20px; 
                }}
                
                .fmi-header h2 {{ 
                    font-weight: 700; 
                    margin: 0; 
                    font-size: 1.4em;
                    color: var(--text-color);
                }}

                .fmi-bar-container {{
                    padding: 20px 0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 15px;
                }}
                .fmi-bar-labels {{
                    width: 100%;
                    max-width: 500px;
                    display: flex;
                    justify-content: space-between;
                    font-size: 1.1em;
                    font-weight: 700;
                    font-family: 'Orbitron', monospace;
                }}
                .fmi-bar-labels .short-label {{ color: var(--red-color); }}
                .fmi-bar-labels .long-label {{ color: var(--green-color); }}

                .fmi-bar {{
                    width: 100%;
                    max-width: 500px;
                    height: 25px;
                    display: flex;
                    background: var(--hover-color);
                    border-radius: 25px;
                    overflow: hidden;
                    border: 1px solid var(--border-color);
                    box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
                }}
                .fmi-short-segment, .fmi-long-segment {{
                    height: 100%;
                    transition: width 0.8s ease-in-out;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: 700;
                    font-size: 0.9em;
                }}
                .fmi-short-segment {{
                    background: linear-gradient(90deg, #b91c1c, var(--red-color));
                    border-radius: 25px 0 0 25px;
                }}
                .fmi-long-segment {{
                    background: linear-gradient(90deg, var(--green-color), #047857);
                    border-radius: 0 25px 25px 0;
                }}
                
                .fmi-details {{ 
                    display: flex; 
                    justify-content: space-between; 
                    align-items: center; 
                    font-size: 0.95em; 
                    padding: 15px 8px 0;
                    width: 100%;
                    border-top: 1px solid var(--border-color);
                }}
                
                .nifty-sentiment {{ 
                    font-family: 'Orbitron', monospace; 
                    font-weight: 700; 
                    font-size: 1.3em; 
                    text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
                    padding: 6px 12px;
                    border-radius: 8px;
                    transition: all 0.3s ease;
                }}
                
                .nifty-sentiment.bullish {{ 
                    color: #fff;
                    background-color: var(--green-color);
                    box-shadow: 0 0 10px var(--green-color);
                }}
                .nifty-sentiment.bearish {{ 
                    color: #fff;
                    background-color: var(--red-color);
                    box-shadow: 0 0 10px var(--red-color);
                }}
                .nifty-sentiment.neutral {{ 
                    color: var(--text-color);
                    background-color: var(--border-color);
                }}
                
                .fmi-last-update {{ 
                    font-size: 0.85em; 
                    color: var(--subtle-text-color); 
                    font-weight: 500;
                }}

                .stats-grid {{ 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
                    gap: 25px; 
                    margin-bottom: 25px; 
                }}
                
                .stat-card {{
                    padding: 30px;
                    text-align: center;
                    transition: all 0.3s ease;
                }}
                
                .stat-card.clickable {{ cursor: pointer; }}
                
                .stat-card.clickable:hover {{ 
                    transform: translateY(-8px) scale(1.02); 
                    box-shadow: 0 12px 25px var(--shadow-color); 
                }}
                
                .stat-card .number {{ 
                    font-size: 2.2em; 
                    font-weight: 800; 
                    margin-bottom: 12px; 
                    font-family: 'Orbitron', monospace;
                }}
                
                .nifty-change {{
                    font-size: 1.1em;
                    font-weight: 600;
                    margin-bottom: 8px;
                    font-family: 'Inter', sans-serif;
                }}
                
                .nifty-change.positive {{ color: var(--green-color); }}
                .nifty-change.negative {{ color: var(--red-color); }}
                .nifty-change.neutral {{ color: var(--subtle-text-color); }}
                .stat-card .label {{ 
                    color: var(--subtle-text-color); 
                    font-size: 1.1em; 
                    text-transform: uppercase; 
                    letter-spacing: 1.5px; 
                    font-weight: 600;
                }}
                
                .stat-card.supply .number {{ color: var(--green-color); }}
                .stat-card.demand .number {{ color: var(--red-color); }}
                .stat-card.nifty .number {{ color: var(--purple-color); }}
                .stat-card.watchlist .number {{ color: var(--orange-color); }}
                
                .tabs {{ 
                    overflow: hidden; 
                }}
                
                .tab-buttons {{ 
                    display: flex; 
                    background: var(--hover-color); 
                }}
                
                .tab-btn {{ 
                    flex: 1; 
                    padding: 18px 24px; 
                    border: none; 
                    background: transparent; 
                    color: var(--subtle-text-color); 
                    cursor: pointer; 
                    font-size: 1.1em; 
                    font-weight: 600; 
                    transition: all 0.3s ease; 
                    border-bottom: 3px solid transparent; 
                }}
                
                .tab-btn:hover {{
                    background: rgba(255,255,255,0.05);
                    color: var(--text-color);
                }}
                
                .tab-btn.active {{ 
                    color: var(--text-color); 
                    background: var(--card-color);
                }}
                
                .tab-btn.active.supply {{ border-bottom-color: var(--green-color); }}
                .tab-btn.active.demand {{ border-bottom-color: var(--red-color); }}
                .tab-btn.active.alerts {{ border-bottom-color: var(--blue-color); }}
                .tab-btn.active.watchlist {{ border-bottom-color: var(--orange-color); }}
                
                .tab-content {{
                    padding: 25px;
                }}
                
                .table-controls {{ 
                    position: relative; 
                    margin-bottom: 20px; 
                    display: flex; 
                    gap: 20px; 
                    align-items: center; 
                    flex-wrap: wrap;
                }}
                
                .filter-input {{
                    padding: 12px 20px;
                    border-radius: 25px;
                    border: 1px solid var(--border-color);
                    background: var(--bg-color);
                    color: var(--text-color);
                    width: 320px;
                    font-size: 1em;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                
                .filter-input:focus {{
                    outline: none;
                    border-color: var(--blue-color);
                    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
                }}
                
                .watchlist-controls {{
                    display: flex;
                    gap: 12px;
                    align-items: center;
                }}
                
                .watchlist-input {{
                    padding: 10px 16px;
                    border-radius: 8px;
                    border: 1px solid var(--border-color);
                    background: var(--bg-color);
                    color: var(--text-color);
                    width: 220px;
                    font-size: 0.95em;
                    transition: all 0.2s ease;
                }}
                
                .watchlist-input:focus {{
                    outline: none;
                    border-color: var(--blue-color);
                    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
                }}
                
                .zone-table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin-top: 10px;
                    background: transparent;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 8px var(--shadow-color);
                }}
                
                .zone-table th, .zone-table td {{ 
                    padding: 16px 12px; 
                    border-bottom: 1px solid var(--border-color); 
                    text-align: center; 
                    vertical-align: middle; 
                }}
                
                .zone-table th {{ 
                    background: var(--hover-color); 
                    font-weight: 700; 
                    color: var(--text-color); 
                    cursor: pointer; 
                    user-select: none; 
                    position: relative; 
                    font-size: 0.95em;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                
                .zone-table td {{ 
                    cursor: pointer; 
                    color: var(--text-color); 
                    transition: all 0.2s ease;
                }}
                
                .zone-table tr:hover td {{ 
                    background: var(--hover-color); 
                    transform: scale(1.01);
                }}
                
                .zone-table th:hover {{ 
                    background: var(--border-color); 
                }}
                
                .zone-table th.sort-asc::after, .zone-table th.sort-desc::after {{ 
                    position: absolute; 
                    right: 8px; 
                    top: 50%; 
                    transform: translateY(-50%); 
                    font-size: 0.8em;
                }}
                
                .zone-table th.sort-asc::after {{ content: '▲'; }}
                .zone-table th.sort-desc::after {{ content: '▼'; }}
                
                .zone-table td:first-child, .zone-table th:first-child {{ text-align: left; }}
                
                .zone-table a {{ 
                    text-decoration: none; 
                    color: var(--text-color); 
                    font-weight: 600; 
                    transition: color 0.2s; 
                }}
                
                .zone-table a:hover {{ color: var(--blue-color); }}
                
                .supply-indicator {{ 
                    background: linear-gradient(135deg, var(--green-color), #059669); 
                    color: white; 
                    padding: 6px 12px; 
                    border-radius: 15px; 
                    font-size: 0.85em; 
                    font-weight: 700; 
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
                }}
                
                .demand-indicator {{ 
                    background: linear-gradient(135deg, var(--red-color), #dc2626); 
                    color: white; 
                    padding: 6px 12px; 
                    border-radius: 15px; 
                    font-size: 0.85em; 
                    font-weight: 700; 
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
                }}
                
                .remove-btn {{ 
                    background: linear-gradient(135deg, var(--red-color), #dc2626); 
                    color: white; 
                    border: none; 
                    padding: 6px 12px; 
                    border-radius: 6px; 
                    cursor: pointer; 
                    font-size: 0.85em; 
                    font-weight: 600;
                    transition: all 0.2s ease;
                }}
                
                .remove-btn:hover {{ 
                    background: linear-gradient(135deg, #dc2626, #b91c1c);
                    transform: translateY(-1px);
                }}
                
                .lot-size-highlight {{
                    background: linear-gradient(135deg, #f59e0b, #d97706);
                    color: white;
                    padding: 8px 14px;
                    border-radius: 10px;
                    font-weight: 700;
                    font-size: 1em;
                    display: inline-block;
                    min-width: 50px;
                    text-align: center;
                    box-shadow: 0 3px 6px rgba(245, 158, 11, 0.3);
                    border: 1px solid rgba(255,255,255,0.2);
                }}
                
                .time-highlight {{
                    background: linear-gradient(135deg, var(--blue-color), #1e40af);
                    color: white;
                    padding: 6px 12px;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 0.9em;
                    box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
                    border: 1px solid rgba(255,255,255,0.2);
                }}
                
                .alerts-container {{
                    max-height: 70vh;
                    overflow-y: auto;
                    padding-right: 10px;
                }}

                .alert-row.highlight-row td {{
                    background-color: var(--highlight-color) !important;
                    transition: background-color 0.5s ease;
                }}
                
                .filter-buttons {{
                    display: flex;
                    gap: 12px;
                    margin-bottom: 20px;
                    flex-wrap: wrap;
                }}
                
                .filter-btn {{
                    padding: 10px 18px;
                    border: 1px solid var(--border-color);
                    background: var(--card-color);
                    color: var(--text-color);
                    border-radius: 25px;
                    cursor: pointer;
                    font-size: 0.9em;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                
                .filter-btn:hover {{ 
                    background: var(--hover-color); 
                    transform: translateY(-2px); 
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }}
                
                .filter-btn.active {{ 
                    background: linear-gradient(135deg, var(--blue-color), #1e40af); 
                    color: white; 
                    border-color: var(--blue-color); 
                    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
                }}
                
                .no-data {{ 
                    text-align: center; 
                    padding: 50px; 
                    color: var(--subtle-text-color); 
                    font-size: 1.2em; 
                    font-weight: 500;
                }}
                
                .floating-action-buttons {{
                    position: fixed;
                    top: 25px;
                    right: 25px;
                    display: flex;
                    gap: 15px;
                    z-index: 1000;
                }}
                .floating-action-buttons .btn {{
                    border-radius: 50%;
                    width: 56px;
                    height: 56px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-size: 1.5em;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                }}
                
                #theme-toggle {{
                    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
                    color: white !important;
                    border: none !important;
                    transition: all 0.3s ease;
                }}
                
                #theme-toggle:hover {{
                    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
                    transform: scale(1.1);
                    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
                }}

                .notification-container {{
                    position: relative;
                }}
                
                .notification-bell {{
                    background: transparent !important;
                    color: var(--green-color) !important;
                    border: 3px solid var(--green-color) !important;
                    transition: all 0.3s ease;
                    position: relative;
                    overflow: visible;
                }}
                
                .notification-bell.error-alert {{
                    color: var(--red-color) !important;
                    border-color: var(--red-color) !important;
                    box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
                    animation: pulse-red 2s infinite;
                }}
                
                .notification-bell.new-notification {{
                    animation: bellGlowBorder 1.5s ease-in-out infinite;
                }}
                
                @keyframes bellGlowBorder {{
                    0%, 100% {{ 
                        transform: scale(1);
                        border-color: var(--green-color);
                        box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
                    }}
                    50% {{ 
                        transform: scale(1.15);
                        border-color: #22d3ee;
                        box-shadow: 0 0 25px rgba(16, 185, 129, 0.7), 0 0 40px rgba(34, 211, 238, 0.4);
                    }}
                }}
                
                .notification-bell:hover {{
                    background: var(--green-color) !important;
                    color: white !important;
                    transform: scale(1.1);
                    box-shadow: 0 0 20px rgba(16, 185, 129, 0.6) !important;
                }}

                .notification-panel {{
                    position: absolute;
                    top: 110%;
                    right: 0;
                    width: 350px;
                    max-height: 400px;
                    overflow-y: auto;
                    background: var(--card-color);
                    border: 1px solid var(--border-color);
                    border-radius: 10px;
                    box-shadow: 0 8px 16px rgba(0,0,0,0.3);
                    z-index: 1001;
                    display: none;
                }}
                .notification-panel.show {{
                    display: block;
                }}
                .notification-item {{
                    padding: 12px 15px;
                    border-bottom: 1px solid var(--border-color);
                    display: flex;
                    gap: 10px;
                    align-items: start;
                    cursor: pointer;
                    transition: background-color 0.2s ease;
                }}
                .notification-item:hover {{
                    background-color: var(--hover-color);
                }}
                .notification-item:last-child {{
                    border-bottom: none;
                }}
                .notification-item .icon {{
                    font-size: 1.2em;
                    margin-top: 2px;
                }}
                .notification-item .content .message {{
                    font-weight: 500;
                }}
                .notification-item .content .time {{
                    font-size: 0.8em;
                    color: var(--subtle-text-color);
                    margin-top: 4px;
                }}
                
                .live-popup-alert {{
                    position: fixed;
                    bottom: 25px;
                    left: 25px;
                    background: var(--card-color);
                    color: var(--text-color);
                    padding: 20px 25px;
                    border-radius: 12px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                    z-index: 1002;
                    width: 100%;
                    max-width: 480px;
                    transform: translateX(-120%);
                    transition: transform 0.6s cubic-bezier(0.68, -0.55, 0.27, 1.55);
                    border: 1px solid var(--border-color);
                    border-left: 5px solid var(--blue-color);
                    backdrop-filter: blur(15px);
                    -webkit-backdrop-filter: blur(15px);
                }}
                
                .live-popup-alert.show {{
                    transform: translateX(0);
                }}
                
                .live-popup-alert.supply {{ border-left-color: var(--green-color); }}
                .live-popup-alert.demand {{ border-left-color: var(--red-color); }}
                
                .popup-alert-header {{
                    font-weight: 700;
                    font-size: 1.2em;
                    margin-bottom: 12px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                
                .popup-alert-content {{
                    font-size: 1em;
                    line-height: 1.5;
                }}
                
                .popup-alert-stock {{
                    font-weight: 700;
                    font-size: 1.1em;
                    color: var(--blue-color);
                    text-decoration: none;
                    cursor: pointer;
                }}
                
                .live-popup-alert.supply .popup-alert-stock {{ color: var(--green-color); }}
                .live-popup-alert.demand .popup-alert-stock {{ color: var(--red-color); }}

                .popup-progress-bar {{
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    height: 4px;
                    background: var(--blue-color);
                    border-radius: 0 0 0 12px;
                    animation: progressBarShrink 7s linear;
                }}
                .live-popup-alert.supply .popup-progress-bar {{ background: var(--green-color); }}
                .live-popup-alert.demand .popup-progress-bar {{ background: var(--red-color); }}
                
                @keyframes progressBarShrink {{
                    from {{ width: 100%; }}
                    to {{ width: 0%; }}
                }}
                
                @media (max-width: 768px) {{
                    .container {{ padding: 15px; }}
                    .header {{ padding: 20px; }}
                    .header h1 {{ font-size: 2.5em; }}
                    .controls {{ flex-direction: column; align-items: stretch; }}
                    .stats-grid {{ grid-template-columns: 1fr; }}
                    .tab-buttons {{ flex-direction: column; }}
                    .table-controls {{ flex-direction: column; align-items: stretch; }}
                    .filter-input {{ width: 100%; }}
                    .floating-action-buttons {{
                        top: 15px;
                        right: 15px;
                        flex-direction: column;
                    }}
                    .live-popup-alert {{
                        bottom: 15px;
                        left: 15px;
                        right: 15px;
                        max-width: none;
                        width: auto;
                    }}
                }}
                
                /* Custom Scrollbar */
                body::-webkit-scrollbar, .notification-panel::-webkit-scrollbar, .alerts-container::-webkit-scrollbar {{
                    width: 8px;
                }}
                
                body::-webkit-scrollbar-track, .notification-panel::-webkit-scrollbar-track, .alerts-container::-webkit-scrollbar-track {{
                    background: var(--bg-color);
                }}
                
                body::-webkit-scrollbar-thumb, .notification-panel::-webkit-scrollbar-thumb, .alerts-container::-webkit-scrollbar-thumb {{
                    background: var(--border-color);
                    border-radius: 4px;
                }}
                
                body::-webkit-scrollbar-thumb:hover, .notification-panel::-webkit-scrollbar-thumb:hover, .alerts-container::-webkit-scrollbar-thumb:hover {{
                    background: var(--subtle-text-color);
                }}
            </style>
        </head>
        <body>
            <div class="background-dots"></div>
            <div id="error-indicator" class="error-indicator">
                <span id="error-message"></span>
            </div>
            
            <div class="container">
                <div class="header">
                    <h1>
                        <div class="candlestick-icon">
                            <svg width="60" height="60" viewBox="0 0 24 24" style="filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));">
                                <rect x="5" y="10" width="4" height="8" rx="1" fill="#10b981"></rect>
                                <line x1="7" y1="4" x2="7" y2="20" stroke="#10b981" stroke-width="2.5" stroke-linecap="round"></line>
                                <rect x="15" y="6" width="4" height="8" rx="1" fill="#ef4444"></rect>
                                <line x1="17" y1="4" x2="17" y2="20" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round"></line>
                            </svg>
                        </div>
                        FiFTO
                    </h1>
                    <div class="subtitle">Enhanced F&O Analytics with Watchlist & Real-time Reporting</div>
                </div>
                
                <div class="controls">
                    <div class="left-controls">
                        <button class="btn success" id="run-scan-btn" onclick="runNewScan()">🔄 Run New Scan</button>
                        <button class="btn" onclick="refreshData()">📊 Refresh Data</button>
                    </div>
                    <div class="right-controls">
                        <div class="control-group">
                            <label for="scan-interval">Zone Scan:</label>
                            <select id="scan-interval" onchange="setScanInterval()">
                                <option value="60">1 Min</option>
                                <option value="120">2 Mins</option>
                                <option value="300">5 Mins</option>
                                <option value="600">10 Mins</option>
                                <option value="0">Off</option>
                            </select>
                        </div>
                        <div class="control-group">
                            <label for="scan-mode">Scan Mode:</label>
                            <select id="scan-mode" onchange="setScanMode()">
                                <option value="Intraday">Intraday</option>
                                <option value="2 Days">Full Scan</option>
                            </select>
                        </div>
                        <span id="live-clock-container">⏰ <span id="live-clock"></span></span>
                        <span id="lastUpdate"></span>
                    </div>
                </div>

                <div class="fmi-section">
                    <div class="fmi-header">
                        <h2>Fund Momentum Indicator (F&O Stocks)</h2>
                        <button class="btn small" id="fmi-refresh-btn" onclick="triggerFmiRefresh()">🔄 Refresh Now</button>
                    </div>
                    <div class="fmi-bar-container">
                        <div class="fmi-bar-labels">
                            <span class="short-label">Short</span>
                            <span class="long-label">Long</span>
                        </div>
                        <div class="fmi-bar">
                            <div id="fmi-short-segment" class="fmi-short-segment"></div>
                            <div id="fmi-long-segment" class="fmi-long-segment"></div>
                        </div>
                    </div>
                    <div class="fmi-details">
                        <div>Nifty Sentiment: <span id="nifty-sentiment-label" class="nifty-sentiment neutral">Initializing...</span></div>
                        <div id="fmi-last-update" class="fmi-last-update"></div>
                    </div>
                </div>

                <div class="stats-grid">
                    <div class="stat-card nifty">
                        <div class="number" id="niftyPrice">-</div>
                        <div class="nifty-change" id="niftyChange">-</div>
                        <div class="label">NIFTY Current</div>
                    </div>
                    <div class="stat-card supply clickable" onclick="goToTab('supply')">
                        <div class="number" id="supplyBreaks">-</div>
                        <div class="label">Supply Breakouts</div>
                    </div>
                    <div class="stat-card demand clickable" onclick="goToTab('demand')">
                        <div class="number" id="demandBreaks">-</div>
                        <div class="label">Demand Breakdowns</div>
                    </div>
                    <div class="stat-card watchlist clickable" onclick="goToTab('watchlist')">
                        <div class="number" id="watchlistCount">-</div>
                        <div class="label">Watchlist Stocks</div>
                    </div>
                </div>
                
                <div class="tabs">
                    <div class="tab-buttons">
                        <button class="tab-btn active alerts" onclick="showTab('alerts', this)">🚨 Live Alerts</button>
                        <button class="tab-btn supply" onclick="showTab('supply', this)">🟢 Supply Zones</button>
                        <button class="tab-btn demand" onclick="showTab('demand', this)">🔴 Demand Zones</button>
                        <button class="tab-btn watchlist" onclick="showTab('watchlist', this)">⭐ Watchlist</button>
                    </div>
                    <div class="tab-content">
                        <div id="alerts-tab" class="tab-panel">
                             <h3>Live Alert Feed</h3>
                             <div class="table-controls">
                                 <input type="text" id="alerts-filter" class="filter-input" onkeyup="filterAlerts()" placeholder="Search alerts by stock name...">
                                 <div class="filter-buttons">
                                     <button class="filter-btn active" id="alert-filter-all" onclick="filterAlertsByType('all', this)">All Alerts</button>
                                     <button class="filter-btn" id="alert-filter-supply" onclick="filterAlertsByType('supply', this)">Supply Only</button>
                                     <button class="filter-btn" id="alert-filter-demand" onclick="filterAlertsByType('demand', this)">Demand Only</button>
                                     <button class="filter-btn" onclick="filterAlertsByWatchlist(this)">⭐ Watchlist Only</button>
                                 </div>
                             </div>
                             <div class="alerts-container">
                                 <div id="alerts-content"><div class="no-data">Loading...</div></div>
                             </div>
                        </div>
                        <div id="supply-tab" class="tab-panel" style="display: none;">
                            <h3>Supply Zone Breakouts</h3>
                            <div id="supply-content"><div class="no-data">Loading...</div></div>
                        </div>
                        <div id="demand-tab" class="tab-panel" style="display: none;">
                            <h3>Demand Zone Breakdowns</h3>
                            <div id="demand-content"><div class="no-data">Loading...</div></div>
                        </div>
                        <div id="watchlist-tab" class="tab-panel" style="display: none;">
                             <h3>Your Watchlist</h3>
                             <div class="table-controls">
                                 <input type="text" id="watchlist-filter" class="filter-input" onkeyup="filterTable('watchlist-filter', 'watchlist-table')" placeholder="Filter watchlist stocks...">
                                 <div class="watchlist-controls">
                                     <input type="text" id="add-stock-input" class="watchlist-input" placeholder="Enter or select stock" list="fno-stocks-list" onkeypress="handleAddStockEnter(event)">
                                     <datalist id="fno-stocks-list">{fno_options_html}</datalist>
                                     <button class="btn small" onclick="addToWatchlist()">➕ Add Stock</button>
                                 </div>
                             </div>
                             <div id="watchlist-content"><div class="no-data">Loading...</div></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="floating-action-buttons">
                <div class="notification-container">
                    <button id="notification-bell" class="btn icon-btn notification-bell" title="Notifications">
                        🔔
                    </button>
                    <div id="notification-panel" class="notification-panel">
                        </div>
                </div>
                <button id="theme-toggle" class="btn" title="Toggle Theme">🌙</button>
            </div>

            <script>
                let notifications = [];
                let lastErrorMessage = "";
                let currentTab = 'alerts';

                // **MODIFIED**: New browser notification icon based on the user's image.
                const logoDataUri = 'data:image/svg+xml;base64,' + btoa(`
                    <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24">
                        <path fill="#10b981" d="M4,18h3v-5H4v5z M9,12h3v-5H9v5z M14,6h3V3h-3V6z M1,16l6-6.5l4,4.5l7.5-8L21,8.5l-9.5,9.5l-4-4.5l-5,5.5V16z"/>
                    </svg>
                `);

                function updateErrorIndicator(errorData) {{
                    const indicator = document.getElementById('error-indicator');
                    const message = document.getElementById('error-message');
                    const bellIcon = document.getElementById('notification-bell');
                    
                    if (errorData.data_fetch_error || errorData.internet_error) {{
                        const errorType = errorData.internet_error ? 'internet' : 'data';
                        const icon = errorType === 'internet' ? '🌐' : '📊';
                        
                        indicator.className = `error-indicator ${{errorType}} show`;
                        message.textContent = `${{icon}} ${{errorData.error_message || 'Connection issue detected'}}`;
                        
                        bellIcon.classList.add('error-alert');
                        
                        if (errorData.error_message && errorData.error_message !== lastErrorMessage) {{
                            addNotification('error', errorData.error_message);
                            lastErrorMessage = errorData.error_message;
                        }}

                    }} else {{
                        indicator.classList.remove('show');
                        bellIcon.classList.remove('error-alert');
                        lastErrorMessage = "";
                    }}
                }}

                function checkErrorStatus() {{
                    fetch('/api/error-status')
                        .then(res => res.json())
                        .then(data => updateErrorIndicator(data))
                        .catch(err => {{
                            console.error('Error checking status:', err);
                            const msg = 'Failed to check system status. Possible connection loss.';
                            if (msg !== lastErrorMessage) {{
                                addNotification('error', msg);
                                lastErrorMessage = msg;
                            }}
                            updateErrorIndicator({{ internet_error: true, error_message: 'Failed to check system status' }});
                        }});
                }}

                function formatDateTime(isoString) {{
                    if (!isoString) return '--:--:--';
                    const date = new Date(isoString);
                    const options = {{ 
                        year: '2-digit', 
                        month: '2-digit', 
                        day: '2-digit', 
                        hour: '2-digit', 
                        minute: '2-digit', 
                        second: '2-digit',
                        hour12: true 
                    }};
                    return date.toLocaleString('en-IN', options).replace(',', '');
                }}

                function formatTime(isoString) {{
                    if (!isoString) return '--:--:--';
                    const date = new Date(isoString);
                    const options = {{ 
                        hour: '2-digit', 
                        minute: '2-digit', 
                        second: '2-digit', 
                        hour12: true 
                    }};
                    return date.toLocaleTimeString('en-US', options);
                }}

                const themeToggleBtn = document.getElementById('theme-toggle');

                function applyTheme(theme) {{
                    if (theme === 'light') {{
                        document.body.classList.add('light-theme');
                        themeToggleBtn.innerHTML = '🌙';
                    }} else {{
                        document.body.classList.remove('light-theme');
                        themeToggleBtn.innerHTML = '☀️';
                    }}
                }}

                function toggleTheme() {{
                    const newTheme = document.body.classList.contains('light-theme') ? 'dark' : 'light';
                    localStorage.setItem('theme', newTheme);
                    applyTheme(newTheme);
                }}

                function updateClock() {{
                    const clockElement = document.getElementById('live-clock');
                    if(clockElement) {{
                        clockElement.textContent = formatTime(new Date().toISOString());
                    }}
                }}

                function setScanInterval() {{
                    const intervalSeconds = document.getElementById('scan-interval').value;
                    localStorage.setItem('scanInterval', intervalSeconds);
                    fetch('/api/set-interval', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ interval: parseInt(intervalSeconds) }})
                    }})
                    .then(res => res.json())
                    .then(data => console.log(data.message))
                    .catch(err => console.error('Error setting scan interval:', err));
                }}

                function triggerFmiRefresh() {{
                    const btn = document.getElementById('fmi-refresh-btn');
                    btn.disabled = true;
                    btn.textContent = 'Refreshing...';
                    
                    fetch('/api/fmi/refresh')
                        .then(res => res.json())
                        .then(data => {{
                            console.log(data.message);
                            setTimeout(() => {{
                                loadFmiData();
                                btn.disabled = false;
                                btn.innerHTML = '🔄 Refresh Now';
                            }}, 5000);
                        }})
                        .catch(err => {{
                            console.error('Error triggering FMI refresh:', err);
                            btn.disabled = false;
                            btn.innerHTML = '🔄 Refresh Now';
                        }});
                }}

                function setScanMode() {{
                    const mode = document.getElementById('scan-mode').value;
                    localStorage.setItem('scanMode', mode);
                    fetch('/api/set-mode', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ mode: mode }})
                    }})
                    .then(res => res.json())
                    .then(data => console.log(data.message))
                    .catch(err => console.error('Error setting scan mode:', err));
                }}

                let currentWatchlist = [];
                let currentAlertFilter = 'all';

                function filterAlerts() {{
                    const searchTerm = document.getElementById('alerts-filter').value.toLowerCase();
                    const table = document.getElementById('live-alerts-table');
                    if (!table) return;
                    const rows = table.getElementsByTagName("tbody")[0].rows;
                    for (const row of rows) {{
                        const stockName = row.cells[1].textContent.toLowerCase();
                        const matchesSearch = stockName.includes(searchTerm);
                        const matchesFilter = checkAlertFilter(row);
                        row.style.display = (matchesSearch && matchesFilter) ? '' : 'none';
                    }}
                }}

                function checkAlertFilter(rowElement) {{
                    if (currentAlertFilter === 'all') return true;
                    if (currentAlertFilter === 'supply') return rowElement.classList.contains('supply');
                    if (currentAlertFilter === 'demand') return rowElement.classList.contains('demand');
                    if (currentAlertFilter === 'watchlist') {{
                        const stockName = rowElement.dataset.stock;
                        return currentWatchlist.includes(stockName);
                    }}
                    return true;
                }}

                function filterAlertsByType(type, buttonElement) {{
                    currentAlertFilter = type;
                    document.querySelectorAll('#alerts-tab .filter-btn').forEach(btn => btn.classList.remove('active'));
                    buttonElement.classList.add('active');
                    filterAlerts();
                }}

                function filterAlertsByWatchlist(buttonElement) {{
                    currentAlertFilter = 'watchlist';
                    document.querySelectorAll('#alerts-tab .filter-btn').forEach(btn => btn.classList.remove('active'));
                    buttonElement.classList.add('active');

                    fetch('/api/watchlist')
                        .then(res => res.json())
                        .then(data => {{
                            currentWatchlist = data.map(item => item.stock);
                            filterAlerts();
                        }})
                        .catch(err => console.error('Error loading watchlist for filter:', err));
                }}

                function filterTable(inputId, tableId) {{
                    const filter = document.getElementById(inputId).value.toUpperCase();
                    const table = document.getElementById(tableId);
                    if (!table) return;
                    const rows = table.getElementsByTagName("tbody")[0].rows;

                    for (const row of rows) {{
                         if (row.hasAttribute('data-hidden-by-watchlist')) {{
                            continue;
                        }}
                        const matchesSearch = row.textContent.toUpperCase().includes(filter);
                        row.style.display = matchesSearch ? "" : "none";
                    }}
                }}
                
                function toggleWatchlistFilter(button, tableId) {{
                    button.classList.toggle('active');
                    const isActive = button.classList.contains('active');

                    fetch('/api/watchlist')
                        .then(res => res.json())
                        .then(watchlistData => {{
                            const watchlistStocks = watchlistData.map(item => item.stock);
                            const table = document.getElementById(tableId);
                            if (!table) return;
                            const rows = table.getElementsByTagName("tbody")[0].rows;
                            
                            for (const row of rows) {{
                                const stockName = row.dataset.stock;
                                if (isActive) {{
                                    if (!watchlistStocks.includes(stockName)) {{
                                        row.style.display = 'none';
                                        row.setAttribute('data-hidden-by-watchlist', 'true');
                                    }}
                                }} else {{
                                    row.removeAttribute('data-hidden-by-watchlist');
                                    row.style.display = '';
                                }}
                            }}
                            const filterInputId = tableId.replace('-table', '-filter');
                            if (document.getElementById(filterInputId)) {{
                                filterTable(filterInputId, tableId);
                            }}
                        }})
                        .catch(err => console.error('Error loading watchlist for filter:', err));
                }}

                function addToWatchlist() {{
                    const stockInput = document.getElementById('add-stock-input');
                    const stock = stockInput.value.trim().toUpperCase();
                    if (!stock) return alert('Please enter a stock symbol');

                    fetch('/api/watchlist/add', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ stock: stock }})
                    }})
                    .then(res => res.json())
                    .then(data => {{
                        if (data.success) {{
                            stockInput.value = '';
                            loadWatchlist();
                            updateWatchlistCount();
                        }} else {{
                            alert('Failed to add stock: ' + (data.message || 'Unknown error'));
                        }}
                    }})
                    .catch(err => alert('Error adding stock to watchlist'));
                }}

                function removeFromWatchlist(stock) {{
                    if (!confirm(`Remove ${{stock}} from watchlist?`)) return;
                    fetch('/api/watchlist/remove', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ stock: stock }})
                    }})
                    .then(res => res.json())
                    .then(data => {{
                        if (data.success) {{
                            loadWatchlist();
                            updateWatchlistCount();
                        }} else {{
                            alert('Failed to remove stock: ' + (data.message || 'Unknown error'));
                        }}
                    }})
                    .catch(err => alert('Error removing stock from watchlist'));
                }}

                function handleAddStockEnter(event) {{
                    if (event.key === 'Enter') addToWatchlist();
                }}

                function loadWatchlist() {{
                    fetch('/api/watchlist')
                        .then(res => res.json())
                        .then(data => {{
                            const content = document.getElementById('watchlist-content');
                            if (data.length === 0) {{
                                content.innerHTML = '<div class="no-data">No stocks in watchlist. Add some using the input above.</div>';
                                return;
                            }}

                            let tableHTML = `<table class="zone-table" id="watchlist-table">
                                <thead><tr>
                                    <th onclick="sortTable(this, 0)">Stock</th>
                                    <th onclick="sortTable(this, 1)">Current Price</th>
                                    <th onclick="sortTable(this, 2)">Lot Size</th>
                                    <th>Action</th>
                                </tr></thead><tbody>`;

                            data.forEach(item => {{
                                const tradingViewUrl = `https://www.tradingview.com/chart/?symbol=NSE:${{item.stock}}`;
                                tableHTML += `<tr>
                                    <td><strong><a href="${{tradingViewUrl}}" target="_blank">${{item.stock}}</a></strong></td>
                                    <td>₹${{item.price.toFixed(2)}}</td>
                                    <td><span class="lot-size-highlight">${{item.lot_size}}</span></td>
                                    <td><button class="remove-btn" onclick="removeFromWatchlist('${{item.stock}}')">Remove</button></td>
                                </tr>`;
                            }});
                            content.innerHTML = tableHTML + '</tbody></table>';
                        }})
                        .catch(err => {{
                            console.error('Error loading watchlist:', err);
                            document.getElementById('watchlist-content').innerHTML = '<div class="no-data">Error loading watchlist</div>';
                        }});
                }}

                function updateWatchlistCount() {{
                    fetch('/api/watchlist')
                        .then(res => res.json())
                        .then(data => {{
                            currentWatchlist = data.map(item => item.stock);
                            document.getElementById('watchlistCount').textContent = data.length;
                        }})
                        .catch(err => console.error('Error updating watchlist count:', err));
                }}

                function loadFmiData() {{
                    fetch('/api/fmi')
                        .then(res => res.json())
                        .then(data => {{
                            const shortSegment = document.getElementById('fmi-short-segment');
                            const longSegment = document.getElementById('fmi-long-segment');
                            const niftyLabel = document.getElementById('nifty-sentiment-label');
                            const lastUpdateElem = document.getElementById('fmi-last-update');

                            const longPct = data.long_pct || 0;
                            const shortPct = data.short_pct || 0;
                            
                            shortSegment.style.width = `${{shortPct}}%`;
                            longSegment.style.width = `${{longPct}}%`;
                            
                            shortSegment.textContent = `${{shortPct.toFixed(1)}}%`;
                            longSegment.textContent = `${{longPct.toFixed(1)}}%`;
                            
                            niftyLabel.textContent = data.nifty_signal;
                            niftyLabel.className = 'nifty-sentiment ' + data.nifty_signal.toLowerCase();

                            if (data.last_update) {{
                                lastUpdateElem.textContent = `Last FMI Update: ${{formatTime(data.last_update)}}`;
                            }}
                        }})
                        .catch(err => console.error('Error loading FMI data:', err));
                }}

                function createDots() {{
                    const container = document.querySelector('.background-dots');
                    if (!container) return;
                    const numDots = 30;
                    for (let i = 0; i < numDots; i++) {{
                        const dot = document.createElement('div');
                        dot.classList.add('dot');
                        const size = Math.random() * 5 + 1;
                        dot.style.width = `${{size}}px`;
                        dot.style.height = `${{size}}px`;
                        dot.style.left = `${{Math.random() * 100}}%`;
                        dot.style.bottom = '0px';
                        const duration = Math.random() * 15 + 10;
                        dot.style.animationDuration = `${{duration}}s`;
                        const delay = Math.random() * 5;
                        dot.style.animationDelay = `${{delay}}s`;
                        container.appendChild(dot);
                    }}
                }}
                
                let hasUnreadNotifications = false;

                function addNotification(type, message, alertObject = null) {{
                    const now = new Date();
                    const newNotification = {{
                        type: type,
                        message: message,
                        stock: alertObject ? alertObject.stock : null,
                        time: now.toISOString(),
                        read: false
                    }};
                    notifications.unshift(newNotification);
                    if (notifications.length > 50) {{
                        notifications.pop();
                    }}
                    
                    hasUnreadNotifications = true;
                    document.getElementById('notification-bell').classList.add('new-notification');
                    
                    if (type === 'alert' && alertObject) {{
                        showLivePopupAlert(alertObject);
                        showWebNotification(alertObject);
                    }}
                }}

                function showLivePopupAlert(alert) {{
                    const existingPopup = document.querySelector('.live-popup-alert');
                    if (existingPopup) {{
                        existingPopup.remove();
                    }}

                    const popup = document.createElement('div');
                    const isSupply = alert.type.toLowerCase().includes('supply');
                    const actionText = alert.action || (isSupply ? 'BREAKOUT' : 'BREAKDOWN');
                    
                    popup.className = `live-popup-alert ${{isSupply ? 'supply' : 'demand'}}`;
                    
                    const icon = isSupply ? '🟢' : '🔴';
                    
                    popup.innerHTML = `
                        <div class="popup-alert-header">
                            ${{icon}} ${{actionText}} ALERT
                        </div>
                        <div class="popup-alert-content">
                            <span class="popup-alert-stock" onclick="handlePopupStockClick('${{alert.stock}}')">${{alert.stock}}</span>
                            <div>
                                Price: ₹${{alert.price.toFixed(2)}} | Lot: ${{alert.lot_size}}
                            </div>
                        </div>
                        <div class="popup-progress-bar"></div>
                    `;

                    document.body.appendChild(popup);
                    setTimeout(() => popup.classList.add('show'), 100);
                    setTimeout(() => {{
                        popup.classList.remove('show');
                        setTimeout(() => popup.remove(), 600);
                    }}, 7000);
                }}

                function handlePopupStockClick(stockSymbol) {{
                    const popup = document.querySelector('.live-popup-alert');
                    if (popup) {{
                        popup.classList.remove('show');
                        setTimeout(() => popup.remove(), 500);
                    }}
                    handleNotificationClick(stockSymbol);
                }}

                function handleNotificationClick(stockSymbol) {{
                    if (!stockSymbol) return;
                    document.getElementById('notification-panel').classList.remove('show');
                    goToTab('alerts');
                    setTimeout(() => {{
                        const alertRow = document.querySelector(`#live-alerts-table .alert-row[data-stock='${{stockSymbol}}']`);
                        if (alertRow) {{
                            alertRow.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                            alertRow.classList.add('highlight-row');
                            setTimeout(() => {{
                                alertRow.classList.remove('highlight-row');
                            }}, 3000);
                        }}
                    }}, 200);
                }}

                function renderNotifications() {{
                    const panel = document.getElementById('notification-panel');
                    if (notifications.length === 0) {{
                        panel.innerHTML = '<div class="no-data" style="padding: 20px;">No notifications yet.</div>';
                        return;
                    }}
                    
                    let html = '';
                    notifications.forEach(n => {{
                        const icon = n.type === 'alert' ? '⚡️' : '⚠️';
                        const timeStr = formatTime(n.time);
                        const clickHandler = n.stock ? `onclick="handleNotificationClick('${{n.stock}}')"` : '';
                        
                        html += `
                            <div class="notification-item" ${{clickHandler}} data-stock="${{n.stock || ''}}">
                                <div class="icon">${{icon}}</div>
                                <div class="content">
                                    <div class="message">${{n.message}}</div>
                                    <div class="time">${{timeStr}}</div>
                                </div>
                            </div>
                        `;
                    }});
                    panel.innerHTML = html;
                }}

                function markNotificationsAsRead() {{
                    notifications.forEach(n => n.read = true);
                    hasUnreadNotifications = false;
                    document.getElementById('notification-bell').classList.remove('new-notification');
                }}

                document.addEventListener('DOMContentLoaded', () => {{
                    const notificationBell = document.getElementById('notification-bell');
                    const notificationPanel = document.getElementById('notification-panel');

                    themeToggleBtn.addEventListener('click', toggleTheme);
                    applyTheme(localStorage.getItem('theme') || 'dark');
                    
                    createDots();

                    notificationBell.addEventListener('click', (event) => {{
                        event.stopPropagation();
                        notificationPanel.classList.toggle('show');
                        if (notificationPanel.classList.contains('show')) {{
                            markNotificationsAsRead();
                            renderNotifications();
                        }}
                    }});

                    document.addEventListener('click', (event) => {{
                        if (!notificationPanel.contains(event.target) && !notificationBell.contains(event.target)) {{
                            notificationPanel.classList.remove('show');
                        }}
                    }});

                    document.getElementById('scan-interval').value = localStorage.getItem('scanInterval') || '60';
                    document.getElementById('scan-mode').value = localStorage.getItem('scanMode') || 'Intraday';
                    
                    updateClock();
                    setInterval(updateClock, 1000);

                    requestNotificationPermission();
                    loadAllData();
                    loadFmiData();
                    loadWatchlist();
                    updateWatchlistCount();
                    startAutoRefresh();
                    loadAlerts();
                    
                    setInterval(checkErrorStatus, 10000);
                }});

                function requestNotificationPermission() {{ if ('Notification' in window) Notification.requestPermission(); }}

                function showWebNotification(alert) {{
                    if (Notification.permission !== "granted") return;
                    const title = `${{alert.stock}} - ${{alert.action}}`;
                    const options = {{
                        body: `Price: ₹${{alert.price.toFixed(2)}} | Lot Size: ${{alert.lot_size || 'N/A'}}`,
                        icon: logoDataUri, 
                        badge: logoDataUri,
                        tag: `fifto-alert-${{alert.stock}}`,
                        renotify: true
                    }};
                    
                    const notification = new Notification(title, options);

                    notification.onclick = function(event) {{
                        event.preventDefault();
                        window.open('https://fifto-scanner.onrender.com', '_blank');
                        notification.close();
                    }};
                }}

                function showTab(tabName, element) {{
                    document.querySelectorAll('.tab-panel').forEach(p => p.style.display = 'none');
                    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                    document.getElementById(`${{tabName}}-tab`).style.display = 'block';
                    element.classList.add('active');
                    currentTab = tabName;
                    if (tabName === 'watchlist') loadWatchlist();
                }}

                function goToTab(tabName, filterType = null) {{
                    const tabButton = document.querySelector(`.tab-btn.${{tabName}}`);
                    if (tabButton) {{
                        tabButton.click();
                        const tabsContainer = document.querySelector('.tabs');
                        if (tabsContainer) {{
                            tabsContainer.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                        }}
                        if (filterType) {{
                            setTimeout(() => {{
                                const filterButton = document.getElementById(`alert-filter-${{filterType}}`);
                                if (filterButton) filterButton.click();
                            }}, 100);
                        }}
                    }}
                }}

                function loadAllData() {{
                    fetch('/api/zones')
                        .then(res => res.json())
                        .then(data => {{
                            updateStats(data);
                            document.getElementById('supply-content').innerHTML = createTableHTML(data.supply_zones || [], 'supply');
                            document.getElementById('demand-content').innerHTML = createTableHTML(data.demand_zones || [], 'demand');
                            updateLastUpdate(data.last_update);
                        }})
                        .catch(err => {{
                            console.error('Error loading data:', err);
                            updateErrorIndicator({{
                                data_fetch_error: true,
                                error_message: 'Failed to load zone data'
                            }});
                        }});
                }}

                function updateStats(data) {{
                    document.getElementById('supplyBreaks').textContent = (data.supply_zones || []).length;
                    document.getElementById('demandBreaks').textContent = (data.demand_zones || []).length;
                    document.getElementById('niftyPrice').textContent = data.nifty_price || '-';
                    
                    const niftyChangeElement = document.getElementById('niftyChange');
                    if (data.nifty_change !== undefined && data.nifty_change_percent !== undefined) {{
                        const changePoints = data.nifty_change > 0 ? `+${{data.nifty_change.toFixed(2)}}` : data.nifty_change.toFixed(2);
                        const changePercent = data.nifty_change_percent > 0 ? `+${{data.nifty_change_percent.toFixed(2)}}%` : `${{data.nifty_change_percent.toFixed(2)}}%`;
                        
                        niftyChangeElement.textContent = `${{changePoints}} (${{changePercent}})`;
                        
                        niftyChangeElement.className = 'nifty-change';
                        if (data.nifty_change > 0) {{
                            niftyChangeElement.classList.add('positive');
                        }} else if (data.nifty_change < 0) {{
                            niftyChangeElement.classList.add('negative');
                        }} else {{
                            niftyChangeElement.classList.add('neutral');
                        }}
                    }} else {{
                        niftyChangeElement.textContent = '-';
                        niftyChangeElement.className = 'nifty-change neutral';
                    }}
                }}

                function createTableHTML(zones, type) {{
                    if (zones.length === 0) return `<div class="no-data">No ${{type}} zone events detected.</div>`;
                    const tableId = `${{type}}-table`;
                    const isSupply = type === 'supply';

                    let tableHTML = `<div class="table-controls">
                            <input type="text" id="${{type}}-filter" class="filter-input" onkeyup="filterTable('${{type}}-filter', '${{tableId}}')" placeholder="Search by stock...">
                            <button class="filter-btn" onclick="toggleWatchlistFilter(this, '${{tableId}}')">⭐ Watchlist Only</button>
                        </div>`;

                    tableHTML += `<table class="zone-table" id="${{tableId}}"><thead><tr>
                        <th onclick="sortTable(this, 0)">Stock</th>
                        <th onclick="sortTable(this, 1)">Price</th>
                        <th onclick="sortTable(this, 2)">Zone Low</th>
                        <th onclick="sortTable(this, 3)">Zone High</th>
                        <th onclick="sortTable(this, 4)">${{isSupply ? 'Breakout %' : 'Breakdown %'}}</th>
                        <th onclick="sortTable(this, 5)">Lot Size</th>
                        <th onclick="sortTable(this, 6)">Status</th>
                        <th onclick="sortTable(this, 7)">Time</th>
                        </tr></thead><tbody>`;

                    zones.forEach(zone => {{
                        const tradingViewUrl = `https://www.tradingview.com/chart/?symbol=NSE:${{zone.stock}}`;
                        const percent = isSupply ? (((zone.price - zone.zone_high) / zone.zone_high) * 100).toFixed(2) : (((zone.zone_low - zone.price) / zone.zone_low) * 100).toFixed(2);
                        const statusText = isSupply ? 'BREAKOUT' : 'BREAKDOWN';
                        const statusClass = isSupply ? 'supply-indicator' : 'demand-indicator';

                        tableHTML += `<tr data-stock="${{zone.stock}}">
                            <td><strong><a href="${{tradingViewUrl}}" target="_blank">${{zone.stock}}</a></strong></td>
                            <td>₹${{zone.price.toFixed(2)}}</td>
                            <td>₹${{zone.zone_low.toFixed(2)}}</td>
                            <td>₹${{zone.zone_high.toFixed(2)}}</td>
                            <td>${{percent}}%</td>
                            <td><span class="lot-size-highlight">${{zone.lot_size || '-'}}</span></td>
                            <td><span class="${{statusClass}}">${{statusText}}</span></td>
                            <td><span class="time-highlight">${{zone.time || '--:--:--'}}</span></td>
                        </tr>`;
                    }});
                    return tableHTML + '</tbody></table>';
                }}

                function loadAlerts() {{
                    fetch('/api/alerts')
                        .then(res => res.json())
                        .then(alerts => {{
                            const lastNotifiedTimestamp = localStorage.getItem('lastNotifiedTimestamp') || '';
                            let latestTimestampThisBatch = lastNotifiedTimestamp;

                            alerts.forEach(alert => {{
                                if (alert.timestamp > lastNotifiedTimestamp) {{
                                    const message = `${{alert.stock}} - ${{alert.action}} @ ₹${{alert.price.toFixed(2)}}`;
                                    addNotification('alert', message, alert);
                                    if(alert.timestamp > latestTimestampThisBatch) {{
                                        latestTimestampThisBatch = alert.timestamp;
                                    }}
                                }}
                            }});
                            
                            if (latestTimestampThisBatch > lastNotifiedTimestamp) {{
                                localStorage.setItem('lastNotifiedTimestamp', latestTimestampThisBatch);
                            }}

                            const content = document.getElementById('alerts-content');
                            if (alerts.length === 0) {{
                                content.innerHTML = '<div class="no-data">No alerts today.</div>';
                                return;
                            }}

                            let alertsHTML = `<table class="zone-table" id="live-alerts-table">
                                <thead><tr>
                                    <th onclick="sortTable(this, 0)" class="sort-desc">Time</th>
                                    <th onclick="sortTable(this, 1)">Stock</th>
                                    <th onclick="sortTable(this, 2)">Action</th>
                                    <th onclick="sortTable(this, 3)">Price</th>
                                    <th onclick="sortTable(this, 4)">Zone</th>
                                    <th onclick="sortTable(this, 5)">Lot Size</th>
                                </tr></thead><tbody>`;

                            alerts.slice().reverse().forEach(alert => {{
                                const tradingViewUrl = `https://www.tradingview.com/chart/?symbol=NSE:${{alert.stock}}`;
                                const isSupply = alert.type.toLowerCase().includes('supply');
                                const actionText = alert.action || (isSupply ? 'BREAKOUT' : 'BREAKDOWN');
                                const actionClass = isSupply ? 'supply-indicator' : 'demand-indicator';

                                alertsHTML += `<tr class="alert-row ${{isSupply ? 'supply' : 'demand'}}" data-stock="${{alert.stock}}">
                                    <td><span class="time-highlight">${{formatDateTime(alert.timestamp)}}</span></td>
                                    <td><strong><a href="${{tradingViewUrl}}" target="_blank">${{alert.stock}}</a></strong></td>
                                    <td><span class="${{actionClass}}">${{actionText}}</span></td>
                                    <td>₹${{alert.price.toFixed(2)}}</td>
                                    <td>₹${{alert.zone_low.toFixed(2)}} - ₹${{alert.zone_high.toFixed(2)}}</td>
                                    <td><span class="lot-size-highlight">${{alert.lot_size || 'N/A'}}</span></td>
                                </tr>`;
                            }});

                            content.innerHTML = alertsHTML + '</tbody></table>';
                            setTimeout(() => filterAlerts(), 100);
                        }})
                        .catch(err => {{
                            console.error('Error loading alerts:', err);
                            updateErrorIndicator({{
                                data_fetch_error: true,
                                error_message: 'Failed to load alerts'
                            }});
                        }});
                }}

                function runNewScan() {{ 
                    fetch('/scan')
                        .then(() => setTimeout(refreshData, 2000))
                        .catch(err => {{
                            console.error('Error triggering scan:', err);
                            updateErrorIndicator({{
                                data_fetch_error: true,
                                error_message: 'Failed to trigger scan'
                            }});
                        }});
                }}
                
                function refreshData() {{ 
                    loadAllData(); 
                    loadAlerts(); 
                    updateWatchlistCount(); 
                    loadFmiData(); 
                    checkErrorStatus();
                }}
                
                function startAutoRefresh() {{ setInterval(refreshData, 30000); }}
                
                function updateLastUpdate(isoTime) {{ 
                    document.getElementById('lastUpdate').textContent = `Last Scan: ${{formatTime(isoTime)}}`; 
                }}

                function sortTable(th, n) {{
                    const table = th.closest('table');
                    if (!table) return;
                    const tbody = table.tBodies[0];
                    if (!tbody) return;
                    const rows = Array.from(tbody.rows);
                    const currentDir = th.classList.contains('sort-desc') ? 'asc' : 'desc';
                    
                    table.querySelectorAll('th').forEach(header => {{
                        if (header !== th) {{
                           header.classList.remove('sort-asc', 'sort-desc');
                        }}
                    }});

                    th.classList.remove('sort-asc', 'sort-desc');
                    th.classList.add(`sort-${{currentDir}}`);

                    rows.sort((a, b) => {{
                        let aText = a.cells[n].textContent.trim();
                        let bText = b.cells[n].textContent.trim();
                        
                        const isTimeColumn = (aText.match(/\d{{4}}-\d{{2}}-\d{{2}}/) || aText.match(/\d{{2}}\/\d{{2}}\/\d{{2}}/));

                        if (isTimeColumn) {{
                            const aDate = new Date(aText.replace(/(\d{{2}})\/(\d{{2}})\/(\d{{2}})/, '20$3-$2-$1'));
                            const bDate = new Date(bText.replace(/(\d{{2}})\/(\d{{2}})\/(\d{{2}})/, '20$3-$2-$1'));
                            const comparison = aDate.getTime() - bDate.getTime();
                            return currentDir === 'asc' ? comparison : -comparison;
                        }}
                        
                        const aNum = parseFloat(aText.replace(/[₹,]/g, ''));
                        const bNum = parseFloat(bText.replace(/[₹,]/g, ''));
                        const aVal = !isNaN(aNum) ? aNum : aText.toLowerCase();
                        const bVal = !isNaN(bNum) ? bNum : bText.toLowerCase();

                        let comparison = 0;
                        if (aVal > bVal) comparison = 1;
                        if (aVal < bVal) comparison = -1;
                        
                        return currentDir === 'asc' ? comparison : -comparison;
                    }});

                    rows.forEach(row => tbody.appendChild(row));
                }}
            </script>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

    def serve_zone_data(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        supply_zones, demand_zones = [], []
        try:
            if os.path.exists("weekly_supply_broken.xlsx"):
                df_supply = pd.read_excel("weekly_supply_broken.xlsx")
                if 'Time' in df_supply.columns and 'Lot Size' in df_supply.columns:
                    df_supply['Time'] = pd.to_datetime(df_supply['Time'], format='%Y-%m-%d %I:%M:%S %p', errors='coerce').dt.strftime('%I:%M:%S %p')
                    df_supply.sort_values(by='Time', ascending=False, inplace=True)
                supply_zones = df_supply.rename(columns={ 'Stock': 'stock', 'Price': 'price', 'Supply Low': 'zone_low', 'Supply High': 'zone_high', 'Time': 'time', 'Lot Size': 'lot_size' }).to_dict('records')
        except Exception as e:
            print(f"Error reading supply file: {e}")
            update_error_status(True, "data", f"Supply data read error: {e}")
        try:
            if os.path.exists("weekly_demand_broken.xlsx"):
                df_demand = pd.read_excel("weekly_demand_broken.xlsx")
                if 'Time' in df_demand.columns and 'Lot Size' in df_demand.columns:
                    df_demand['Time'] = pd.to_datetime(df_demand['Time'], format='%Y-%m-%d %I:%M:%S %p', errors='coerce').dt.strftime('%Y-%m-%d %I:%M:%S %p')
                    df_demand.sort_values(by='Time', ascending=False, inplace=True)
                demand_zones = df_demand.rename(columns={ 'Stock': 'stock', 'Price': 'price', 'Demand Low': 'zone_low', 'Demand High': 'zone_high', 'Time': 'time', 'Lot Size': 'lot_size' }).to_dict('records')
        except Exception as e:
            print(f"Error reading demand file: {e}")
            update_error_status(True, "data", f"Demand data read error: {e}")
        nifty_price = "-"
        nifty_change = 0
        nifty_change_percent = 0
        try:
            nifty = yf.Ticker("^NSEI")
            nifty_data = nifty.history(period="2d", interval="1d")
            if not nifty_data.empty and len(nifty_data) >= 2:
                current_price = nifty_data['Close'].iloc[-1]
                previous_price = nifty_data['Close'].iloc[-2]
                nifty_price = f"{current_price:.2f}"
                nifty_change = current_price - previous_price
                nifty_change_percent = (nifty_change / previous_price) * 100
            elif not nifty_data.empty:
                current_price = nifty_data['Close'].iloc[-1]
                nifty_price = f"{current_price:.2f}"
        except Exception as e:
            print(f"Error fetching NIFTY price: {e}")
            update_error_status(True, "data", f"NIFTY price fetch error: {e}")
        response_data = {
            'supply_zones': supply_zones, 'demand_zones': demand_zones,
            'nifty_price': nifty_price, 'nifty_change': nifty_change, 'nifty_change_percent': nifty_change_percent,
            'last_update': datetime.now(pytz.timezone('Asia/Kolkata')).isoformat()
        }
        self.wfile.write(json.dumps(response_data).encode())

    def serve_alerts(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        alerts = []
        if os.path.exists("today_alerts.json"):
            try:
                with open("today_alerts.json", 'r') as f:
                    alerts = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error reading alerts file: {e}")
                update_error_status(True, "data", f"Alerts file read error: {e}")
        self.wfile.write(json.dumps(alerts).encode())

def start_web_server():
    try:
        port = int(os.environ.get('PORT', 8080))
        server_address = ('0.0.0.0', port)
        server = HTTPServer(server_address, ZoneScannerWebUI)
        print(f"🌐 Web UI server started. Access it at https://fifto-scanner.onrender.com")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Server could not start: {e}")

def save_alert_to_json(stock, price, zone_low, zone_high, zone_type, action):
    ist_tz = pytz.timezone('Asia/Kolkata')
    ist_time = datetime.now(ist_tz)
    lot_size = lot_sizes.get(stock, '-')
    alert = { 'timestamp': ist_time.isoformat(), 'stock': stock, 'price': price, 'zone_low': zone_low, 'zone_high': zone_high, 'type': zone_type, 'action': action, 'lot_size': lot_size }
    alert_file = "today_alerts.json"
    alerts = []
    if not os.path.exists(alert_file) or datetime.fromtimestamp(os.path.getmtime(alert_file), tz=ist_tz).date() != ist_time.date():
         with open(alert_file, 'w') as f: json.dump([], f)
    try:
        with open(alert_file, 'r') as f: alerts = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError): pass
    alerts.append(alert)
    with open(alert_file, 'w') as f: json.dump(alerts, f, indent=2)

def send_telegram_message(message):
    try:
        if bot_token == "YOUR_BOT_TOKEN" or chat_id == "YOUR_CHAT_ID":
            print("📣 Telegram credentials not set. Skipping message.")
            return
        max_length = 4096
        if len(message) > max_length:
            parts = [message[i:i+max_length] for i in range(0, len(message), max_length)]
            for part in parts:
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                payload = {"chat_id": chat_id, "text": part, "parse_mode": "HTML", "disable_web_page_preview": False}
                requests.post(url, data=payload, timeout=10)
                time.sleep(1)
        else:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML", "disable_web_page_preview": False}
            requests.post(url, data=payload, timeout=10)
        print(f"📱 Telegram message sent.")
    except Exception as e:
        print(f"❌ Telegram error: {e}")
        update_error_status(True, "internet", f"Telegram send failed: {e}")

def send_daily_telegram_report():
    today_str = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%d-%b-%Y')
    alert_file = "today_alerts.json"
    if not os.path.exists(alert_file):
        message = f"<b>FiFTO Daily Report: {today_str}</b>\n\nNo alerts were generated today."
        send_telegram_message(message)
        return
    try:
        with open(alert_file, 'r') as f:
            alerts = json.load(f)
        if not alerts:
            message = f"<b>FiFTO Daily Report: {today_str}</b>\n\nNo alerts were generated today."
            send_telegram_message(message)
            return
        supply_alerts = [a for a in alerts if a['type'] == 'SUPPLY']
        demand_alerts = [a for a in alerts if a['type'] == 'DEMAND']
        message = f"<b>📊 FiFTO Daily Report: {today_str}</b>\n\n"
        if supply_alerts:
            message += f"<b>🟢 Supply Breakouts ({len(supply_alerts)}):</b>\n"
            for alert in supply_alerts:
                message += f"- {alert['stock']} @ ₹{alert['price']:.2f}\n"
            message += "\n"
        if demand_alerts:
            message += f"<b>🔴 Demand Breakdowns ({len(demand_alerts)}):</b>\n"
            for alert in demand_alerts:
                message += f"- {alert['stock']} @ ₹{alert['price']:.2f}\n"
            message += "\n"
        message += f"Total alerts generated: {len(alerts)}"
        send_telegram_message(message)
    except Exception as e:
        print(f"❌ Error generating daily Telegram report: {e}")
        update_error_status(True, "data", f"Daily report generation failed: {e}")

def send_zone_alert(title, data, zone_type):
    ist_tz = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist_tz)
    today_str = now_ist.strftime('%Y-%m-%d')
    memory_file = "notified_stocks_today.txt"
    notified_today = set()
    if os.path.exists(memory_file):
        try:
            with open(memory_file, 'r') as f:
                lines = f.read().splitlines()
                if lines and lines[0] == today_str:
                    notified_today.update(lines[1:])
                else:
                    with open(memory_file, 'w') as f_write: f_write.write(today_str + '\n')
        except Exception as e:
            print(f"Error reading notification memory file: {e}")
            with open(memory_file, 'w') as f_write: f_write.write(today_str + '\n')
    else:
        with open(memory_file, 'w') as f_write: f_write.write(today_str + '\n')
    for x in data:
        stock = x['Stock']
        if stock in notified_today: continue
        price = x['Price']
        lot_size = x.get('Lot Size', lot_sizes.get(stock, '-'))
        alert_time = now_ist.strftime('%d-%b-%Y %I:%M %p')
        if "Supply" in zone_type:
            zone_low, zone_high = x['Supply Low'], x['Supply High']
            header, alert_type, action = "🟢 SUPPLY BREAKOUT", "SUPPLY", "Breakout"
            zone_icon = "⬆️"
        else:
            zone_low, zone_high = x['Demand Low'], x['Demand High']
            header, alert_type, action = "🔴 DEMAND BREAKDOWN", "DEMAND", "Breakdown"
            zone_icon = "⬇️"
        zone_range = abs(zone_high - zone_low)
        zone_mid = (zone_high + zone_low) / 2
        zone_range_pct = (zone_range / zone_mid) * 100 if zone_mid > 0 else 0
        within_zone = zone_low <= price <= zone_high
        zone_status = "🎯 WITHIN ZONE" if within_zone else f"{zone_icon} BROKEN"
        web_trading_view_url = f"https://www.tradingview.com/chart/?symbol=NSE:{stock}"
        stock_link = f'<a href="{web_trading_view_url}">{stock}</a>'
        telegram_message = (f"<b>{header}</b>\n\n"
            f"📊 <b>Stock:</b> {stock_link}\n"
            f"💰 <b>Price:</b> ₹{price:.2f}\n"
            f"🎯 <b>Zone:</b> ₹{zone_low:.2f} - ₹{zone_high:.2f}\n"
            f"📏 <b>Range:</b> {zone_range_pct:.1f}% | {zone_status}\n"
            f"📦 <b>Lot Size:</b> {lot_size}\n"
            f"🕒 <b>Time:</b> {alert_time}")
        send_telegram_message(telegram_message)
        save_alert_to_json(stock, price, zone_low, zone_high, alert_type, action)
        print(f"🚨 {alert_type} Alert: {stock} @ ₹{price:.2f} | Lot: {lot_size} | {zone_status}")
        try:
            with open(memory_file, 'a') as f_append: f_append.write(stock + '\n')
            notified_today.add(stock)
        except Exception as e:
            print(f"Error writing to notification memory file: {e}")

fno_stocks = ['360ONE', 'ABB', 'ACC', 'APLAPOLLO', 'AUBANK', 'AARTIIND', 'ADANIENSOL', 'ADANIENT', 'ADANIGREEN', 'ADANIPORTS', 'ATGL', 'ABCAPITAL', 'ABFRL', 'ALKEM', 'AMBER', 'AMBUJACEM', 'ANGELONE', 'APOLLOHOSP', 'ASHOKLEY', 'ASIANPAINT', 'ASTRAL', 'AUROPHARMA', 'DMART', 'AXISBANK', 'BSOFT', 'BSE', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BALKRISIND', 'BANDHANBNK', 'BANKBARODA', 'BANKINDIA', 'BDL', 'BEL', 'BHARATFORG', 'BHEL', 'BPCL', 'BHARTIARTL', 'BIOCON', 'BLUESTARCO', 'BOSCHLTD', 'BRITANNIA', 'CESC', 'CGPOWER', 'CANBK', 'CDSL', 'CHAMBLFERT', 'CHOLAFIN', 'CIPLA', 'COALINDIA', 'COFORGE', 'COLPAL', 'CAMS', 'CONCOR', 'CROMPTON', 'CUMMINSIND', 'CYIENT', 'DLF', 'DABUR', 'DALBHARAT', 'DELHIVERY', 'DIVISLAB', 'DIXON', 'DRREDDY', 'EICHERMOT', 'EXIDEIND', 'NYKAA', 'FORTIS', 'GAIL', 'GMRAIRPORT', 'GLENMARK', 'GODREJCP', 'GODREJPROP', 'GRANULES', 'GRASIM', 'HCLTECH', 'HDFCAMC', 'HDFCBANK', 'HDFCLIFE', 'HFCL', 'HAVELLS', 'HEROMOTOCO', 'HINDALCO', 'HAL', 'HINDCOPPER', 'HINDPETRO', 'HINDUNILVR', 'HINDZINC', 'HUDCO', 'ICICIBANK', 'ICICIGI', 'ICICIPRULI', 'IDFCFIRSTB', 'IIFL', 'IRB', 'ITC', 'INDIANB', 'IEX', 'IOC', 'IRCTC', 'IRFC', 'IREDA', 'IGL', 'INDUSTOWER', 'INDUSINDBK', 'NAUKRI', 'INFY', 'INOXWIND', 'INDIGO', 'JSWENERGY', 'JSWSTEEL', 'JSL', 'JINDALSTEL', 'JIOFIN', 'JUBLFOOD', 'KEI', 'KPITTECH', 'KALYANKJIL', 'KAYNES', 'KFINTECH', 'KOTAKBANK', 'LTF', 'LICHSGFIN', 'LTIM', 'LT', 'LAURUSLABS', 'LICI', 'LUPIN', 'LODHA', 'MGL', 'M&MFIN', 'M&M', 'MANAPPURAM', 'MANKIND', 'MARICO', 'MARUTI', 'MFSL', 'MAXHEALTH', 'MAZDOCK', 'MPHASIS', 'MCX', 'MUTHOOTFIN', 'NBCC', 'NCC', 'NHPC', 'NMDC', 'NTPC', 'NATIONALUM', 'NESTLEIND', 'OBEROIRLTY', 'ONGC', 'PAYTM', 'OFSS', 'POLICYBZR', 'PGEL', 'PIIND', 'PNBHOUSING', 'PAGEIND', 'PATANJALI', 'PERSISTENT', 'PETRONET', 'PIDILITIND', 'PEL', 'PPLPHARMA', 'POLYCAB', 'POONAWALLA', 'PFC', 'POWERGRID', 'PRESTIGE', 'PNB', 'RBLBANK', 'RECLTD', 'RVNL', 'RELIANCE', 'SBICARD', 'SBILIFE', 'SHREECEM', 'SJVN', 'SRF', 'MOTHERSON', 'SHRIRAMFIN', 'SIEMENS', 'SOLARINDS', 'SONACOMS', 'SBIN', 'SAIL', 'SUNPHARMA', 'SUPREMEIND', 'SYNGENE', 'TATACONSUM', 'TITAGARH', 'TVSMOTOR', 'TATACHEM', 'TATACOMM', 'TCS', 'TATAELXSI', 'TATAMOTORS', 'TATAPOWER', 'TATASTEEL', 'TATATECH', 'TECHM', 'FEDERALBNK', 'INDHOTEL', 'PHOENIXLTD', 'TITAN', 'TORNTPHARM', 'TORNTPOWER', 'TRENT', 'TIINDIA', 'UNOMINDA', 'UPL', 'ULTRACEMCO', 'UNIONBANK', 'UNITDSPR', 'VBL', 'VEDL', 'IDEA', 'VOLTAS', 'WIPRO', 'YESBANK', 'ZYDUSLIFE']

def fetch_historical_data(stock, period="3mo", interval="1d"):
    try:
        df = yf.Ticker(stock + ".NS").history(period=period, interval=interval)
        return df[['Open', 'High', 'Low', 'Close']] if not df.empty else None
    except Exception as e:
        print(f"Error fetching data for {stock}: {e}")
        update_error_status(True, "data", f"Data fetch error for {stock}: {e}")
        return None

def calculate_weekly_zones(data):
    df = data.resample('W').agg({'Open': 'first', 'High': 'max', 'Low': 'min'}).dropna()
    rng5, rng10 = (df['High'] - df['Low']).rolling(5).mean(), (df['High'] - df['Low']).rolling(10).mean()
    base = df['Open']
    u1, u2 = base + 0.5 * rng5, base + 0.5 * rng10
    l1, l2 = base - 0.5 * rng5, base - 0.5 * rng10
    return pd.DataFrame({'u1': u1, 'u2': u2, 'l1': l1, 'l2': l2})

def calculate_multi_day_zones(data, days):
    df = data.tail(days)
    if df.empty or len(df) < days: return None
    return {'zone_low': df['Low'].min(), 'zone_high': df['High'].max()}

def run_zone_scan(scan_type="AUTO"):
    try:
        now_ist = datetime.now(pytz.timezone('Asia/Kolkata'))
        should_scan, current_nifty = should_trigger_scan()
        if not should_scan and scan_type == "AUTO":
            print(f"⏸️ [{now_ist.strftime('%I:%M:%S %p')}] Scan skipped - NIFTY price unchanged")
            return
        with mode_lock: current_mode = SCAN_MODE
        print(f"\n🔄 [{now_ist.strftime('%I:%M:%S %p')}] Starting {scan_type} scan in '{current_mode}' mode... (Processing {len(fno_stocks)} stocks)")
        if current_nifty:
            print(f"📊 NIFTY Current: {current_nifty:.2f}")
            save_nifty_cache(current_nifty)
        historical_data = load_historical_data()
        intraday_alerts = load_intraday_alerts()
        all_supply_broken, all_demand_broken = [], []
        scan_time_str = now_ist.strftime('%Y-%m-%d %I:%M:%S %p')
        for i, stock in enumerate(fno_stocks):
            try:
                historical_df = fetch_historical_data(stock)
                if historical_df is None or historical_df.empty: continue
                print(f"  Scanning {stock} ({i+1}/{len(fno_stocks)})", end='\r')
                try:
                    live_price = yf.Ticker(stock + ".NS").fast_info['last_price']
                except Exception:
                    live_price = historical_df['Close'].iloc[-1]
                latest_price = round(live_price, 2)
                if current_mode == "Intraday":
                    weekly_zones = calculate_weekly_zones(historical_df)
                    if weekly_zones.empty or len(weekly_zones) < 2: continue
                    last_zone = weekly_zones.dropna().iloc[-1]
                    umin, umax = min(last_zone['u1'], last_zone['u2']), max(last_zone['u1'], last_zone['u2'])
                    lmin, lmax = min(last_zone['l1'], last_zone['l2']), max(last_zone['l1'], last_zone['l2'])
                else:
                    zones = calculate_multi_day_zones(historical_df, 2)
                    if zones is None: continue
                    umin, umax = zones['zone_low'], zones['zone_high']
                    lmin, lmax = zones['zone_low'], zones['zone_high']
                if latest_price > umax:
                    is_fresh = is_fresh_breakout(stock, "supply", historical_data)
                    is_alerted_today = any(a.get("stock") == stock and a.get("type") == "SUPPLY" for a in intraday_alerts)
                    if (current_mode == "Intraday" and is_fresh and not is_alerted_today) or current_mode != "Intraday":
                        all_supply_broken.append({ 'Stock': stock, 'Price': latest_price, 'Supply Low': umin, 'Supply High': umax, 'Time': scan_time_str, 'Lot Size': lot_sizes.get(stock, '-') })
                if latest_price < lmin:
                    is_fresh = is_fresh_breakout(stock, "demand", historical_data)
                    is_alerted_today = any(a.get("stock") == stock and a.get("type") == "DEMAND" for a in intraday_alerts)
                    if (current_mode == "Intraday" and is_fresh and not is_alerted_today) or current_mode != "Intraday":
                        all_demand_broken.append({ 'Stock': stock, 'Price': latest_price, 'Demand Low': lmin, 'Demand High': lmax, 'Time': scan_time_str, 'Lot Size': lot_sizes.get(stock, '-') })
            except Exception as e:
                print(f"\nERROR processing stock {stock}: {e}")
                update_error_status(True, "data", f"Stock processing error: {stock}")
        print(f"\n✅ [{datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M:%S %p')}] {scan_type} Scan Complete: Found {len(all_supply_broken)} Supply Breakouts and {len(all_demand_broken)} Demand Breakdowns.")
        save_historical_data({"supply_zones": all_supply_broken, "demand_zones": all_demand_broken}, current_mode)
        if all_supply_broken or all_demand_broken:
            new_alerts = [{"stock": s['Stock'], "type": "SUPPLY", "price": s['Price']} for s in all_supply_broken]
            new_alerts.extend([{"stock": d['Stock'], "type": "DEMAND", "price": d['Price']} for d in all_demand_broken])
            save_intraday_alerts(intraday_alerts + new_alerts)
        try:
            if all_supply_broken:
                pd.DataFrame(all_supply_broken).to_excel("weekly_supply_broken.xlsx", index=False)
                send_zone_alert("Supply Broken", all_supply_broken, "Supply")
            elif os.path.exists("weekly_supply_broken.xlsx"): os.remove("weekly_supply_broken.xlsx")
        except Exception as e:
            print(f"❌ ERROR writing to weekly_supply_broken.xlsx. It might be open. {e}")
        try:
            if all_demand_broken:
                pd.DataFrame(all_demand_broken).to_excel("weekly_demand_broken.xlsx", index=False)
                send_zone_alert("Demand Broken", all_demand_broken, "Demand")
            elif os.path.exists("weekly_demand_broken.xlsx"): os.remove("weekly_demand_broken.xlsx")
        except Exception as e:
            print(f"❌ ERROR writing to weekly_demand_broken.xlsx. It might be open. {e}")
        update_error_status(False)
    except Exception as e:
        print(f"❌ Zone scan error: {e}")
        update_error_status(True, "data", f"Zone scan failed: {e}")

def main():
    print("🚀 FiFTO Scanner Initialized")
    print("📊 Features:")
    print("   - Live Zone Breakout/Breakdown Scanning")
    print("   - Clickable stat cards for quick navigation")
    print("   - Telegram alerts with direct web links")
    print("   - Fund Momentum Indicator (FMI)")
    fmi_thread = threading.Thread(target=update_fmi_data_periodically, daemon=True)
    fmi_thread.start()
    server_thread = threading.Thread(target=start_web_server, daemon=True)
    server_thread.start()
    time.sleep(2)
    print("📊 Running initial zone scan...")
    run_zone_scan(scan_type='INITIAL')
    print("\n✅ FiFTO Scanner is running!")
    print("   -> Web Dashboard: https://fifto-scanner.onrender.com")
    print("\nPress Ctrl+C to stop the scanner.")
    time_since_last_scan = 0
    try:
        while True:
            ist_tz = pytz.timezone('Asia/Kolkata')
            now = datetime.now(ist_tz)
            with interval_lock: current_interval = SCAN_INTERVAL
            if current_interval > 0:
                time_since_last_scan += 1
                if time_since_last_scan >= current_interval:
                    run_zone_scan(scan_type='AUTO')
                    time_since_last_scan = 0
            else:
                time_since_last_scan = 0
            report_time = now.replace(hour=16, minute=0, second=0, microsecond=0)
            last_report_file = "last_report_date.txt"
            last_sent_date_str = ""
            if os.path.exists(last_report_file):
                with open(last_report_file, 'r') as f:
                    last_sent_date_str = f.read().strip()
            if now >= report_time and last_sent_date_str != now.strftime('%Y-%m-%d'):
                print(f"🕒 [{now.strftime('%I:%M:%S %p')}] Time to send daily report...")
                send_daily_telegram_report()
                with open(last_report_file, 'w') as f:
                    f.write(now.strftime('%Y-%m-%d'))
                print("✅ Daily report sent. Will not send again today.")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 FiFTO Scanner stopped by user.")

if __name__ == "__main__":
    main()
