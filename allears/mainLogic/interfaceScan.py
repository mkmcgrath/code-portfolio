import os
import sys
import sqlite3
import json
import pywifi
from datetime import datetime
from time import sleep


def ensure_root():
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
            timestamp TEXT
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


def save_to_database(cursor, networks):
    for network in networks:
        akm_serialized = json.dumps(network.akm)  # Serialize the AKM list
        cursor.execute(
            """
            INSERT INTO networks (ssid, bssid, signal, frequency, auth, akm, cipher, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
            ),
        )


def display_networks(networks):
    # Get terminal dimensions
    rows, columns = os.get_terminal_size()

    # Define column widths based on content and terminal size
    column_widths = [
        min(15, columns // 7),  # SSID
        min(17, columns // 7),  # BSSID
        min(8, columns // 7),  # Signal
        min(11, columns // 7),  # Frequency
        min(8, columns // 7),  # Auth
        min(8, columns // 7),  # AKM
        min(10, columns // 7),  # Cipher
    ]

    # Create separator line
    separator = "+-" + "-+".join(["-" * w for w in column_widths]) + "-+"

    # Print header row
    print(separator)
    print(
        "| {:^{}} | {:^{}} | {:^{}} | {:^{}} | {:^{}} | {:^{}} | {:^{}} |".format(
            "SSID",
            column_widths[0],
            "BSSID",
            column_widths[1],
            "Signal",
            column_widths[2],
            "Frequency",
            column_widths[3],
            "Auth",
            column_widths[4],
            "AKM",
            column_widths[5],
            "Cipher",
            column_widths[6],
        )
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
            )
        )


def main():
    ensure_root()
    conn = setup_database()
    cursor = conn.cursor()

    try:
        while True:
            networks = interface_scan()
            if networks is None:
                print("No networks found.")
            else:
                os.system("clear")  # Clear the screen
                display_networks(networks)

            sleep(1.5)  # Introduce a short delay

    except KeyboardInterrupt:
        print("\nScanning stopped by user (Ctrl+C).")

    finally:
        # Save to database before exiting
        save_to_database(cursor, networks)
        conn.commit()
        conn.close()
        print("Wi-Fi scan complete.")


if __name__ == "__main__":
    main()

