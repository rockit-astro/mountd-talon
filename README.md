## W1m data pipeline daemon [![Travis CI build status](https://travis-ci.org/warwick-one-metre/teld.svg?branch=master)](https://travis-ci.org/warwick-one-metre/teld)

Part of the observatory software for the Warwick one-meter telescope.

`teld` interfaces with and wraps the low-level talon daemons and exposes a
coherant telescope control interface via Pyro.

`tel` is a commandline utility for controlling the telescope.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the W1m software architecture and instructions for developing and deploying the code.

### Software setup

After installing `onemetre-telescope-server`, the `teld` must be enabled using:
```
sudo systemctl enable teld.service
```

The service will automatically start on system boot, or you can start it immediately using:
```
sudo systemctl start teld.service
```

Next, open a port in the firewall so that other machines on the network can access the daemon:
```
sudo firewall-cmd --zone=public --add-port=9003/tcp --permanent
sudo firewall-cmd --reload
```


