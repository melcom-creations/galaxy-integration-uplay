# Ubisoft Connect Integration Plugin for GOG Galaxy 2.1+ (64-bit)

This repository contains the Ubisoft Connect integration plugin for the 64-bit version of GOG Galaxy 2.1+.

The original community integration has been updated to work with the current 64-bit GOG Galaxy client and Python 3.13. In addition to compatibility improvements, this project includes dependency updates, bug fixes, stability improvements, and ongoing maintenance.

---

## ✨ Features

- Compatible with GOG Galaxy 2.1+ (64-bit)
- Python 3.13 support
- Updated 64-bit dependencies
- Improved login reliability
- Modern Ubisoft Connect compatibility
- Improved stability and compatibility
- Ongoing maintenance and bug fixes

---

## 🛠️ Technical Highlights

This section summarizes the parts of the plugin that make the integration work reliably on current 64-bit systems.

- ⚙️ **64-bit Registry Handling** - Ubisoft Connect installation data is read from the redirected 32-bit registry view when needed, with a fallback to the native registry view. This lets the plugin detect installed games correctly on modern 64-bit Windows systems.

- 🛡️ **Crash Protection in Game Loading** - The game loading path wraps local parsing and Ubisoft API calls in exception handling. If an API request or filesystem read fails, the plugin returns an empty result instead of crashing GOG Galaxy.

- 🔑 **Current Login and API Identifiers** - The login flow uses the current Ubisoft Connect login app ID, while API requests use a separate Ubisoft App ID. Legacy identifiers are kept as fallback values where needed.

- 🧹 **Bundled Runtime Dependencies** - The plugin ships with its required Python runtime modules in the `modules` folder so GOG Galaxy can load the integration without relying on a separate environment.

- 📄 **Usage and Recovery Notes** - The README includes installation steps, plugin database reset guidance, and support details to help with common setup issues.

---

## 📦 Installation

### Standard Installation (Recommended)

1. Close GOG Galaxy completely.
2. Download the latest release from this repository.
3. Open:

```text
%localappdata%\GOG.com\Galaxy\plugins\installed\
```

4. Extract the ZIP archive **directly into this folder**.

The resulting directory structure **must** look like this:

```text
%localappdata%\GOG.com\Galaxy\plugins\installed\
└── uplay_afb5a69c-b2ee-4d58-b916-f4cd75d4999a\
    ├── manifest.json
    ├── plugin.py
    ├── README.md
    └── ...
```

5. Start GOG Galaxy.

### If the plugin folder is missing

If a future ZIP archive does **not** already contain the folder:

```text
uplay_afb5a69c-b2ee-4d58-b916-f4cd75d4999a
```

1. Open:

```text
%localappdata%\GOG.com\Galaxy\plugins\installed\
```

2. Create a new folder with exactly that name.
3. Extract **all files from the ZIP archive into the newly created folder**.

---

## 🔄 Resetting the Plugin Database (Recommended)

If the plugin behaves unexpectedly after an update, resetting the local plugin database is recommended.

1. Open:

```text
C:\ProgramData\GOG.com\Galaxy\storage\plugins\
```

2. Locate all files beginning with:

```text
uplay_
```

and ending with:

```text
-storage.db
```

3. Rename each database by appending `.old` to its filename.

Example:

```text
uplay_xxxxxxxxx-storage.db
```

becomes

```text
uplay_xxxxxxxxx-storage.db.old
```

4. Start GOG Galaxy again.
5. Reconnect the Ubisoft Connect integration if necessary.

---

## ⚠️ Important

Do **not** place backup copies of this plugin inside the `plugins\installed` directory.

GOG Galaxy scans every folder inside this directory during startup. Duplicate plugin folders can lead to GUID conflicts or cause Galaxy to load an outdated version of the plugin.

---

## 🙏 Credits

**Original Community Integration**  
Friends of Galaxy  
https://github.com/FriendsOfGalaxy/galaxy-integration-uplay

**64-bit Port, Maintenance and Improvements**  
melcom

---

## 🤝 Support & Feedback

This project is developed and maintained by one person. Response times may vary, especially during periods when health-related limitations reduce available development time.

**GitHub Issues are intentionally disabled.**

If you would like to report a bug, suggest an improvement, or get in touch, please use the contact form on my website:

📩 https://melcom-creations.github.io/melcom-music/contact.html

Thank you for your patience and support!
