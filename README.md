# Ubisoft Connect Integration Plugin for GOG Galaxy 2.1+ (64-bit)

This repository contains the Ubisoft Connect integration plugin for the native 64-bit version of GOG Galaxy 2.1+. It is based on the original community integration and has been updated for the current GOG Galaxy client and Python 3.13. The project includes updated dependencies, login and compatibility fixes, stability improvements, and ongoing maintenance.

---

## ✨ Features

* Imports your owned Ubisoft Connect games into GOG Galaxy
* Imports supported Ubisoft subscription games
* Imports game time from Ubisoft Connect
* Detects locally installed Ubisoft games
* Installs, launches, and uninstalls games through Ubisoft Connect
* Supports Ubisoft games linked to third-party launchers where available
* Includes improved login reliability and current Ubisoft API identifiers
* Supports GOG Galaxy 2.1+ 64-bit and Python 3.13
* Includes updated dependencies, compatibility fixes, and stability improvements

---

## 🛠️ Technical Highlights

* **64-bit Registry Handling** - Reads Ubisoft Connect installation data from the redirected 32-bit registry view when required and falls back to the native registry view.
* **Game Loading Protection** - Handles local parsing, filesystem, and Ubisoft API failures without crashing GOG Galaxy.
* **Current Login and API Identifiers** - Uses the current Ubisoft Connect login and API identifiers while retaining compatible fallback values.
* **Bundled Runtime Dependencies** - Includes the required Python modules so no separate Python installation is needed.

---

## 📦 Installation

### Automatic Installation with Plugin Updater (Recommended)

The easiest way to install the Ubisoft Connect integration is with the [melcom GOG Galaxy Plugin Updater](https://github.com/melcom-creations/galaxy-integrations-64bit/tree/main/tools/melcom-galaxy_plugin_updater). The updater detects existing integrations and can install any supported melcom plugins that are still missing.

1. Download and extract the Plugin Updater.
2. Double-click `update-plugins.bat`.
3. Select your preferred language.
4. Follow the displayed instructions.

### Manual Installation

1. Close GOG Galaxy completely and make sure it is no longer running in the system tray.
2. Download the latest release package from this repository.
3. Extract the ZIP archive directly into:

```text
%localappdata%\GOG.com\Galaxy\plugins\installed\
```

The resulting directory structure must look like this:

```text
%localappdata%\GOG.com\Galaxy\plugins\installed\
└── uplay_afb5a69c-b2ee-4d58-b916-f4cd75d4999a\
    ├── manifest.json
    ├── plugin.py
    ├── README.md
    └── ...
```

4. Continue with **First Start and Initial Sync** below.

---

## 🚀 First Start and Initial Sync

For the first synchronization after installing or updating the plugin:

1. Start Ubisoft Connect and keep it open.
2. Start GOG Galaxy.
3. Connect the Ubisoft Connect integration through **Settings -> Integrations** if necessary.
4. Complete the Ubisoft login when prompted.
5. Open the account menu in the top-right corner and select **Sync integrations**.
6. Wait until the synchronization has finished.

---

## 🔄 Resetting the Plugin Database (Troubleshooting)

Reset the local plugin database only if the integration behaves unexpectedly or synchronization problems continue after restarting both applications.

1. Close GOG Galaxy completely.
2. Open `C:\ProgramData\GOG.com\Galaxy\storage\plugins\`.
3. Find every file starting with `uplay_` and ending in `-storage.db`.
4. Rename each matching file by appending `.old`, for example:

   `uplay_xxxxxxxxx-storage.db` -> `uplay_xxxxxxxxx-storage.db.old`

5. Start Ubisoft Connect and keep it open.
6. Start GOG Galaxy and reconnect the Ubisoft Connect integration if necessary.
7. Open the account menu in the top-right corner and select **Sync integrations**.
8. Wait until the synchronization has finished.

---

## ⚠️ Important

Do **not** place backup copies of this plugin inside the `plugins\installed` directory.

GOG Galaxy scans every folder inside this directory during startup. Duplicate plugin folders can lead to GUID conflicts or cause Galaxy to load an outdated version of the plugin.

---

## 🙏 Credits

**Original Community Integration**  
Friends of Galaxy  
[Friends of Galaxy Ubisoft Connect integration](https://github.com/FriendsOfGalaxy/galaxy-integration-uplay)

**64-bit Port, Maintenance and Improvements**  
melcom

---

## 🤝 Support & Feedback

This project is developed and maintained by one person. Response times may vary, especially during periods when health-related limitations reduce available development time.

**GitHub Issues are intentionally disabled.**

If you would like to report a bug, suggest an improvement, or get in touch, please use the contact form on my website:

📩 [Contact form](https://melcom-creations.github.io/melcom-music/contact.html)

Thank you for your patience and support!
