import os
from importlib import import_module
from typing import Any
from definitions import GameStatus
from consts import SYSTEM, System, STEAM_REGISTRY
winreg: Any = None
if SYSTEM == System.WINDOWS:
    winreg = import_module('winreg')


def _get_steam_install_path():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, STEAM_REGISTRY) as lkey:
            steam_path, _ = winreg.QueryValueEx(lkey, 'SteamExe')
            return os.path.normcase(os.path.normpath(steam_path))
    except OSError:
        return None


def is_steam_installed():
    steam_path = _get_steam_install_path()
    if steam_path:
        return os.path.exists(steam_path)
    return False


def _parse_steam_registry_status(key):
    if int(winreg.QueryValueEx(key, "Installed")[0]):
        try:
            if int(winreg.QueryValueEx(key, "Running")[0]):
                return GameStatus.Running
            elif int(winreg.QueryValueEx(key, "Updating")[0]):
                # todo, 'Updating' status not yet supported
                return GameStatus.Installed
            else:
                return GameStatus.Installed
        except WindowsError:
            return GameStatus.Installed
    else:
        return GameStatus.NotInstalled


def get_steam_game_status(path):
    if not path:
        return GameStatus.NotInstalled

    reg_path = path
    index = reg_path.lower().find("software")
    end = reg_path.lower().find("installed")
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path[index:end], 0, winreg.KEY_READ) as key:
            return _parse_steam_registry_status(key)
    except WindowsError:
        return GameStatus.NotInstalled
