import time
import math
import csv
import krpc

# НАСТРОЙКИ
DURATION = 460.0     
DT = 0.1             
CSV_FILE = "data.csv"

def vec_mag(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

def main():
    conn = krpc.connect(name="logger_CSV")
    sc = conn.space_center
    vessel = sc.active_vessel
    body = vessel.orbit.body

    rf_surface = body.reference_frame
    rf_orbital = body.non_rotating_reference_frame

    flight = vessel.flight(rf_surface)

    t0 = sc.ut

    # Данные
    rows = []

    while True:
        ut = sc.ut
        t = ut - t0
        if t > DURATION:
            break

        # Скорости
        surface_speed = vec_mag(vessel.velocity(rf_surface))
        orbital_speed = vec_mag(vessel.velocity(rf_orbital))

        # Параметры полёта
        altitude = flight.mean_altitude
        pitch = flight.pitch
        mass = vessel.mass

        rows.append([
            t,
            surface_speed,
            orbital_speed,
            altitude,
            pitch,
            mass
        ])

        time.sleep(DT)

    # СОХРАНЕНИЕ CSV
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "t_sec",
            "surface_speed_mps",
            "orbital_speed_mps",
            "altitude_m",
            "pitch_deg",
            "mass_t"
        ])
        writer.writerows(rows)

if __name__ == "__main__":
    main()
