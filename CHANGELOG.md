# Changelog

All notable changes to this plugin will be documented in this file.

---

## v2.0.9-64bit

### Fixed in Version 2.0.9-64bit

- **Owned Ubisoft Libraries Were Incomplete:** The legacy Club GraphQL request can return only a subset of the PC games owned by an account, while the local Ubisoft ownership cache may also omit newer titles. The plugin now uses the current Ubisoft Connect entitlement endpoint as the authoritative ownership source, accepts only owned, non-expired game entitlements, and matches them to local entries through their space or product IDs. This restores titles that were present in Ubisoft Connect but missing from GOG Galaxy without treating every local configuration record as owned.
- **Owned Games Without Existing Local Metadata Could Not Be Imported:** Entitlements can identify owned games that are absent from the local Ubisoft cache. The plugin now retrieves their names and platform metadata in bounded batches, imports PC titles with stable Ubisoft space IDs, and keeps the previous Club request as a compatibility fallback for titles omitted by the current catalogue metadata response.

### Special Thanks for Version 2.0.9-64bit

- Thanks to **hausi2** for reporting the incomplete Ubisoft library and testing the fix.

---

## v2.0.8-64bit

### Fixed in Version 2.0.8-64bit

- **Login Window Remained Open After Successful Ubisoft Sign-In:** Ubisoft Connect can complete authentication inside its single-page application without loading another page, and a successful login may not provide the optional `PRODrememberMe` local-storage object. The previous flow checked local storage only when its script ran and required both session and remember-me data, so Galaxy could wait indefinitely after Ubisoft had already signed the user in. The login flow now watches for the required session fields, accepts missing optional remember-me and last-profile values, and completes through the dedicated `connect.ubisoft.com/change_domain/` URL.
- **Valid Missing Profile Data Caused Login to Fail:** Ubisoft may store `PRODlastProfile` as `null` even when the session credentials are valid. The credential parser attempted to iterate over every local-storage value and raised `TypeError` for this optional `null` entry, causing Galaxy to mark the integration as offline after closing the login window. Non-object optional entries are now ignored, while all required authentication fields remain validated before the session is accepted.
- **Duplicate Login Configuration Removed:** `plugin.py` imported the shared authentication parameters but then replaced them with a second inline copy. The login flow now uses the single configuration in `consts.py`, keeping the login URL, completion matcher, and injected authentication script consistent.

### Special Thanks for Version 2.0.8-64bit

- Thanks to **Kazio\_Wihura** for reporting the login issue and testing the fix.

---

## v2.0.7-64bit

### Fixed in Version 2.0.7-64bit

- **Static Types for Game State Constants:** `GameType`, `GameStatus`, and `ProcessType` provide string constants at runtime, but dataclass fields were annotated as enum instances. Static analysis therefore rejected valid `UbisoftGame` construction in the subscription and Club import paths. The annotations now match the runtime values.
- **Misleading Ownership-Path Warning Before Login:** The periodic local-status check could run before Ubisoft authentication supplied a user ID. The ownership path is intentionally unavailable at that point, but the plugin attempted to stat it anyway and logged that Ubisoft Connect might not be installed. The check now waits for initialization; a missing path after initialization remains a real warning.
- **Temporary Ubisoft+ Endpoint Failures Reported as Import Failures:** The optional Ubisoft+ catalogue endpoint can temporarily return `NetworkError`. This was propagated to Galaxy as a failed subscription import even though the ordinary Ubisoft library and authentication remained functional. The endpoint now logs a warning and reports no active subscription for that sync; the next scheduled sync retries normally.
- **Incomplete local launcher files no longer interrupt scanning:** Empty or truncated ownership/settings files, missing registry values, and inaccessible process data now stop only the affected local check safely.
- **Authentication timestamps and cached identities are validated:** Invalid session timestamps, missing authentication fields, and empty two-factor data now fail through the existing authentication flow rather than causing an unexpected exception.
- **Friend and subscription imports use the Galaxy API result types:** Friend entries and subscription generators now match the interface expected by the current Galaxy plugin API.

---

## v2.0.6-64bit

### Fixed in Version 2.0.6-64bit

- **Stale Game Status Not Refreshed When Launcher Log Is Empty:** `GameStatusNotifier._process_data` only recomputed game statuses when the Ubisoft Connect launcher log had readable lines in that cycle. Steam-owned games determine install status from the Windows registry, independent of the launcher log, so an empty or temporarily unavailable log left their status unrefreshed. This could leave a Steam-owned game reported as "not installed" even after installation completed. The status loop now recomputes statuses for all tracked games every cycle regardless of launcher log content.
- **Cache Directory Resolution Order:** `_resolve_cache_dir` now checks `%LOCALAPPDATA%\Ubisoft Game Launcher\cache` before falling back to `<InstallDir>\cache`, since current Ubisoft Connect installations keep the live `configuration`/`ownership` files there. Reading a stale install-directory cache could cause recently added games to be missing from the local configuration parse entirely.
- **Steam-Linked Config Records Discarded on Unresolved Name:** Configuration records for Steam-linked entries whose display name could not be resolved were previously skipped without a trace, so the plugin never learned their `install_id`, `launch_id`, or install status. Such records are now preserved with a placeholder name (`steam_linked_<id>`) so their metadata is available for merging.
- **Merge Logic Kept the Steam-Linked Placeholder Name:** Because the placeholder name `steam_linked_<id>` was not recognized as a placeholder, `_has_useful_name` treated it as valid, so the real title from the Club Request data was never merged in. GOG Galaxy could show `steam_linked_<id>` instead of the actual game title. `_has_useful_name` now also treats the `steam_linked_` prefix as a placeholder.
- **Merge Logic Overwrote `Steam` Type With `New`:** Once the previous fix allowed the Club Request entry (`type='New'`) to be merged into a Steam-linked entry, `_copy_preferred_metadata` unconditionally overwrote `target.type` with the incoming `type`, downgrading a Steam-linked entry to `New`. This caused a later status check for `GameType.New` to find no matching Ubisoft-registry install record and reset the game to "not installed", even though it was installed via Steam. `_copy_preferred_metadata` no longer overwrites `type` on a target that is already `GameType.Steam`.

### Known Issues in Version 2.0.6-64bit

- **Occasional Ghost Entries / Missing Free Extras:** Some accounts may see a title listed as owned in GOG Galaxy that no longer shows up in Ubisoft Connect, or vice versa (for example, free bonus content like the Discovery Tour editions of Assassin's Creed Origins/Odyssey not appearing at all). This comes from how Ubisoft's own backend reports ownership for these titles - the data the plugin receives from Ubisoft simply does not distinguish these cases from regular ownership, and in at least one observed case the same title's reported ownership changed on Ubisoft's side over time without any action from the user. There is currently no reliable way to detect or filter this from the plugin side.
- Thanks to **Randalator** from the GOG Community for reporting and helping narrow this down.

### Special Thanks for Version 2.0.6-64bit

Special thanks to **MacStew** from the GOG Community for the detailed testing and logs.
Without his report and follow-up verification, I would not have caught this issue because the plugin was working fine in my own environment.

---

## Version 2.0.5-64bit

### Overview for Version 2.0.5-64bit

Maintenance release focused on startup reliability and package-layout consistency. The update aligns ZIP root structure with plugin metadata and hardens dependency-path bootstrapping for bundled modules.

### Fixed in Version 2.0.5-64bit

- **Plugin Root Folder and Module Loader Normalization:** The ZIP root folder now matches the `guid` from `manifest.json` exactly, and the startup loader accepts `modules`, `Modules`, or any case-variant of that folder name before adding it to `sys.path`. This prevents start failures caused by a mismatched package root or a case-sensitive bundled module path.
- **YAML import startup hardening:** Improved `sys.path` bootstrap with normalized absolute-path handling and duplicate-path protection so bundled `yaml` is reliably discovered, preventing `ModuleNotFoundError: No module named 'yaml'` in edge-case runtime environments.

### Technical Breakdown for Version 2.0.5-64bit

#### 1. Package root and module resolution alignment

The plugin package root now matches manifest identity and dependency bootstrapping accepts module-folder case variants, preventing startup mismatches.

#### 2. Startup import robustness

Normalized absolute-path insertion and duplicate-path guards keep bundled dependency discovery stable across different runtime path states.

---

## Version 2.0.4-64bit

### Fixed in Version 2.0.4-64bit

- **Library Silently Emptied by a Single Bad Configuration Entry:** `LocalParser.parse_games()` parsed the Ubisoft configuration file as a Python generator. If any single game record in that file was malformed (corrupt/truncated YAML, or missing the expected `root` section), the resulting exception propagated out of the generator entirely, and `_parse_local_games()` in `plugin.py` only caught `scanner.ScannerError` — not `yaml.YAMLError`, `KeyError`, or `TypeError`. The exception therefore skipped `games_collection.extend(games)` completely, discarding every game already parsed for that pass, not just the bad one. Combined with `get_owned_games()`'s crash-safety wrapper, this could make the whole library appear empty and then reappear once the file changed again. Each configuration record is now parsed defensively; a malformed record is logged and skipped, and every other valid record is still added.
- **Race Condition on Ownership-File Reparse:** `tick()` checked `self.updating_games` on the main thread but the flag was only set to `True` inside the worker function `_update_games()`, which runs via `run_in_executor()`. If the ownership file changed again before the worker actually started, a second reparse could be scheduled on top of the first. The flag is now set on the main thread immediately before scheduling the worker.
- **Event Loop Blocked on Shutdown:** `BackendClient.close()` used a blocking `time.sleep(1.5)` inside an `async def`, freezing the entire plugin (not just the closing client) for up to 1.5 seconds during shutdown/reload. Replaced with `await asyncio.sleep(1.5)`.
- **Masked Errors During Auth Refresh:** `_refresh_auth()` used a bare `except:`, which also catches things like `asyncio.CancelledError` and reroutes them into a full remember-me refresh cycle instead of letting them propagate. Narrowed to `except Exception:` with proper logging.
- **Watched-Process Cleanup Could Skip Entries:** `update_watched_processes_list()` removed items from `self.watched_processes` while iterating over that same list, which can skip the entry immediately following a removed one. Now iterates over a snapshot copy.
- **False Process Match on Empty Game Path:** `_get_process_by_path()` checked `game.path.lower() in p.info['exe'].lower()`. When `game.path` was empty, this substring check was always `True`, so the first process psutil returned could be incorrectly reported as the running game. Now returns `None` immediately if the game has no known path.
- **Dead Code in `GamesCollection.append()`:** The override constructed an `AssertionError` but never raised it, so calling `.append()` directly would silently do nothing instead of failing loudly. It isn't currently called anywhere in the codebase, but now raises as originally intended, so any future misuse fails fast instead of failing silently.
- **Version Mismatch:** `version.py` reported `2.0.2-64bit` while `manifest.json` reported `2.0.3-64bit`. Both now report `2.0.4-64bit`.

### Removed in Version 2.0.4-64bit

- **Unused Console-Script Stubs (`idna.exe`, `chardetect.exe`):** Both files were pip-generated console-script entry points, byproducts of installing the `idna` and `chardet`/`charset-normalizer` packages. Neither is imported or called by the plugin at runtime; only the underlying Python modules are used. `idna.exe` embedded a local Windows account name in its shebang line, and `chardetect.exe` embedded an internal CI workspace path. Both files have been removed from the package.

---

## Version 2.0.3-64bit

### Fixed in Version 2.0.3-64bit

- **Installed Games Not Detected (Cache Directory Moved by Ubisoft Connect):** On newer Ubisoft Connect installations, the client now stores its cache folder (containing the `ownership`, `configuration`, and `settings` files) under `%LOCALAPPDATA%\Ubisoft Game Launcher\cache` instead of `<InstallDir>\cache`. The plugin previously only looked in `<InstallDir>\cache`, causing `import_local_games` to always return an empty list - owned games showed up correctly, but none were recognized as installed, so they couldn't be launched from GOG Galaxy. Added a new `_resolve_cache_dir(install_path)` method that checks `<InstallDir>\cache` first and falls back to `%LOCALAPPDATA%\Ubisoft Game Launcher\cache` if not present. `refresh()` now uses the resolved cache directory for all three paths. Existing installations with the cache still in `InstallDir` are unaffected.

### Notes for Version 2.0.3-64bit

- We also checked whether the plugin uses an `activations` folder (created by Ubisoft Connect when a game is installed or launched) that could have the same install-location problem. It doesn't - this plugin never reads that folder, so there's nothing to fix there.

### Thanks for Version 2.0.3-64bit

- Special thanks to GOG Community member **MacStew** for the detailed log files that helped track this down! 🙂

---

## Version 2.0.2-64bit

### Fixed in Version 2.0.2-64bit

- **Ownership Filter Regression in `get_owned_games`:** The `2.0.1` crash-safety rework had also dropped the `if game.owned` filter when building the list returned to GOG Galaxy, so the API would return every entry in `games_collection` regardless of confirmed ownership. Since `UbisoftGame.owned` defaults to `None` and entries can be added from local configuration parsing before the separate ownership file has been matched, this risked surfacing unowned or unconfirmed titles in the GOG library. The ownership filter has been restored; the crash-safety wrapper is kept as a separate, additive layer rather than a replacement for it.
- **Swallowed Authentication State:** `get_owned_games`'s safety wrapper now re-raises `AuthenticationRequired` instead of catching it like any other error. Previously an expired/invalid session could be reported back to GOG Galaxy as "zero owned games" instead of "please log in again".

---

## Version 2.0.1-64bit

### Fixed in Version 2.0.1-64bit

- **Core Stability Layer (Crash Prevention):** Introduced a global safety wrapper around ownership and library parsing to prevent uncaught exceptions from propagating into GOG Galaxy and triggering plugin reloads.
- **Crash Prevention in Game Import Flow:** Wrapped local game parsing and ownership resolution in safe execution blocks to ensure Ubisoft API failures or filesystem issues no longer crash the plugin.
- **Safe API Response Handling:** All external API calls now enforce safe fallback returns (empty lists instead of exceptions) to guarantee consistent data delivery to GOG Galaxy.
- **Authentication & Login Flow Fixes:** Fixed Ubisoft login flow issues, including outdated redirect handling and authentication endpoint mismatches. Login now uses current Ubisoft Connect appId/genomeId with fallback to legacy identifiers and safe post-login redirects.
- **API Authentication Fix (403 Errors):** Resolved issue where deprecated Ubisoft API identifiers caused 403 Forbidden responses after login. All API calls now use updated Ubisoft Connect identifiers.
- **Installed Games Detection (64-bit Registry Fix):** Fixed issue where Ubisoft Connect games were not detected correctly on 64-bit systems by correctly reading the WOW6432Node registry path.

### Changed in Version 2.0.1-64bit

- Improved internal error isolation across all core plugin execution paths.
- Standardized fallback behavior for failed API and parsing operations.

### Notes for Version 2.0.1-64bit

- This release combines multiple internal fixes and stability improvements.
- Earlier overlapping fixes were consolidated for clarity without changing functionality.

---

## Version 2.0.0-64bit

### Overview for Version 2.0.0-64bit

Major 64-bit overhaul for GOG Galaxy 2.1+ compatibility. The dependency stack was modernized and aligned for Python 3.13. Project maintenance was taken over by melcom.

### Changed in Version 2.0.0-64bit

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
