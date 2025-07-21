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
import pytz # MODIFIED FOR IST: Import the pytz library

# Configuration
bot_token = "7657983245:AAEx45-05EZOKANiaEnJV9M4V1zeKqaSgBMSUM"
chat_id = "-4913116305df"

# --- (The large 'lot_sizes' dictionary and other global variables remain unchanged) ---
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

# --- (All functions from update_error_status to serve_alerts remain the same) ---
# ...
# The code for functions like run_fmi_scan, ZoneScannerWebUI, etc. is correct and doesn't need to be repeated here.
# The key changes are in functions that generate timestamps.
# ...

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
    # MODIFIED FOR IST: Get current time in 'Asia/Kolkata' timezone
    ist_tz = pytz.timezone('Asia/Kolkata')
    ist_time = datetime.now(ist_tz)
    
    lot_size = lot_sizes.get(stock, '-')
    alert = {
        'timestamp': ist_time.isoformat(), # Use the timezone-aware time
        'stock': stock, 'price': price, 'zone_low': zone_low,
        'zone_high': zone_high, 'type': zone_type, 'action': action,
        'lot_size': lot_size
    }
    alert_file = "today_alerts.json"
    alerts = []
    # MODIFIED FOR IST: Check file date using timezone-aware object
    if not os.path.exists(alert_file) or datetime.fromtimestamp(os.path.getmtime(alert_file), tz=ist_tz).date() != ist_time.date():
         with open(alert_file, 'w') as f: json.dump([], f)
    try:
        with open(alert_file, 'r') as f: alerts = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError): pass
    alerts.append(alert)
    with open(alert_file, 'w') as f: json.dump(alerts, f, indent=2)

# --- (send_telegram_message and send_daily_telegram_report remain the same) ---

def send_zone_alert(title, data, zone_type):
    # MODIFIED FOR IST: Get current time and date in 'Asia/Kolkata' timezone
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
        # MODIFIED FOR IST: Use the already fetched IST time
        alert_time = now_ist.strftime('%d-%b-%Y %I:%M %p')

        # ... (rest of the function remains the same)
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
        
        telegram_message = (
            f"<b>{header}</b>\n\n"
            f"📊 <b>Stock:</b> {stock_link}\n"
            f"💰 <b>Price:</b> ₹{price:.2f}\n"
            f"🎯 <b>Zone:</b> ₹{zone_low:.2f} - ₹{zone_high:.2f}\n"
            f"📏 <b>Range:</b> {zone_range_pct:.1f}% | {zone_status}\n"
            f"📦 <b>Lot Size:</b> {lot_size}\n"
            f"🕒 <b>Time:</b> {alert_time}"
        )

        send_telegram_message(telegram_message)
        save_alert_to_json(stock, price, zone_low, zone_high, alert_type, action)
        print(f"🚨 {alert_type} Alert: {stock} @ ₹{price:.2f} | Lot: {lot_size} | {zone_status}")

        try:
            with open(memory_file, 'a') as f_append: f_append.write(stock + '\n')
            notified_today.add(stock)
        except Exception as e:
            print(f"Error writing to notification memory file: {e}")

# ...
# The `fno_stocks` list and data fetching/zone calculation functions remain the same.
# The key change is in `run_zone_scan` where it records the time.
# ...

def run_zone_scan(scan_type="AUTO"):
    try:
        should_scan, current_nifty = should_trigger_scan()
        if not should_scan and scan_type == "AUTO":
            print(f"⏸️ [{datetime.now().strftime('%I:%M:%S %p')}] Scan skipped - NIFTY price unchanged")
            return

        with mode_lock: current_mode = SCAN_MODE
        print(f"\n🔄 [{datetime.now().strftime('%I:%M:%S %p')}] Starting {scan_type} scan in '{current_mode}' mode... (Processing {len(fno_stocks)} stocks)")
        
        if current_nifty:
            print(f"📊 NIFTY Current: {current_nifty:.2f}")
            save_nifty_cache(current_nifty)
        
        historical_data = load_historical_data()
        intraday_alerts = load_intraday_alerts()
        all_supply_broken, all_demand_broken = [], []
        
        # MODIFIED FOR IST: Get the current time once for all alerts in this scan
        ist_tz = pytz.timezone('Asia/Kolkata')
        scan_time_str = datetime.now(ist_tz).strftime('%Y-%m-%d %I:%M:%S %p')

        for i, stock in enumerate(fno_stocks):
            try:
                # ... (inner loop logic is the same)
                historical_df = fetch_historical_data(stock)
                if historical_df is None or historical_df.empty: continue
                print(f"  Scanning {stock} ({i+1}/{len(fno_stocks)})", end='\r')
                try:
                    live_price = yf.Ticker(stock + ".NS").fast_info['last_price']
                except Exception:
                    live_price = historical_df['Close'].iloc[-1]
                latest_price = round(live_price, 2)
                
                # ... (zone calculation logic is the same)
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
                        all_supply_broken.append({
                            'Stock': stock, 'Price': latest_price, 'Supply Low': umin, 'Supply High': umax,
                            'Time': scan_time_str, # MODIFIED FOR IST: Use consistent IST time
                            'Lot Size': lot_sizes.get(stock, '-')
                        })

                if latest_price < lmin:
                    is_fresh = is_fresh_breakout(stock, "demand", historical_data)
                    is_alerted_today = any(a.get("stock") == stock and a.get("type") == "DEMAND" for a in intraday_alerts)
                    if (current_mode == "Intraday" and is_fresh and not is_alerted_today) or current_mode != "Intraday":
                        all_demand_broken.append({
                            'Stock': stock, 'Price': latest_price, 'Demand Low': lmin, 'Demand High': lmax,
                            'Time': scan_time_str, # MODIFIED FOR IST: Use consistent IST time
                            'Lot Size': lot_sizes.get(stock, '-')
                        })
            except Exception as e:
                print(f"\nERROR processing stock {stock}: {e}")
                update_error_status(True, "data", f"Stock processing error: {stock}")

        # ... (rest of the function is the same)
        print(f"\n✅ [{datetime.now().strftime('%I:%M:%S %p')}] {scan_type} Scan Complete: Found {len(all_supply_broken)} Supply Breakouts and {len(all_demand_broken)} Demand Breakdowns.")
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
    # ... (startup messages are the same)
    
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
            # MODIFIED FOR IST: Use timezone aware objects for checking report time
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
