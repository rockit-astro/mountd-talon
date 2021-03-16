## Talon telescope daemon

Part of the observatory software for the Warwick one-meter and SuperWASP telescopes.

`teld` interfaces with and wraps the low-level talon daemons and exposes a
coherant telescope control interface via Pyro.

`tel` is a commandline utility for controlling the telescope.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the W1m software architecture and instructions for developing and deploying the code.

### Software setup

After installing `<telescope>-talon-server`, the `teld` must be enabled using:
```
sudo systemctl enable teld@<telescope>
```

where `<telescope>` is `onemetre` or `superwasp`.

The service will automatically start on system boot, or you can start it immediately using:
```
sudo systemctl start teld@<telescope>
```

Next, open a port in the firewall so that other machines on the network can access the daemon:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```

where `<port>` is the port associated with the daemon referenced in the json config file.
