# SPDX-License-Identifier: AGPL-3.0-or-later
"""
chart_engine module: Provides two core functions:
- build_charts(payload: dict) -> dict
- next_lunar_phases(input_dt: str or datetime) -> dict

build_charts computes planetary placements, Chiron, mean lunar node, mean apogee (Lilith),
ASC, MC, DC, IC based on a UTC datetime and location.
next_lunar_phases finds the next New Moon and Full Moon after a given UTC datetime.
"""
import os
from datetime import datetime
import swisseph as swe

# Initialize ephemeris path
ephe_path = os.path.join(os.path.dirname(__file__), "sweph")
swe.set_ephe_path(ephe_path)


def _parse_datetime(dt_input):
    """
    Parse an ISO8601 string ending in 'Z' or a datetime object, returning a naive UTC datetime.
    """
    if isinstance(dt_input, str):
        s = dt_input
        if s.endswith('Z'):
            s = s[:-1]
        try:
            return datetime.fromisoformat(s)
        except Exception as e:
            raise ValueError(f"Invalid datetime_utc: '{dt_input}'. Use 'YYYY-MM-DDTHH:MM:SSZ'.") from e
    elif isinstance(dt_input, datetime):
        return dt_input
    else:
        raise ValueError("datetime_utc must be an ISO8601 string ending in 'Z' or a datetime instance.")


def build_chart(payload: dict) -> dict:
    # 1. Parse and validate datetime
    dt = _parse_datetime(payload.get('datetime_utc', ''))

    # 2. Validate coordinates
    try:
        lat = float(payload.get('latitude'))
        if not -90.0 <= lat <= 90.0:
            raise ValueError
    except Exception:
        raise ValueError(f"Latitude must be between -90 and 90. Got: {payload.get('latitude')}.")
    try:
        lon = float(payload.get('longitude'))
        if not -180.0 <= lon <= 180.0:
            raise ValueError
    except Exception:
        raise ValueError(f"Longitude must be between -180 and 180. Got: {payload.get('longitude')}.")

    # 3. Compute Julian Day (UT)
    try:
        jd = swe.julday(
            dt.year, dt.month, dt.day,
            dt.hour + dt.minute/60 + dt.second/3600
        )
    except Exception as e:
        raise RuntimeError(f"Failed to compute Julian Day: {e}") from e

    # 4. Calculate planetary and minor body placements
    bodies = [
        swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
        swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO,
        swe.CHIRON, swe.MEAN_NODE, swe.MEAN_APOG  # Lilith (mean apogee)
    ]
    placements = {}
    for code in bodies:
        try:
            result = swe.calc_ut(jd, code)
        except Exception as e:
            name = swe.get_planet_name(code)
            raise RuntimeError(f"Failed to calculate {name}: {e}") from e
        # Unpack based on 2-element return (err, data) or direct 4-element tuple

        if isinstance(result, tuple) and len(result) == 2:
            # (data_array, error_code) in this environment
            data = result[0]
            lon_deg, lat_deg, dist, speed = data[0], data[1], data[2], data[3]
        else:
            # assume last four values are (lon, lat, dist, speed)
            lon_deg, lat_deg, dist, speed = result[-4], result[-3], result[-2], result[-1]

            # assume 4-element (lon, lat, dist, speed) or more
            lon_deg, lat_deg, dist, speed = result[-4], result[-3], result[-2], result[-1]
        placements[swe.get_planet_name(code)] = {
            'longitude': lon_deg,
            'latitude': lat_deg,
            'distance_au': dist,
            'speed': speed,
            'retrograde': speed < 0,
        }

    # 5. Compute house angles: ASC, MC, DC, IC
    try:
        cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P')  # 'P' = Placidus house system
        asc, mc = ascmc[0], ascmc[1]
        dc = (asc + 180.0) % 360.0
        ic = (mc + 180.0) % 360.0
    except Exception as e:
        raise RuntimeError(f"Failed to compute houses/angles: {e}") from e

    angles = {'Ascendant': asc, 'Midheaven': mc, 'Descendant': dc, 'IC': ic}
    for name, angle in angles.items():
        placements[name] = {'longitude': angle, 'latitude': 0.0, 'distance_au': 0.0, 'speed': 0.0, 'retrograde': False}

    # 6. Return the result dict
    return {
        'name': payload.get('name'),
        'datetime_utc': dt.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'latitude': lat,
        'longitude': lon,
        'julian_day': jd,
        'placements': placements,
    }


