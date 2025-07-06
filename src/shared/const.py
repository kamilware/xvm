import os.path

XVM_DIR = os.path.expanduser("~/.xvm")
LOG_PATH = os.path.join(XVM_DIR, "xvm.log")
XVM_GO_DIR = os.path.join(XVM_DIR, 'go')
XVM_NODE_DIR = os.path.join(XVM_DIR, 'node')

SUPPORTED_OS = ['linux']
SUPPORTED_ARCH = ['x86_64', 'amd64', 'x64']
LANG_MAP = {
    'golang': 'go',
}
GO_ARCH_MAP = {
    "x86_64": "amd64",
    "x64": "amd64"
}
NODE_ARCH_MAP = {
    "x86_64": "x64",
    "amd64": "x64"
}
SUPPORTED_LANGUAGES = ['go', 'node']
SUPPORTED_SHELLS = ['bash']
SUPPORTED_COMMANDS = ['list', 'install', 'uninstall', "active", "autoupdate"]
