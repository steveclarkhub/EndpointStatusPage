from flask import Flask, render_template
from datetime import datetime
import socket
import time
import sqlite3


app = Flask(__name__)

# function for checking sites
def check_connectivity(host, port):
    try:
        # Using a short timeout to avoid blocking requests
        socket.setdefaulttimeout(1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.close()
        return True
    except Exception:
        return False

@app.route("/")
def index():
    now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    dns_reachable = check_connectivity("8.8.8.8", 54)
    google_reachable = check_connectivity("www.google.com", 443)
    return render_template("index.html", time=now, dns_reachable=dns_reachable, google_reachable=google_reachable)

if __name__ == "__main__":
    # # background check w/separate thread
    # def background_check():
    #     while True:
    #         time.sleep(60)
    #         # Perform checks and update results (not displayed on the page)
    #         check_connectivity("8.8.8.8", 53)
    #         check_connectivity("www.google.com", 443)

    # from threading import Thread
    # thread = Thread(target=background_check)
    # thread.daemon = True
    # thread.start()

    app.run(debug=True)