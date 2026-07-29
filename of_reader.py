from pymavlink import mavutil
import csv
from math import sqrt
import os
from datetime import datetime

# Constants
HEIGHT = 1.2  # metres AGL
PORT = '/dev/ttymxc5'
BAUD = 115200
LOG_DIR = '/root/of_logs'

def main():
    os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'{LOG_DIR}/of_log_{timestamp}.csv'

    connection = mavutil.mavlink_connection(PORT, baud=BAUD)
    print(f"Connected to {PORT} at {BAUD} baud")
    print(f"Logging to {log_file}")
    print("Press Ctrl+C to stop\n")

    with open(log_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['TimeUS', 'flow_x', 'flow_y',
                         'speed_ms', 'quality'])

        try:
            while True:
                msg = connection.recv_match(type='OPTICAL_FLOW',
                                           blocking=True, timeout=2)
                if msg is None:
                    print("No message received, waiting...")
                    continue

                time_usec = msg.time_usec
                flow_x    = msg.flow_x      # raw pixels
                flow_y    = msg.flow_y      # raw pixels
                quality   = msg.quality

                # flow_comp_m_x/y are nan without rangefinder
                # so we compute speed from raw flow + known height
                # flow_x/y are in pixels — need sensor scale factor
                # PX4Flow scale: 1 pixel ~ 0.1 rad at 1m (approximate)
                SCALE = 0.1
                Vx = HEIGHT * flow_x * SCALE
                Vy = HEIGHT * flow_y * SCALE
                speed = sqrt(Vx**2 + Vy**2)

                print(f"TimeUS: {time_usec} | "
                      f"flowX: {flow_x} | flowY: {flow_y} | "
                      f"speed: {speed:.3f} m/s | quality: {quality}")

                writer.writerow([time_usec, flow_x, flow_y,
                                 round(speed, 4), quality])
                csvfile.flush()

        except KeyboardInterrupt:
            print(f"\nRecording stopped. Log saved to {log_file}")

if __name__ == "__main__":
    main()