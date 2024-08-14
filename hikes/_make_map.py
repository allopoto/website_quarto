# %%
from pathlib import Path

import gpxpy
from ipyleaflet import Map, Marker, Polyline
from ipywidgets import HTML, Layout

AMS = (2.377956, 4.897070)


# %%
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


# %%
m = Map(center=AMS, zoom=2, scroll_wheel_zoom=True, layout=Layout(height="600px"))


def valid(p: Path) -> bool:
    if p.stem.startswith("."):
        return False
    if p.is_dir():
        return True
    return False


dirs = [d for d in Path("hikes-gpx").iterdir() if valid(d)]
for dpath in dirs:
    coords = load_coords(dpath)
    gpx_track = Polyline(locations=coords, color="blue", fill=False, opacity=0.7)
    gpx_marker = Marker(location=coords[0], draggable=False)
    if (Path("posts") / (dpath.stem + ".qmd")).exists():
        hike_name = dpath.stem.replace("-", " ").title()
        popup_html = f"""
        <h3>{hike_name}</h3>
        <a href="/hikes/posts/{dpath.stem}.html">View Details</a>
        """
        gpx_marker.popup = HTML(popup_html)
    m.add_layer(gpx_track)
    m.add_layer(gpx_marker)
m

# %%
