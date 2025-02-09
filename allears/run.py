import os
import sys
import sqlite3
import json
import pywifi
from datetime import datetime
from time import sleep
from gpsScan import scan_gps
from loadingScreen import loading
import curses


def ensure_root():  # Make sure user has root
    if os.geteuid() != 0:
        print("This script must be run as root. Attempting to re-run with sudo...")
        os.execvp("sudo", ["sudo", sys.executable] + sys.argv)


def setup_database(db_name="wifi_networks.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS networks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ssid TEXT,
            bssid TEXT,
            signal INTEGER,
            frequency INTEGER,
            auth INTEGER,
            akm INTEGER,
            cipher INTEGER,
            timestamp TEXT,
            longitude FLOAT,
            latitude FLOAT,
            altitude FLOAT
        )
    """)
    conn.commit()
    return conn


def interface_scan():
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()

    if not interfaces:
        print("No WiFi interfaces found.")
        return None

    iface = interfaces[0]  # Assume the first interface is the one to use
    iface.scan()
    print("Scanning for networks...")

    results = iface.scan_results()
    return results


def save_to_database(cursor, networks, gpsdata):
    for network in networks:
        akm_serialized = json.dumps(network.akm)  # Serialize the AKM list
        cursor.execute(
            """
            INSERT INTO networks (ssid, bssid, signal, frequency, auth, akm, cipher, timestamp, longitude, latitude, altitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                network.ssid,
                network.bssid,
                network.signal,
                network.freq,
                network.auth,
                akm_serialized,  # Store the serialized list
                network.cipher,
                datetime.now().isoformat(),
                gpsdata[0],
                gpsdata[1],
                gpsdata[2],
            ),
        )


def display_networks(networks, gpsdata):
    # Get terminal dimensions
    # rows, columns = os.get_terminal_size()
    rows, columns = 80, 24

    # Define column widths based on content and terminal size
    column_widths = [
        min(20, columns // 1),  # SSID
        min(23, columns // 7),  # BSSID
        min(12, columns // 3),  # Signal
        min(16, columns // 7),  # Frequency
        min(12, columns // 6),  # Auth
        min(12, columns // 4),  # AKM
        min(15, columns // 3),  # Cipher
        min(30, columns // 3),  # Longitude
        min(30, columns // 3),  # Latitude
        min(16, columns // 4),  # Altitude
    ]

    # Create separator line
    # separator = "+-" + "-+".join(["-" * w for w in column_widths]) + "-+"
    print()
    print("TO EXIT, PRESS CTRL+C")
    print()
    separator = "_________________________________________________________________________________________"

    # Print header row
    print(separator)
    print(
        "| {:^{}} | {:^{}} | {:^{}} | {:^{}} | {:^{}} | {:^{}} | {:^{}} | {:^{}} | {:^{}} | {:^{}} |".format(
            "SSID",
            column_widths[0],
            "      BSSID      ",
            column_widths[1],
            "Signal",
            column_widths[2],
            "Freq",
            column_widths[3],
            "Auth",
            column_widths[4],
            " AKM ",
            column_widths[5],
            "Cipher",
            column_widths[6],
            "Longitude",
            column_widths[7],
            "Latitude",
            column_widths[8],
            "Altitude",
            column_widths[9],
        ),
        print(),
    )
    print(separator)

    # Print network data rows
    for network in networks:
        akm_string = network.akm  # Assume it's a string initially
        if isinstance(network.akm, list):  # Check if it's actually a list
            akm_string = ", ".join(str(x) for x in network.akm)  # Join list elements

        print(
            "| {:^{}} | {:^{}} | {:^{}} | {:^{}} | {:^{}} | {:^{}} | {:^{}} |".format(
                network.ssid,
                column_widths[0],
                network.bssid,
                column_widths[1],
                network.signal,
                column_widths[2],
                network.freq,
                column_widths[3],
                network.auth,
                column_widths[4],
                akm_string,
                column_widths[5],
                network.cipher,
                column_widths[6],
                gpsdata[0],
                column_widths[7],
                gpsdata[1],
                column_widths[8],
                gpsdata[2],
                column_widths[9],
            )
        )


def main():
    ensure_root()
    curses.wrapper(loading)
    conn = setup_database()
    cursor = conn.cursor()

    try:
        while True:
            networks = interface_scan()
            gpsdata = scan_gps()

            if networks is None:
                print("No networks found.")
            else:
                os.system("clear")  # Clear the screen
                display_networks(networks, gpsdata)

            sleep(6)  # Introduce a short delay

    except KeyboardInterrupt:
        print("\nScanning stopped by user (Ctrl+C).")

    finally:
        # Save to database before exiting
        save_to_database(cursor, networks, gpsdata)
        conn.commit()
        conn.close()
        print("Wi-Fi scan complete.")


if __name__ == "__main__":
    main()
