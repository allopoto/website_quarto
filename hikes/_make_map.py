# %%
from pathlib import Path
from typing import Iterable

import gpxpy
from ipyleaflet import Map, Marker, MarkerCluster, Polyline
from ipywidgets import HTML, Layout

AMS = (2.377956, 4.897070)


# %%


def valid(p: Path) -> bool:
    if p.stem.startswith("."):
        return False
    if p.is_dir():
        return True
    return False


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


def make_tracks(segment_coords: Iterable[list[tuple[float, float]]]) -> list[Polyline]:
    tracks = []
    for i, segment in enumerate(segment_coords):
        gpx_track = Polyline(
            locations=segment,
            color="blue" if i % 2 == 0 else "green",
            fill=False,
            opacity=0.7,
            scaling=False,
            rotations=False,
        )
        tracks.append(gpx_track)
    return tracks


# %%
m = Map(center=AMS, zoom=2, scroll_wheel_zoom=True, layout=Layout(height="600px"))

dirs = [d for d in Path("hikes-gpx").iterdir() if valid(d)]
markers = []
for dpath in dirs:
    segment_coords = [parse_gpx(fpath) for fpath in sorted(dpath.glob("*.gpx"))]
    tracks = make_tracks(segment_coords)
    for track in tracks:
        m.add(track)
    # gpx_track = Polyline(locations=coords, color="blue", fill=False, opacity=0.7)
    gpx_marker = Marker(location=segment_coords[0][0], draggable=False)
    if (Path("posts") / (dpath.stem + ".qmd")).exists():
        hike_name = dpath.stem.replace("-", " ").title()
        popup_html = f"""
        <h3>{hike_name}</h3>
        <a href="/hikes/posts/{dpath.stem}.html">View Details</a>
        """
        gpx_marker.popup = HTML(popup_html)

    # m.add(gpx_track)
    markers.append(gpx_marker)

m.add(MarkerCluster(markers=markers))

m

# %%
