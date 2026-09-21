from streamtuner_ng.plugins.base import Channel, make_row


class ExampleRadio(Channel):

    from pathlib import Path

    # Set the root directory here
    ROOT = Path("/mnt/netgear/media/music/Radio")

    id = "myownstations"           # unique key, lowercase (must not clash with another channel)
    title = "My own stations"      # the label shown in the sidebar
    description = "My own stations as found on the nas server by Rocus van Oosten"
    homepage = "file:/"+ str(ROOT) # right-click a station → Open web goes here
    has_search = True              # True = update_streams() honours the toolbar filter
    icon_emoji = "🎧"              # sidebar fallback icon when a station has no favicon

    STATIONS = {}

    for directory in sorted(ROOT.iterdir()):
        if not directory.is_dir():
            continue

        files = []
        for file in sorted(directory.iterdir()):
            if file.is_file():
                files.append((file.stem, str(file)))
        if files:
            STATIONS[directory.name] = files
		
    # The names shown in the middle "categories" column (kept in this order).
    def update_categories(self):
        return list(self.STATIONS.keys())

    # Return the station rows for the selected category. make_row() needs only
    # title + url; everything else is optional. mpv plays direct URLs, .pls, .m3u.
    def update_streams(self, category, search=None):
        rows = []
        for name, url in self.STATIONS.get(category, []):
            if search and search.lower() not in name.lower():
                continue                     # respect the search box (has_search = True)
            rows.append(make_row(
                title=name,
                url=url,
                genre=category,
                bitrate=128,
                format="audio/mpeg",
                listformat="",            # "srv" = a direct stream URL (no .pls/.m3u indirection)
            ))
        return rows
