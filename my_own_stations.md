Several month ago I made two plugins for your Streamtuner-ng program and I planned to show them to you. Because at the same time I converted my PC's to Debian13 and installed several programs anew including your streamtuner-ng I noticed that one of my plugins did not work on the version 1.4.1 (but worked OK on my previous version 1.2.0). I noticed that you have rewritten the program quite extensively probably to make it more stable and secure. It has become clear to me that at two places your changes prevented my plugin to work.

As background I must tell you that my radio stations are organized in PLS files in a directory (2 levels) structure on a NAS. Several programs use the PLS files in this directory. My plugin is meant to be able to access this directory structure. An other background program (that I described in http://github.com/rocus/sync-streamtuner-ng) is running on my Streamtuner-ng PC and is supposed to convert streamtuner's favorites to PLS files in my radio directory. In this way I can easily save found radio stations and thus use in other places around my house.

The plugin 'my_own_stations.py' shows my radio directory tree like any other radio browser provider. Because the URL's are local and the 'website' defined in my plugin is local there are two changes I propose in your streamtuner-ng Python files. I describe them below:

- small addition in streamtuner_ng/security.py in valid_url. see line 8 and 9
- small change in streamtuner_ng/ui/mainwindow.py in open_website. see line 2 and 3  

```
def valid_url(value: object, *, token: bool = False, web: bool = False) -> bool:
    if not isinstance(value, str) or not value or len(value) > MAX_URL:
        return False
    if any(ord(c) <= 32 or ord(c) == 127 for c in value) or '\\' in value:
        return False
    try:
        url = urlsplit(value)
        if url.scheme == 'file':
            return not web
        if not url.hostname or url.username is not None or url.password is not None:
            return False
        if url.port is not None and not 1 <= url.port <= 65535:
            return False
        if token and url.scheme == 'audioaddict':
            return (url.hostname in AUDIOADDICT_DOMAINS and url.port is None
                    and bool(re.fullmatch(r'/[a-zA-Z0-9_-]+', url.path))
                    and not url.query and not url.fragment)
        return url.scheme in ({'http', 'https'} if web else NETWORK_SCHEMES) 
    except (ValueError, UnicodeError):
        return False
```

```
    def _open_website(self, url: str) -> None:
        if not (valid_url(url, web=True) 
           or (url.startswith('file://') 
               and url.endswith('/') and valid_url(url, web=False))):
            self._status_error("Only HTTP(S) website links and local directory links can be opened")
            return
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices
        QDesktopServices.openUrl(QUrl(url))
```

My plugin 'my_own_stations.py' is quite straightforward:

```
from pathlib import Path
from streamtuner_ng.plugins.base import Channel, make_row


# Set the root directory here
ROOT = Path("/mnt/lacie/media/music/Radio")


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
    description = "My own stations as present in "+str(ROOT)
    homepage = "file:/" + str(ROOT) + "/"
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
                url=Path(url).as_uri(),
                genre=category,
            ))

        return rows
```
The things that needed to be changed by a user is ROOT and the string variables id, title, description. If the homepage starts with 'file:' and ends with '/' the directory (in ROOT) will be opened by a filemanager (if that is your default application for a simple file or directory).

