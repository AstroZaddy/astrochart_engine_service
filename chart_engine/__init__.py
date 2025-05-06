# chart_engine.py
# Licensed under the GNU GPL v2.0 or later
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2025 Rob Wall

import os
from datetime import datetime
import pytz
import swisseph as swe

# Set ephemeris path
EPHE_PATH = os.path.join(os.path.dirname(__file__), 'sweph')
swe.set_ephe_path(EPHE_PATH)

def detailed_format(pos):
    """Return detailed positional data for a celestial body."""
    lon, lat, dist, speed = pos[0], pos[1], pos[2], pos[3]
    return {
        "longitude": round(lon, 6),
        "latitude": round(lat, 6),
        "distance_au": round(dist, 6),
        "speed": round(speed, 6),
        "retrograde": speed < 0
    }

def build_chart(birth_data):
    """
    Generate core astronomical chart data for a given date, time, and location.
    Returns planetary longitudes, angles, and retrograde flags.
    """

    name = birth_data.get("name", "Unknown")
    birth_date = birth_data.get("date")
    birth_time = birth_data.get("time")
    location = birth_data.get("location", {})
    lat = location.get("lat", 0.0)
    lon = location.get("lon", 0.0)
    tz_str = location.get("timezone", "UTC")

    if lon > 180:
        lon -= 360

    try:
        dt_local = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
        local_tz = pytz.timezone(tz_str)
        dt_utc = local_tz.localize(dt_local).astimezone(pytz.utc)
    except Exception:
        dt_utc = pytz.utc.localize(datetime.strptime(f"{birth_date} 12:00", "%Y-%m-%d %H:%M"))

    jd = swe.julday(
        dt_utc.year,
        dt_utc.month,
        dt_utc.day,
        dt_utc.hour + dt_utc.minute / 60.0
    )

    chart = {
        "name": name,
        "birth_date": birth_date,
        "birth_time_local": birth_time,
        "latitude": lat,
        "longitude": lon,
        "timezone": tz_str,
        "julian_day": jd,
        "placements": {}
    }

    # Celestial bodies to include
    bodies = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mercury": swe.MERCURY,
        "Venus": swe.VENUS,
        "Mars": swe.MARS,
        "Jupiter": swe.JUPITER,
        "Saturn": swe.SATURN,
        "Uranus": swe.URANUS,
        "Neptune": swe.NEPTUNE,
        "Pluto": swe.PLUTO,
        "North Node": swe.MEAN_NODE,
        "Chiron": 15,
        "Lilith": swe.MEAN_APOG,
    }

    for name, code in bodies.items():
        pos, _ = swe.calc_ut(jd, code)
        chart["placements"][name] = detailed_format(pos)

    # South Node = opposite of North Node
    if "North Node" in chart["placements"]:
        nn_lon = chart["placements"]["North Node"]["longitude"]
        sn_lon = (nn_lon + 180) % 360
        chart["placements"]["South Node"] = {
            "longitude": round(sn_lon, 6),
            "latitude": 0.0,  # Not calculated
            "distance_au": 0.0,  # Not applicable
            "speed": 0.0,
            "retrograde": False
        }

    # House angles
    try:
        cusps, ascmc = swe.houses(jd, lat, lon, b"P")
        asc = ascmc[0]
        mc = ascmc[1]
        desc = (asc + 180) % 360
        ic = (mc + 180) % 360

        chart["placements"]["Ascendant"] = {
            "longitude": round(asc, 6),
            "latitude": 0.0,
            "distance_au": 0.0,
            "speed": 0.0,
            "retrograde": False
        }
        chart["placements"]["Midheaven"] = {
            "longitude": round(mc, 6),
            "latitude": 0.0,
            "distance_au": 0.0,
            "speed": 0.0,
            "retrograde": False
        }
        chart["placements"]["Descendant"] = {
            "longitude": round(desc, 6),
            "latitude": 0.0,
            "distance_au": 0.0,
            "speed": 0.0,
            "retrograde": False
        }
        chart["placements"]["IC"] = {
            "longitude": round(ic, 6),
            "latitude": 0.0,
            "distance_au": 0.0,
            "speed": 0.0,
            "retrograde": False
        }

    except Exception as e:
        chart["error"] = f"Houses/angles could not be calculated: {e}"

    return chart

if __name__ == "__main__":
    test_data = {
        "name": "Demo",
        "date": "2025-03-21",
        "time": "15:30",
        "location": {
            "lat": 53.54,
            "lon": -113.49,
            "timezone": "America/Edmonton"
        }
    }
    chart = build_chart(test_data)
    for point, data in chart["placements"].items():
        print(f"{point}: {data}")