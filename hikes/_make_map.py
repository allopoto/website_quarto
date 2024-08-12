from pathlib import Path

import gpxpy
from ipyleaflet import Map, Marker, Polyline
from ipywidgets import Layout

AMS = (2.377956, 4.897070)


def parse_gpx(file_path: Path) -> list[tuple[float, float]]:
    gpx = gpxpy.parse(file_path.read_text())

    # Extract the first track in the GPX file
    track = gpx.tracks[0]
    segment = track.segments[0]

    # Extract coordinates from the segment
    coordinates = [(point.latitude, point.longitude) for point in segment.points]
    return coordinates


def load_coords(dir_path: Path) -> list[tuple[float, float]]:
    coords = []
    for file_path in sorted(dir_path.glob("*.gpx")):
        coords.extend(parse_gpx(file_path))
    return coords


dpath = Path("deadly-shenanigans")
coords = load_coords(dpath)
m = Map(center=AMS, zoom=2, scroll_wheel_zoom=True, layout=Layout(height="600px"))
gpx_track = Polyline(locations=coords, color="blue", fill=False, opacity=0.7)
gpx_marker = Marker(location=coords[0], draggable=False)

m.add_layer(gpx_track)
m.add_layer(gpx_marker)
m
