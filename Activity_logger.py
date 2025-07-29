import psutil
import sqlite3
import time
import threading
from datetime import datetime
from plyer import notification
import tkinter as tk
from tkinter import scrolledtext

# Database setup
conn = sqlite3.connect("logger.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS process_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    process_name TEXT,
    timestamp TEXT
)
""")
conn.commit()

# Suspicious keywords
suspicious_keywords = ["keylogger", "wireshark", "sniffer", "nmap", "malware"]

# Logging flag
logging_active = False

# Log function
def log_processes():
    global logging_active
    while logging_active:
        for proc in psutil.process_iter(['name']):
            try:
                pname = proc.info['name']
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO process_logs (process_name, timestamp) VALUES (?, ?)", (pname, timestamp))
                if any(s in pname.lower() for s in suspicious_keywords):
                    notification.notify(
                        title="Suspicious Process Detected",
                        message=f"{pname} is running!",
                        timeout=4
                    )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        conn.commit()
        time.sleep(60)  # every 60 seconds

# Start/stop handlers
def start_logging():
    global logging_active
    if not logging_active:
        logging_active = True
        thread = threading.Thread(target=log_processes)
        thread.daemon = True
        thread.start()
        log_output.insert(tk.END, "🟢 Logging started...\n")

def stop_logging():
    global logging_active
    logging_active = False
    log_output.insert(tk.END, "🔴 Logging stopped.\n")

def show_logs():
    log_output.delete(1.0, tk.END)
    cursor.execute("SELECT * FROM process_logs ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    for row in rows:
        log_output.insert(tk.END, f"[{row[2]}] {row[1]}\n")

# GUI Setup
window = tk.Tk()
window.title("Digital Footprint Logger")
window.geometry("600x400")

btn_start = tk.Button(window, text="Start Logging", command=start_logging, bg='green', fg='white')
btn_start.pack(pady=5)

btn_stop = tk.Button(window, text="Stop Logging", command=stop_logging, bg='red', fg='white')
btn_stop.pack(pady=5)

btn_show = tk.Button(window, text="Show Last 10 Logs", command=show_logs)
btn_show.pack(pady=5)

log_output = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=15)
log_output.pack(padx=10, pady=10)

window.mainloop()
