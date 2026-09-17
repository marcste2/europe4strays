# -*- coding: utf-8 -*-
"""Render the two location maps as static images from OpenStreetMap tiles.

The site used to embed Google Maps iframes, which send every visitor's IP
address to Google before they have clicked anything. The maps were never
interactive (the whole frame is one link to Google Maps), so a picture does
the same job with no third-party request at all.

Run once; re-run only if a location changes:
    python tools/build-maps.py

Tiles: (c) OpenStreetMap contributors, shown on the page as required.
"""
import io
import math
import time
import urllib.request

from PIL import Image

UA = "Europe4strays-website-build/1.0 (static map render, one-off)"
W, H = 800, 400          # 1x pixels; the page shows it unscaled and crops the centre

MAPS = [
    # name, lat, lon, zoom  (same view the Google embeds used)
    ("map-address", 45.9542894, 27.1047129, 13),   # Strada Maresal Constantin Prezan, Movilita
    ("map-shelter", 45.957137, 27.121161, 14),     # the Cheerful Kindergarten
]


def world_px(lat, lon, z):
    n = 256 * 2 ** z
    x = (lon + 180.0) / 360.0 * n
    s = math.sin(math.radians(lat))
    y = (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n
    return x, y


def tile(z, x, y, cache={}):
    key = (z, x, y)
    if key not in cache:
        url = "https://tile.openstreetmap.org/%d/%d/%d.png" % (z, x, y)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            cache[key] = Image.open(io.BytesIO(r.read())).convert("RGB")
        time.sleep(0.25)   # be polite to the tile servers
    return cache[key]


for name, lat, lon, z in MAPS:
    cx, cy = world_px(lat, lon, z)
    left, top = int(round(cx - W / 2)), int(round(cy - H / 2))
    out = Image.new("RGB", (W, H))
    for ty in range(top // 256, (top + H - 1) // 256 + 1):
        for tx in range(left // 256, (left + W - 1) // 256 + 1):
            out.paste(tile(z, tx, ty), (tx * 256 - left, ty * 256 - top))
    path = "assets/%s.webp" % name
    out.save(path, "WEBP", quality=86, method=6)
    print("%s  z%d  %dx%d  -> %s" % (name, z, W, H, path))
