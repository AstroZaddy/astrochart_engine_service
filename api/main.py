# chart_runner.py
# SPDX-License-Identifier: AGPL-3.0-or-later

# This file is part of astrochart-engine‑API.
#
# astrochart-engine‑API is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# …
# LICENSE document found at https://github.com/AstroZaddy/astrochart_engine_service.git

# SPDX-License-Identifier: AGPL-3.0-or-later
from typing import Any, Dict, Optional, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

from chart_engine import build_chart



# CORS — allow only your commercial domain to call this
from fastapi.middleware.cors import CORSMiddleware


# ------------ Pydantic Models ------------

class PlanetPlacement(BaseModel):
    longitude: float
    latitude: float
    distance_au: float
    speed: float
    retrograde: bool

class ChartResponse(BaseModel):
    name: Optional[str] = None
    datetime_utc: str
    latitude: float
    longitude: float
    julian_day: float
    placements: Dict[str, PlanetPlacement]
    # add any extra fields resulting from modification to build_chart returns,
    # e.g. aspects: List[Aspect], houses: Dict[str,float], etc.

class ChartRequest(BaseModel):
    name: Optional[str] = None
    datetime_utc: str # ISO 8601 ending in 'Z'
    latitude: float
    longitude: float


# ------------ FastAPI App ------------

app = FastAPI(
    title="AstroChart Engine Service",
    description="AGPL 3.0-or-later service wrapping chart_engine.build_chart()",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=[True],
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.mount(
    "/demo",
    StaticFiles(directory="docs", html=True),
    name="demo",
)

@app.post("/v1/build-chart", response_model=ChartResponse)

async def build_chart_endpoint(req: ChartRequest) -> ChartResponse:
    """
    Build a chart using chart_engine.build_chart().

    Accepts:
    - name (optional)
    - datetime_utc: ISO string, tz‑aware, ending in 'Z'
    - latitude: decimal degrees
    - longitude: decimal degrees

    Returns a ChartResponse with datetime and placements.
    """
    try:
        result = build_chart(req.dict())
        return ChartResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
