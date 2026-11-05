from pathlib import Path
from streamtuner_ng.plugins.base import Channel, make_row


# Set the root directory here
ROOT = Path("/mnt/netgear/media/music/Radio")


def scan_stations():
    stations = {}

    if not ROOT.exists():
        return stations

    for directory in sorted(ROOT.iterdir()):
        if not directory.is_dir():
            continue

        files = []
        for file in sorted(directory.iterdir()):
            if file.is_file():
                files.append((file.stem, str(file)))

        if files:
            stations[directory.name] = files

    return stations


class ExampleRadio(Channel):

    id = "myownstations"
    title = "My own stations"
    description = "My own stations as found on the nas server by Rocus van Oosten"
    homepage = "file:/" + str(ROOT)
    has_search = True
    icon_emoji = "🎧"

    # Initial scan when the plugin is imported.
    STATIONS = scan_stations()

    def update_categories(self):
        return list(self.STATIONS.keys())

    def update_streams(self, category, search=None):

        # Rescan when Reload is used.
        self.STATIONS = scan_stations()

        rows = []

        for name, url in self.STATIONS.get(category, []):
            if search and search.lower() not in name.lower():
                continue

            rows.append(make_row(
                title=name,
                url=url,
                genre=category,
                bitrate=128,
                format="audio/mpeg",
                listformat="",
            ))

        return rows
