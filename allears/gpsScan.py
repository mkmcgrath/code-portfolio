import socket
import json
import time

# GPSD is necessary to get this software working.
# At this point, only GPSD is supported, thus limiting the execution of this software to Linux systems.
# In order to execute this software on your system, tweaks may need to be made.
# I am currently in the process of making this code more distribution-agnostic.


def scan_gps():
    try:
        gpsd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gpsd_socket.connect(
            ("localhost", 2947)
        )  # Connect to gpsd server (NEEDS TO BE INITIALIZED PRIOR TO CODE EXECUTION)

        gpsdata = None  # Initialize gpsdata to None

        for _ in range(50):  # 5 retries before exiting with error.
            gpsd_socket.sendall(b'?WATCH={"enable":true, "json":true};\r\n')
            time.sleep(1)

            data = gpsd_socket.recv(4096).decode("utf-8")

            for line in data.splitlines():
                if line.strip():
                    try:
                        data = json.loads(line)
                        # print(json.dumps(data, indent=2))  # uncomment for debugging

                        if data.get("class") == "TPV":
                            mode = data.get("mode", 0)
                            if mode > 1:  # Fix acquired
                                print("GPS Fix Acquired:")
                                latitude = data.get("lat")
                                longitude = data.get("lon")
                                altitude = data.get("alt")
                                speed = data.get("speed")
                                track = data.get("track")
                                time_data = data.get("time")

                                gpsdata = [
                                    latitude,
                                    longitude,
                                    altitude,
                                    speed,
                                    track,
                                    time_data,
                                ]

                                print(
                                    f"  Latitude: {latitude}"
                                )  # Print only if available
                                print(f"  Longitude: {longitude}")
                                print(f"  Altitude: {altitude}")
                                print(f"  Speed: {speed}")
                                print(f"  Track: {track}")
                                print(f"  Time: {time_data}")

                                return gpsdata  # Return immediately after getting a fix

                            elif mode < 2:  # No fix yet
                                print("No Fix. Waiting...")
                                # Don't return yet, continue trying

                    except json.JSONDecodeError:
                        print("Invalid JSON data received from gpsd.")

        print("No GPS fix acquired after multiple tries.")  # Error message
        return None  # Return None if no fix after all tries

    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None on error
    finally:
        if gpsd_socket:  # Close the socket in the finally block
            gpsd_socket.close()
