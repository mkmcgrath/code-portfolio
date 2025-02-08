# Overview

[Note: This software is to be used for reseearch purposes only. Please learn the law in your area and remember to use security applications ethically. I will not be responsible for potential misuse of this software. ]

**All Ears** is a simple terminal-based wardriving tool that scans nearby Wi-Fi networks and logs their details along with GPS coordinates. Using a GPS and Wi-Fi module, it collects metadata like SSID, signal strength, encryption type, and location as you move around. The data is stored in a Sqlite3 .db file by default for easy analysis and querying.

## Key Features

- Scan for Wi-Fi networks and capture metadata
- Log GPS coordinates with each network
- Export data in CSV format

This tool is useful for network research, security auditing, or mapping network distribution in a specific area. Just remember to use it ethically and within the boundaries of the law.

Video Demonstration Pending...
[Software Demo Video](http://youtube.link.goes.here)

# Development Environment

To develop this software, I used lazyvim on arch linux. The code (for now) is written in python.
Eventually, I would like to rewrite this program in C so it can run on weaker and embedded devices easier. I would also be open to integrating cython as well.

This software is open to contribitions! The code in it's current state while functional is rough around the edges. Any and all contributions are welcome!

# Useful Websites

- [What is Wardriving?](https://en.wikipedia.org/wiki/Wardriving)
