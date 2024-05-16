# textlink

Process and convert textual link file formats.

Only support .url and .desktop for now,
may expand project scope to other link types and file formats.


## Installation

Move `textlink.py` to any directory in your `$PATH` like `~/.local/bin`
or create a symlink to its location.



## Usage from Terminal

```shell
textlink.py input.url output.desktop
```



## Usage as a Library

...



## File Format Description

### XDG .desktop

A standard file format from freedesktop
used by most desktop environments on linux
(KDE, GNOME, Cinnamon, Xfce, LXQt).

references:
- [freedesktop specification](https://specifications.freedesktop.org/desktop-entry-spec/latest/)
- [archlinux wiki](https://wiki.archlinux.org/title/Desktop_entries)
- [KDE Developer Documentation](https://develop.kde.org/docs/features/desktop-file/)

example:
```
[Desktop Entry]
Icon=text-html
Name=example link
Name[lang_country.encoding@modifier]=localized name
Name[de]=Beispiellink
Name[es]=enlace de ejemplo
Name[fr]=exemple de lien
Type=Link
URL=https://www.example.com/link/

# ignored comment line
```


### Windows .url

example:
```
[InternetShortcut]
URL=http://www.example.com/
WorkingDirectory=C:\WINDOWS\
IconFile=C:\WINDOWS\SYSTEM\url.dll
IconIndex=1
Modified=20F06BA06D07BD014D
HotKey=0
```



## License

Licensed under Apache License, Version 2.0,
([LICENSE-APACHE](LICENSE-APACHE)
or http://www.apache.org/licenses/LICENSE-2.0)

