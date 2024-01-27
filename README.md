## Talon telescope daemon

`talon_mountd` interfaces with and wraps the low-level talon daemons and exposes a
coherent telescope control interface via Pyro.

`tel` is a commandline utility for controlling the telescope.

### Configuration

Configuration is read from json files that are installed by default to `/etc/mountd`.
A configuration file is specified when launching the server, and the `tel` frontend will search this location when launched.

```python
{
  "daemon": "onemetre_telescope", # Run the server as this daemon. Daemon types are registered in `rockit.common.daemons`.
  "log_name": "teld", # The name to use when writing messages to the observatory log.
  "control_machines": ["OneMetreDome", "OneMetreTCS"], # Machine names that are allowed to control (rather than just query) state. Machine names are registered in `rockit.common.IP`.
  "telescope": "W1m", # Either W1m or NGTS  
  "virtual": false, # Run talon's telescoped with simulated hardware.
  "query_delay": 1, # Delay between shared memory queries.
  "initialization_timeout": 60, # Maximum time allowed for talon's telescoped to start.
  "slew_timeout": 120, # Maximum time allowed to slew from any position to any other position (note: telescoped has its own separate value).
  "focus_timeout": 60, # Maximum time allowed for any focus adjustment (note: telescoped has its own separate value).
  "homing_timeout": 120, # Maximum time allowed for each axis homing command (note: telescoped has its own separate value).
  "limit_timeout": 120, # Maximum time allowed for each axis limit command (note: telescoped has its own separate value).
  "ping_timeout": 5, # Maximum time allowed to acknowledge a ping command.
  "ha_soft_limits": [-72, 90], # Allowed hour angle range in degrees (pre-filters bogus pointings with a more graceful error than talon failing)
  "dec_soft_limits": [-30, 85], # Allowed declination range in degrees (pre-filters bogus pointings with a more graceful error than talon failing)
  "focus_tolerance": 0.005, # (W1m only) Consider a focus command complete when it is within this many micron of the requested value.
  "security_system_daemon": "onemetre_roomalert", # (W1m only) Daemon to check whether the W1m security system has tripped.
  "security_system_key": "security_system_safe", # (W1m only) Switch name for the security system status.
  "park_positions": {
    "stow": { # Positions that can be used with 'tel park'.
      "desc": "general purpose park protecting the mirror and instrument", # Description reported by 'tel park'.
      "alt": 35, # Altitude in degrees.
      "az": 25 # Azimuth in degrees.
    }
  }
}
```

### Initial Installation

The automated packaging scripts will push 4 RPM packages to the observatory package repository:

| Package                           | Description                                                                  |
|-----------------------------------|------------------------------------------------------------------------------|
| rockit-mount-talon-server         | Contains the `talond` server and configuration for the W1m telescope.        |
| rockit-mount-talon-client         | Contains the `tel` commandline utility for controlling the telescope server. |
| rockit-mount-talon-data-onemetre  | Contains the json configuration files for the W1m telescope.                 |
| rockit-mount-talon-data-ngts-m06  | Contains the json configuration files for a NGTS telescope.                  |
| python3-rockit-mount-talon        | Contains the python module with shared code.                                 |

After installing packages, the systemd service should be enabled:

```
sudo systemctl enable --now talon_mountd@<config>
```

where `config` is the name of the json file for the appropriate telescope.

Now open a port in the firewall:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```
where `port` is the port defined in `rockit.common.daemons` for the daemon specified in the config.

### Upgrading Installation

New RPM packages are automatically created and pushed to the package repository for each push to the `master` branch.
These can be upgraded locally using the standard system update procedure:
```
sudo yum clean expire-cache
sudo yum update
```

The daemon should then be restarted to use the newly installed code:
```
sudo systemctl restart talon_mountd@<config>
```

### Testing Locally

The server and client can be run directly from a git clone:
```
./talon_mountd onemetre.json
MOUNTD_CONFIG_PATH=./onemetre.json ./tel status
```
