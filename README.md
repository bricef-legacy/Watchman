Watchman
========

Watchman is a process monitor with web interface and inotify integration.

Using [pyinotify](https://github.com/seb-m/pyinotify), Watchman can restart the processes it monitors when files change.

Using [Bottlepy](http://bottlepy.org/docs/dev/), it can provides a web interface to view stdout of monitored processes, inotify events, and configuration.

For security, Watchman does not allow processes to be started or stopped via the web interface.

To start Watchman:

    $ watchman --config path/to/watchman.json --web-port 8080

Note how the configuration file is a json document. A config might look like this:

```json
{
  "working": "path/to/app",
  "processes": {
    "web": { "run": "python app.py" },
    "worker": {"run": "ruby worker.rb" },
    "db": {"run": "mydb -c path/to/db.conf"},
  },
  "file-events": {
    "path/to/app/src": { "restart": ["web"] }
  } 
}
```



