from definitions import SYSTEM, System

from consts import UBISOFT_REGISTRY_LAUNCHER, UBISOFT_WOW6432_REGISTRY_LAUNCHER, APPDATA_PATH
import os
import logging as log
from importlib import import_module
from typing import Any

winreg: Any = None
ctypes: Any = None
if SYSTEM == System.WINDOWS:
    winreg = import_module('winreg')
    ctypes = import_module('ctypes')


class LocalClient(object):
    def __init__(self):
        self.last_modification_times = None
        self.configurations_path = None
        self.ownership_path = None
        self.settings_path = None
        self.launcher_log_path = None
        self.user_id = None
        self._is_installed = None
        self.refresh()

    def initialize(self, user_id):
        if not user_id:
            log.warning("Initialized with null user id!")
        log.info('Setting user id')
        self.user_id = user_id
        self.refresh()
        # Start tracking the ownership file when it exists.
        self.ownership_changed()

    def ownership_accessible(self):
        if self.ownership_path is None:
            return False
        else:
            return os.access(self.ownership_path, os.R_OK)

    def settings_accessible(self):
        if self.settings_path is None:
            return False
        else:
            return os.access(self.settings_path, os.R_OK)

    def configurations_accessible(self):
        if self.configurations_path is None:
            return False
        else:
            return os.access(self.configurations_path, os.R_OK)

    def __read_file(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                return f.read()
        except (FileExistsError, OSError, IOError) as e:
            log.warning(f'file not found [{e}]')
            return None

    def read_config(self):
        return self.__read_file(self.configurations_path)

    def read_ownership(self):
        return self.__read_file(self.ownership_path)

    def read_settings(self):
        return self.__read_file(self.settings_path)

    @property
    def is_installed(self):
        return self._is_installed

    def is_running(self):
        return ctypes.windll.user32.FindWindowW(None, "Ubisoft Connect")

    @property
    def was_user_logged_in(self):
        if not self.ownership_path:
            return False
        return os.path.exists(self.ownership_path)

    def _find_windows_client(self):
        # Try the native launcher key first, then the WOW6432Node key used on some installs.
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, UBISOFT_REGISTRY_LAUNCHER, 0,
                                winreg.KEY_READ) as key:
                directory, _ = winreg.QueryValueEx(key, "InstallDir")
                return os.access(directory, os.F_OK), directory
        except OSError:
            pass
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, UBISOFT_WOW6432_REGISTRY_LAUNCHER, 0,
                                winreg.KEY_READ) as key:
                directory, _ = winreg.QueryValueEx(key, "InstallDir")
                return os.access(directory, os.F_OK), directory
        except OSError:
            return False, ''

    def _resolve_cache_dir(self, install_path):
        install_cache = os.path.join(install_path, "cache")
        appdata_cache = os.path.join(APPDATA_PATH, "cache")

        # Prefer the modern AppData cache when it actually exists, because current
        # Ubisoft Connect installs often keep the live configuration there.
        if os.path.isdir(appdata_cache):
            log.info(f'Using AppData cache location: {appdata_cache}')
            return appdata_cache

        if os.path.isdir(install_cache):
            return install_cache

        # Neither location exists yet; default to the install-dir path to keep a stable fallback.
        return install_cache

    def refresh(self):
        if SYSTEM == System.MACOS:
            return

        exists, path = self._find_windows_client()
        if exists:
            if not self._is_installed:
                log.info('Local client installed')
                self._is_installed = True

            cache_dir = self._resolve_cache_dir(path)
            self.configurations_path = os.path.join(cache_dir, "configuration", "configurations")
            self.launcher_log_path = os.path.join(path, "logs", "launcher_log.txt")

            if self.user_id is not None:
                appdata_ownership = os.path.join(APPDATA_PATH, "cache", "ownership", self.user_id)
                appdata_settings = os.path.join(APPDATA_PATH, "cache", "settings", self.user_id)
                install_ownership = os.path.join(cache_dir, "ownership", self.user_id)
                install_settings = os.path.join(cache_dir, "settings", self.user_id)

                if os.access(appdata_ownership, os.F_OK):
                    self.ownership_path = appdata_ownership
                    log.info('Using AppData path for ownership file')
                else:
                    self.ownership_path = install_ownership
                    log.info('Using cache path for ownership file')

                if os.access(appdata_settings, os.F_OK):
                    self.settings_path = appdata_settings
                    log.info('Using AppData path for settings file')
                else:
                    self.settings_path = install_settings
                    log.info('Using cache path for settings file')
        else:
            if self._is_installed:
                log.info('Local client uninstalled')
            self._is_installed = False
            self.configurations_path = None
            self.ownership_path = None
            self.settings_path = None
            self.launcher_log_path = None

    def ownership_changed(self):
        # The status tick can run before authentication has supplied the Ubisoft
        # user id.  In that state refresh() intentionally has no ownership path
        # to build, so probing it would only produce a misleading warning.
        if self.user_id is None:
            return False

        path = self.ownership_path
        if path is None:
            log.warning('Ownership file path is unavailable after Ubisoft client initialization')
            self.refresh()
            return False

        try:
            stat = os.stat(path)
        except FileNotFoundError:
            log.warning(f'Ownership file at {path} path not present, user never logged in to uplay client.')
            self.refresh()
        except Exception as e:
            log.exception(f'Stating {path} has failed: {str(e)}')
            self.refresh()
        else:
            if stat.st_mtime != self.last_modification_times:
                self.last_modification_times = stat.st_mtime
                return True
        return False
