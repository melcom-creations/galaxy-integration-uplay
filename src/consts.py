import os
from pathlib import Path
from definitions import System, SYSTEM

UBISOFT_REGISTRY = "SOFTWARE\\Ubisoft"
STEAM_REGISTRY = "Software\\Valve\\Steam"
UBISOFT_REGISTRY_LAUNCHER = "SOFTWARE\\Ubisoft\\Launcher"
UBISOFT_WOW6432_REGISTRY_LAUNCHER = "SOFTWARE\\WOW6432Node\\Ubisoft\\Launcher"
UBISOFT_REGISTRY_LAUNCHER_INSTALLS = "SOFTWARE\\Ubisoft\\Launcher\\Installs"

_local_appdata = Path(os.getenv('LOCALAPPDATA') or Path.home() / 'AppData' / 'Local')
APPDATA_PATH = _local_appdata / 'Ubisoft Game Launcher'

if SYSTEM == System.WINDOWS:
    UBISOFT_SETTINGS_YAML = str(APPDATA_PATH / 'settings.yaml')

UBISOFT_CONFIGURATIONS_BLACKLISTED_NAMES = ["gamename", "l1", '', 'ubisoft game', 'name']

CHROME_USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"

# Fallback login values used when the current client data is not available.

CLUB_APPID = "314d4fef-e568-454a-ae06-43e3bece12a6"
CLUB_GENOME_ID = "85c31714-0941-4876-a18d-2c7e9dce8d40"

# The current login flow does not require a matching genomeId.
UBISOFT_LOGIN_APPID = "1068ef52-dfd2-4e62-8ac9-37a47e6c0b78"

# UBISOFT_APPID is read from the Ubisoft Connect client executable and used for API requests.
# It must differ from the login app ID because the API rejects the login ID in the Ubi-AppId header.

UBISOFT_APPID = "f68a4bb5-608a-4ff2-8123-be8ef797e0a6"
UBISOFT_GENOMEID = "954e66a0-be1b-4aa0-9690-fb75201e4e9e"

AUTH_PARAMS = {
    "window_title": "Login | Ubisoft WebAuth",
    "window_width": 460,
    "window_height": 690,
    "start_uri": f"https://connect.ubisoft.com/login?appId={UBISOFT_APPID}&genomeId={UBISOFT_GENOMEID}&lang=en-US&nextUrl=https:%2F%2Fconnect.ubisoft.com%2F",
    "end_uri_regex": r".*connect\.ubisoft\.com/change_domain/.*"
}

AUTH_JS = {
    r".*connect\.ubisoft\.com.*": [
        r'''
        (function () {
            if (window.__galaxyUbisoftAuthWatcher) {
                return;
            }

            function finishGalaxyLogin() {
                var loginData = window.localStorage.getItem("PRODloginData");
                var rememberMe = window.localStorage.getItem("PRODrememberMe");
                var lastProfile = window.localStorage.getItem("PRODlastProfile");

                if (!loginData) {
                    return;
                }

                try {
                    var session = JSON.parse(loginData);
                    if (!session.ticket || !session.sessionId || !session.userId || !session.nameOnPlatform) {
                        return;
                    }
                } catch (error) {
                    return;
                }

                window.clearInterval(window.__galaxyUbisoftAuthWatcher);
                window.__galaxyUbisoftAuthWatcher = null;
                window.location.replace(
                    "https://connect.ubisoft.com/change_domain/" +
                    loginData + "," + (rememberMe || "null") + "," + (lastProfile || "null")
                );
            }

            window.__galaxyUbisoftAuthWatcher = window.setInterval(finishGalaxyLogin, 500);
            finishGalaxyLogin();
        }());
        '''
    ]
}














