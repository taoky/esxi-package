# esxi-package (RunnerD)

A daemon package example running in ESXi 6.0

## Intro

It utilizes the Python 2.7 inside ESXi 6.0 system, opens a single-thread naive HTTP server, and outputs the result of the command set to execute.

## Usage

Copy `RunnerD.vib` to ESXi server (assuming it's `/tmp/RunnerD.vib`), and execute:

```
esxcli software vib install --no-sig-check -v /tmp/RunnerD.vib
```

Then configure the service by editing `/etc/runner.config`:

```
[runner]
cmd = /opt/lsi/MegaCLI/MegaCli -PDlist -aALL
cwd = /opt/lsi/MegaCLI/
```

Adjust `cmd` and `cwd` to your preference.

You can start `runnerd` service in ESXi management page, or:

```
/etc/init.d/runnerd start
```

to start.

Firewall is configured, so you can directly access it by `curl`:

```
curl http://<ip of esxi>:8888
```

## Build

1. Build a docker image by Dockerfile in <https://gist.github.com/taoky/1731dcca55a27e6f3f359450f1a04a10>

```
docker build -t vibauthor .
```

2. Set sticky bit for config file (to make it editable after installation)

```
chmod +t runnerd/payloads/RunnerD/etc/runner.config
```

3. Run builder

```
docker run -v "$PWD":/data vibauthor:latest vibauthor -C -t /data/runnerd -v /data/RunnerD.vib
```

## Uninstall

```
esxcli software vib remove --vibname=RunnerD
```

## References

1. A Daemon's VIB: Building a software package for VMware ESXi
   1. <https://www.v-front.de/2012/11/a-daemons-vib-building-software-package.html>
   2. <https://www.v-front.de/2012/11/a-daemons-vib-part-2-building-software.html>
   3. <https://www.v-front.de/2012/11/a-daemons-vib-part-3-building-software.html>
2. How to create a daemon in Python (2.x):
   1. <https://stackoverflow.com/a/473702>
   2. <https://web.archive.org/web/20131017130434/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/>
3. The removed Vib Author page in Internet Archive:
   1. <https://web.archive.org/web/20161228164601/https://labs.vmware.com/flings/vib-author>
