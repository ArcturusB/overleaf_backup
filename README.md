Download zip backups of Overleaf projects.

~~~
usage: overleaf_backup.sh [-h] [-O OUTPUT] project [project ...]

Download zip backups of Overleaf projects.

positional arguments:
  project               project URL or ID

optional arguments:
  -h, --help            show this help message and exit
  -O OUTPUT, --output OUTPUT
                        output zip file (only for a single project)
~~~

Dependencies : [BeautifulSoup][1], [requests2][2].

# License

Copyright (C) 2018 Gabriel Pelouze

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. See <https://www.gnu.org/licenses/gpl-3.0.txt>.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# Acknowledgements

The OverleafClient class contains code from Todor Mihaylov’s [Overleaf backup
tool][3], that was adapted to work with Overleaf v2.

[1]: https://www.crummy.com/software/BeautifulSoup/
[2]: http://docs.python-requests.org/en/master/
[3]: https://github.com/tbmihailov/overleaf-backup-tool

