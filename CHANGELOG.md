# Changelog

All notable changes to the **Galaxy Ubisoft Connect plugin** will be documented in this file.

---

## Version 2.0.4-64bit

### Fixed

- **Library Silently Emptied by a Single Bad Configuration Entry:** `LocalParser.parse_games()` parsed the Ubisoft configuration file as a Python generator. If any single game record in that file was malformed (corrupt/truncated YAML, or missing the expected `root` section), the resulting exception propagated out of the generator entirely, and `_parse_local_games()` in `plugin.py` only caught `scanner.ScannerError` — not `yaml.YAMLError`, `KeyError`, or `TypeError`. The exception therefore skipped `games_collection.extend(games)` completely, discarding every game already parsed for that pass, not just the bad one. Combined with `get_owned_games()`'s crash-safety wrapper, this could make the whole library appear empty and then reappear once the file changed again. Each configuration record is now parsed defensively; a malformed record is logged and skipped, and every other valid record is still added.
- **Race Condition on Ownership-File Reparse:** `tick()` checked `self.updating_games` on the main thread but the flag was only set to `True` inside the worker function `_update_games()`, which runs via `run_in_executor()`. If the ownership file changed again before the worker actually started, a second reparse could be scheduled on top of the first. The flag is now set on the main thread immediately before scheduling the worker.
- **Event Loop Blocked on Shutdown:** `BackendClient.close()` used a blocking `time.sleep(1.5)` inside an `async def`, freezing the entire plugin (not just the closing client) for up to 1.5 seconds during shutdown/reload. Replaced with `await asyncio.sleep(1.5)`.
- **Masked Errors During Auth Refresh:** `_refresh_auth()` used a bare `except:`, which also catches things like `asyncio.CancelledError` and reroutes them into a full remember-me refresh cycle instead of letting them propagate. Narrowed to `except Exception:` with proper logging.
- **Watched-Process Cleanup Could Skip Entries:** `update_watched_processes_list()` removed items from `self.watched_processes` while iterating over that same list, which can skip the entry immediately following a removed one. Now iterates over a snapshot copy.
- **False Process Match on Empty Game Path:** `_get_process_by_path()` checked `game.path.lower() in p.info['exe'].lower()`. When `game.path` was empty, this substring check was always `True`, so the first process psutil returned could be incorrectly reported as the running game. Now returns `None` immediately if the game has no known path.
- **Dead Code in `GamesCollection.append()`:** The override constructed an `AssertionError` but never raised it, so calling `.append()` directly would silently do nothing instead of failing loudly. It isn't currently called anywhere in the codebase, but now raises as originally intended, so any future misuse fails fast instead of failing silently.
- **Version Mismatch:** `version.py` reported `2.0.2-64bit` while `manifest.json` reported `2.0.3-64bit`. Both now report `2.0.4-64bit`.

### Removed

- **Unused Console-Script Stubs (`idna.exe`, `chardetect.exe`):** Both files were pip-generated console-script entry points, byproducts of installing the `idna` and `chardet`/`charset-normalizer` packages. Neither is imported or called by the plugin at runtime; only the underlying Python modules are used. `idna.exe` embedded a local Windows account name in its shebang line, and `chardetect.exe` embedded an internal CI workspace path. Both files have been removed from the package.

---

## Version 2.0.3-64bit

### Fixed

- **Installed Games Not Detected (Cache Directory Moved by Ubisoft Connect):** On newer Ubisoft Connect installations, the client now stores its cache folder (containing the `ownership`, `configuration`, and `settings` files) under `%LOCALAPPDATA%\Ubisoft Game Launcher\cache` instead of `<InstallDir>\cache`. The plugin previously only looked in `<InstallDir>\cache`, causing `import_local_games` to always return an empty list - owned games showed up correctly, but none were recognized as installed, so they couldn't be launched from GOG Galaxy. Added a new `_resolve_cache_dir(install_path)` method that checks `<InstallDir>\cache` first and falls back to `%LOCALAPPDATA%\Ubisoft Game Launcher\cache` if not present. `refresh()` now uses the resolved cache directory for all three paths. Existing installations with the cache still in `InstallDir` are unaffected.

### Notes

- We also checked whether the plugin uses an `activations` folder (created by Ubisoft Connect when a game is installed or launched) that could have the same install-location problem. It doesn't - this plugin never reads that folder, so there's nothing to fix there.

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