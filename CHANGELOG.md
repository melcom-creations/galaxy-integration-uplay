# Changelog

All notable changes to the **Galaxy Ubisoft Connect plugin** will be documented in this file.

---

## Version 2.0.3-64bit

### Fixed

- **Installed Games Not Detected (Cache Directory Moved by Ubisoft Connect):** On newer Ubisoft Connect installations, the client now stores its cache folder (containing the `ownership`, `configuration`, and `settings` files) under `%LOCALAPPDATA%\Ubisoft Game Launcher\cache` instead of `<InstallDir>\cache`. The plugin previously only looked in `<InstallDir>\cache`, causing `import_local_games` to always return an empty list — owned games showed up correctly, but none were recognized as installed, so they couldn't be launched from GOG Galaxy. Added a new `_resolve_cache_dir(install_path)` method that checks `<InstallDir>\cache` first and falls back to `%LOCALAPPDATA%\Ubisoft Game Launcher\cache` if not present. `refresh()` now uses the resolved cache directory for all three paths. Existing installations with the cache still in `InstallDir` are unaffected.

### Notes

- The `activations` folder (created when a game is installed/launched) has not yet been audited for the same InstallDir-vs-AppData discrepancy; flagged for a future release.

### Thanks

- Special thanks to GOG Community member **MacStew** for the detailed log files that helped track this down! 🙂

---

## Version 2.0.2-64bit

### Fixed

- **Ownership Filter Regression in `get_owned_games`:** The `2.0.1` crash-safety rework had also dropped the `if game.owned` filter when building the list returned to GOG Galaxy, so the API would return every entry in `games_collection` regardless of confirmed ownership. Since `UbisoftGame.owned` defaults to `None` and entries can be added from local configuration parsing before the separate ownership file has been matched, this risked surfacing unowned or unconfirmed titles in the GOG library. The ownership filter has been restored; the crash-safety wrapper is kept as a separate, additive layer rather than a replacement for it.
- **Swallowed Authentication State:** `get_owned_games`'s safety wrapper now re-raises `AuthenticationRequired` instead of catching it like any other error. Previously an expired/invalid session could be reported back to GOG Galaxy as "zero owned games" instead of "please log in again".

---

## Version 2.0.1-64bit

### Fixed

- **Core Stability Layer (Crash Prevention):** Introduced a global safety wrapper around ownership and library parsing to prevent uncaught exceptions from propagating into GOG Galaxy and triggering plugin reloads.
- **Crash Prevention in Game Import Flow:** Wrapped local game parsing and ownership resolution in safe execution blocks to ensure Ubisoft API failures or filesystem issues no longer crash the plugin.
- **Safe API Response Handling:** All external API calls now enforce safe fallback returns (empty lists instead of exceptions) to guarantee consistent data delivery to GOG Galaxy.
- **Authentication & Login Flow Fixes:** Fixed Ubisoft login flow issues, including outdated redirect handling and authentication endpoint mismatches. Login now uses current Ubisoft Connect appId/genomeId with fallback to legacy identifiers and safe post-login redirects.
- **API Authentication Fix (403 Errors):** Resolved issue where deprecated Ubisoft API identifiers caused 403 Forbidden responses after login. All API calls now use updated Ubisoft Connect identifiers.
- **Installed Games Detection (64-bit Registry Fix):** Fixed issue where Ubisoft Connect games were not detected correctly on 64-bit systems by correctly reading the WOW6432Node registry path.

### Changed

- Improved internal error isolation across all core plugin execution paths.
- Standardized fallback behavior for failed API and parsing operations.

### Notes

- This release combines multiple internal fixes and stability improvements.
- Earlier overlapping fixes were consolidated for clarity without changing functionality.

---

## Version 2.0.0-64bit

### Overview
Major 64-bit overhaul for GOG Galaxy 2.1+ compatibility. The dependency stack was modernized and aligned for Python 3.13. Project maintenance was taken over by melcom.

### Changed
- 64-bit migration of all third-party dependencies for Python 3.13.
- Extraction of external libraries into `/modules/`.
- PyYAML security fix using `safe_load`.
- Project restructured for 64-bit Galaxy client compatibility.

---

## Version 0.55.5
- Fix parsing club games during owned games fetch.

## Version 0.55.4
- Hotfix for club games API endpoint.

## Version 0.55.3
- Login window title update.
- Deprecated endpoint replacement.
- Game time fixes for Ubisoft titles.
- Improved gametime rounding logic.

## Version 0.55.2
- Updated galaxy.plugin.api for stable get_local_size.

## Version 0.55.1
- Fixed blocking issue in get_local_size method.