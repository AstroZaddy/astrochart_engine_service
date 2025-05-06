<<<<<<< HEAD
# chart_engine

A Python module for generating astronomical data for use in astrological charts.  
Given a date, time, and geographic location, this module returns core planetary and chart point positions in **absolute ecliptic longitude** (true sidereal).  

This project is designed to be used as a *non-interpretive backend engine* for astrology systems that handle sign and house assignment separately.

---

## Features

- Swiss Ephemeris integration (via `pyswisseph`)
- Returns:
  - Planetary longitudes
  - Ascendant, MC, IC, and Vertex points
  - Retrograde flags
  - Latitude, distance (AU), and velocity for each body
- Clean data output as Python dictionaries
- CLI and/or Jupyter notebook demo included
- Designed for sidereal/true sidereal systems, but adaptable to tropical if needed

---

## What This *Doesn't* Do

- No zodiac sign assignment (tropical or sidereal)
- No house calculations or interpretations
- No full chart rendering or graphical output

Interpretive or system-specific logic should be implemented downstream in separate modules.

---

## 🔧 Installation

```bash
pip install pyswisseph
```

Clone this repo and import as needed:

```python
from chart_engine import build_chart

chart = build_chart(
    date="2025-03-21",
    time="15:30",
    location={"lat": 53.5444, "lon": -113.4909}
)
```

---

## 📁 Structure

```
chart_engine/
│
├── chart_engine/          # Core logic
│   ├── chart_builder.py
│   └── __init__.py
│   └── sweph/             # Swiss Ephemeris data files
│       ├── seas_18.se1
│       ├── semo_18.se1
│       ├── sepl_18.se1
│       └── README.txt
├── tests/                 # Unit tests (optional)
├── notebooks/             # Demos + dev tools (optional)
├── README.md
├── LICENSE                # GPL-2.0 or later
└── .gitignore
```

To use this module, download Swiss Ephemeris data files from astro.com and place them in a folder named `sweph/` in the project root.

---

## Input Format for `build_chart()`

The function accepts a dictionary with the following keys:

```python
{
  "name": "Optional name",
  "date": "YYYY-MM-DD",      # required
  "time": "HH:MM",           # required
  "location": "City, Country" or dict with {"lat": float, "lon": float}
}
```

If the location cannot be resolved, it will default to `(0.0, 0.0)` UTC noon.

---

## Chart Output Format

The `build_chart()` function returns a dictionary containing birth data and raw astronomical placements.  
Each placement includes true sidereal coordinates and motion data, ideal for sidereal systems.

---

### 🔬 Sample Output for a Planet

```json
"Venus": {
  "longitude": 72.84,
  "latitude": 1.12,
  "distance_au": 0.72,
  "speed": -1.22,
  "retrograde": true
}
```

---

## License

This project is licensed under the GNU General Public License v2.0 or later (GPL-2.0+) to remain compatible with Swiss Ephemeris licensing terms.

You are free to use, modify, and redistribute this software under the terms of the GPL. See the LICENSE file for details.

---

## Acknowledgments

- This project uses the **Swiss Ephemeris** by Astrodienst AG  
- Python wrapper via **pyswisseph**

---

## Designed For

Projects like:
- True sidereal astrology platforms (Lahiri, Fagan-Bradley, etc.)
- Whole-sign house systems
- Educational or research tools
- Interpretive frameworks layered on top of raw planetary data
=======
# 🌠 Z13 Astrology · v0.7-beta

> **Real Sky. Real You.**  
> Astrology that reflects the sky *as it actually is* — not how it was 2,000 years ago.

Z13 Astrology is a true sidereal astrology platform built for clarity, precision, and transformation.  
This version marks our **first public beta release** — a fully working MVP that generates natal charts based on **real astronomical constellations**, using a **13-sign system** and **whole sign houses**.

---

## 📂 File Structure

```plaintext
├── api/
│   └── main.py           # FastAPI server routes
├── chart_engine/
│   └── chart_builder.py  # Core chart calculation logic (Z13 system)
├── webui/
│   ├── static/           # CSS, images, assets
│   │   ├── style.css
│   │   ├── z13_logo_gold.png
│   │   └── stars.png
│   ├── templates/
│   │   ├── partials/
│   │   │   ├── nav.html  # Reusable nav bar
│   │   │   └── footer.html
│   │   ├── landing.html
│   │   ├── form.html
│   │   ├── chart.html
│   │   ├── learn.html
│   │   ├── about.html
│   │   ├── subscribe.html
│   │   └── shop.html
├── requirements.txt      # Python dependencies
├── README.md              # This file
└── render.yaml (optional) # For cloud deployment config (Render.com, etc.)

##🚀 Current Features (v0.7-beta)

✅ Real Sky Chart Generation
✅ 13 Signs + Ophiuchus Included
✅ Whole Sign Houses
✅ Responsive Frontend (Mobile + Desktop)
✅ Alpine.js Mobile Navigation
✅ Chart Placements Listed with Retrograde Flags
✅ Starter Informational Pages (Learn, About, Subscribe, Shop)
✅ MVP Launch-Ready Website Structure
✅ Clean, Modular Jinja2 Templates
✅ FastAPI Backend, Static Asset Handling

⸻

## 🌌 Features in Development (v0.8+ Roadmap)

🚧 Email capture + PDF export of natal chart
🚧 Chart wheel diagram (Z13 sidereal version)
🚧 Substack newsletter & community integration
🚧 Swag / merch store (Printful/Printify)
🚧 Tip jar for donations (Ko-fi, Buy Me A Coffee)
🚧 Blog content import from Substack (RSS feed parsing)
🚧 Synastry charts (relationship astrology)
🚧 Transit and progression reporting
🚧 Premium readings and reports

⸻

🛠️ Tech Stack (Requirements)

Component | Stack | 
Backend | Python 3.11+, FastAPI
Frontend | TailwindCSS, Alpine.js, Jinja2 templates
Deployment Ready | Render, Fly.io, DigitalOcean
Chart Engine | Swiss Ephemeris backend (optional for later upgrades)
Optional Tools | WeasyPrint (for PDF export), Substack (newsletter), Stripe (future payments)

## Local Development Setup

Clone the repo
git clone https://github.com/your-username/z13-astrology.git
cd z13-astrology

Create a virtual environment
python -m venv venv
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Run the dev server:
uvicorn api.main:app --reload

Open in browser:
http://localhost:8000

## 📜 License

MIT — use freely, modify soulfully.

⸻

## ✨ Live Site

🔗 https://z13astrology.com (or deployment link once live)
🚀 Public beta is live — expect updates and stellar expansions soon!

⸻

## 💌 Credits

Created with cosmic precision by @astrozaddy.
Guided by the stars. Fueled by caffeine. Driven by truth.
>>>>>>> 1e4e0b7 (Initial import from backup)
