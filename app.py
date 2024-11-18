from flask import Flask, render_template
from datetime import datetime
import socket
import time
import sqlite3


app = Flask(__name__)

# function for checking sites
def check_connectivity(host, port):
    try:
        socket.setdefaulttimeout(1)  # too short?
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.close()
        return True
        result = "Success"
    except Exception:
        return False
        result = "Fail"

    # Send to SQLite
    conn = sqlite3.connect('connectivity_log.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (timestamp, host, port, result) VALUES (?, ?, ?, ?)",
                   (datetime.now(), host, port, result))
    conn.commit()
    conn.close()

    return result

# Initial database setup (run once)
def initialize_database():
    conn = sqlite3.connect('connectivity_log.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs
                   (timestamp TEXT, host TEXT, port INTEGER, result TEXT)''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    dns_reachable = check_connectivity("8.8.8.8", 54)
    google_reachable = check_connectivity("www.google.com", 444)
    return render_template("index.html", time=now, dns_reachable=dns_reachable, google_reachable=google_reachable)

if __name__ == "__main__":
    initialize_database()  # Initialize the database 
    # # port check w/separate thread running in background
    # def background_check():
    #     while True:
    #         time.sleep(60)
    #         check_connectivity("8.8.8.8", 53)
    #         check_connectivity("www.google.com", 443)

    # from threading import Thread
    # thread = Thread(target=background_check)
    # thread.daemon = True
    # thread.start()

    app.run(debug=True)