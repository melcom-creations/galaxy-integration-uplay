# Ubisoft Connect Integration Plugin for GOG Galaxy 2.1+ (64-bit)

This plugin imports your Ubisoft Connect library into GOG Galaxy 2.1+ 64-bit. Based on the original community integration, it has been updated for the current GOG Galaxy client and Python 3.13, with current login and API handling.

The steps below are for Windows. Dependencies are bundled; no separate Python installation is needed.

[Installation](#-installation) | [First Start](#-first-start-and-initial-sync) | [Troubleshooting](#-troubleshooting) | [Support & Feedback](#-support--feedback)

## ✨ Features

* Imports your owned Ubisoft Connect games into GOG Galaxy
* Imports supported Ubisoft subscription games
* Imports game time from Ubisoft Connect
* Detects locally installed Ubisoft games
* Installs, launches, and uninstalls games through Ubisoft Connect
* Supports Ubisoft games linked to third-party launchers where available
* Includes improved login reliability and current Ubisoft API identifiers

> [!NOTE]
> macOS compatibility may be technically possible, but it is currently untested because I do not have access to a Mac. If you use macOS and would like to help test the integration, feel free to contact me.

## 📦 Installation

### 🔄 Automatic Installation with Plugin Updater (Recommended)

Use the [melcom GOG Galaxy Plugin Updater](https://github.com/melcom-creations/galaxy-integrations-64bit/tree/main/tools/melcom-galaxy_plugin_updater) to install or update the integration.

1. Download and extract the Plugin Updater.
2. Double-click `update-plugins.bat`.
3. Select your preferred language and follow the displayed instructions.

### 📂 Manual Installation

1. Close GOG Galaxy completely, including the system tray application.
2. Download the [latest release package](https://github.com/melcom-creations/galaxy-integration-uplay/releases/latest).
3. Extract the plugin folder from the ZIP archive into:

   ```text
   %localappdata%\GOG.com\Galaxy\plugins\installed\
   ```

Place `manifest.json` directly inside this folder, without an extra nested plugin folder:

```text
%localappdata%\GOG.com\Galaxy\plugins\installed\uplay_afb5a69c-b2ee-4d58-b916-f4cd75d4999a\
```

> [!IMPORTANT]
> Do not place backup copies of this plugin inside the `plugins\installed` directory. GOG Galaxy scans every folder inside this directory during startup, so duplicate plugin folders can cause GUID conflicts or load an outdated version.

**Next step:** Continue with [First Start and Initial Sync](#-first-start-and-initial-sync).

## 🚀 First Start and Initial Sync

For the first synchronization after installing or updating the plugin:

1. Start Ubisoft Connect and keep it open.
2. Start GOG Galaxy.
3. Connect the Ubisoft Connect integration through **Settings -> Integrations** if necessary.
4. Complete the Ubisoft login when prompted.
5. Open the account menu in the top-right corner and select **Sync integrations**.
6. Wait until the synchronization has finished.

## 🛠️ Technical Details

* **64-bit Registry Handling** - Reads Ubisoft Connect installation data from the redirected 32-bit registry view when required and falls back to the native registry view.
* **Game Loading Protection** - Handles local parsing, filesystem, and Ubisoft API failures without crashing GOG Galaxy.
* **Current Login and API Identifiers** - Uses the current Ubisoft Connect login and API identifiers while retaining compatible fallback values.
* **Bundled Runtime Dependencies** - Includes the required Python modules so no separate Python installation is needed.

## 🛠️ Troubleshooting

Restart Galaxy and the store app and try one synchronization. If the problem remains, collect a fresh log. A database reset is not required for this.

### 🧪 Create a Fresh Diagnostic Log

1. Close GOG Galaxy completely, including the system tray application.
2. Open `%ProgramData%\GOG.com\Galaxy\logs\`. Move the existing `plugin-uplay-afb5a69c-b2ee-4d58-b916-f4cd75d4999a.log` to a backup folder outside this directory, if present. Leave other logs in place.
3. Start Ubisoft Connect. Start Galaxy, reproduce the problem once, then close Galaxy completely to finish writing the log.
4. Send the newly created plugin log, not the entire folder. Include the plugin and Galaxy versions, your steps, the expected and actual result, and whether the problem can be reproduced.

See [Support & Feedback](#-support--feedback) for contact options.

### 🔄 Reset Plugin Storage (Last Resort)

Use this only if restarting and synchronizing do not help, or when requested for troubleshooting. Cached library data and local playtime may be lost; signing in again may be required. Keep the backup.

1. Close GOG Galaxy completely, including the system tray application.
2. Open `%ProgramData%\GOG.com\Galaxy\storage\plugins\`.
3. Find the active `uplay_...-storage.db` file for your Galaxy account. If unsure which file is correct, stop. Leave other integrations' databases unchanged.
4. Append `.old` to its name. If that backup already exists, use an unused suffix; never overwrite it.
5. Start Ubisoft Connect. Start Galaxy, reconnect if necessary, and select **Sync integrations** once. Wait until it finishes.

To undo: close Galaxy, rename the new database to an unused backup name, then restore the saved database's original name. Never restore it while Galaxy is running.

## 🙏 Credits

**Original Community Integration**  
Friends of Galaxy  
[Friends of Galaxy Ubisoft Connect integration](https://github.com/FriendsOfGalaxy/galaxy-integration-uplay)

**64-bit Port, Maintenance and Improvements**  
melcom

## 🤝 Support & Feedback

**GitHub Issues are intentionally disabled.** Health-related limitations prevent me from reliably managing separate issue trackers across all of my plugin repositories.

Before contacting me, follow [Troubleshooting](#-troubleshooting) and prepare a fresh Ubisoft Connect plugin log with a detailed description.

* **GOG:** Send me a message or add me as a friend through my [GOG profile](https://www.gog.com/u/melcom).
* **Email:** `melcom @ gmx.net`
* **Discord:** `.melcom` - the leading dot is part of the username. You can send me a message or add me as a friend.

Logs can be attached directly or shared using an accessible cloud storage link, such as Dropbox, OneDrive, Google Drive, or a similar service. Response times may vary depending on my health and available development time. Thank you for your understanding.
