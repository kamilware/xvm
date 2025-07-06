import sys

from src.go.cli import handle as go_handler
from src.node.cli import handle as node_handler
from src.shared.const import SUPPORTED_LANGUAGES, LANG_MAP
from src.shared.log import log_to_file
from src.shared.preflight import scaffold, support_check
from src.shared.term import error


def print_usage():
    print("Usage:")
    print("  xvm [go|node] list \t\t\t\t\t\t - List installed and available versions")
    print("  xvm [go|node] install <version|latest> \t - Install version, use 'latest' for latest stable")
    print("  xvm [go|node] uninstall <version> \t\t - Uninstall version")
    print(
        "  xvm [go|node] active <version|latest> \t - Set default system version, use 'latest' for latest stable installed")
    print("  xvm [go|node] autoupdate [on|off] \t\t - Set autoupdate on/off (only stable versions, runs on start)")


if __name__ == '__main__':
    scaffold()
    log_to_file('debug', ' '.join(sys.argv))
    system_info = support_check()

    args = sys.argv[1:]

    if len(args) < 2:
        print_usage()
        sys.exit(1)

    language = args[0].lower()
    if language in LANG_MAP:
        language = LANG_MAP[language]

    if language not in SUPPORTED_LANGUAGES:
        error(f'{language} is not supported, exiting...')
        sys.exit(1)

    if language in ['golang', 'go']:
        go_handler(args)
    elif language == 'node':
        node_handler(args)
