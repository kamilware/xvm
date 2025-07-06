# xvm

Simple manager for go/node versions

## Support
- Linux (x64) [tested on Debian bookworm]

## Commands
 - `[go|node] list` - List installed and available versions
 - `[go|node] install <version|latest>` - Install version, use 'latest' for latest stable
 - `[go|node] uninstall <version>` - Uninstall version
 - `[go|node] active <version|latest>` - Set default system version, use 'latest' for latest stable installed
 - `[go|node] autoupdate [on|off]` - Set autoupdate on/off (only stable versions, runs on start); no arg for status (ON/OFF)
## Quickstart

To install (removes previous installation and disables autoupdate):
```shell
curl -fsSL https://raw.githubusercontent.com/kamilware/xvm/master/scripts/install.sh | bash
```

To install (disables autoupdate):
```shell
curl -fsSL https://raw.githubusercontent.com/kamilware/xvm/master/scripts/uninstall.sh | bash
```
