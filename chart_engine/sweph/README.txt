# Ephemeris Data (not tracked in repo)

This folder contains Swiss Ephemeris data files used by the chart engine.

These files are required for Z13 Astrology's true sidereal chart calculations,
but are excluded from version control due to size.

You can download the required files here:
🔗 https://www.astro.com/ftp/swisseph/ephe/

After downloading, place them in this directory and set the path in `chart_builder.py`:
```python
swisseph.set_ephe_path("data/ephe/")