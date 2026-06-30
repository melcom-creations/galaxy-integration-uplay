__version__ = "2.0.2-64bit"

__changelog__ = {
    "2.0.2-64bit": """
        - Restored the ownership filter in get_owned_games
        - Re-raises AuthenticationRequired so expired sessions are reported correctly
    """,
    "2.0.1-64bit": """
        - Added crash-safety wrappers around ownership and library parsing
        - Added safe fallback returns for external API and parsing failures
        - Updated login flow handling and Ubisoft API identifiers
        - Fixed 64-bit game detection by reading the WOW6432Node registry path
    """,
    "2.0.0-64bit": """
        - 64-bit migration for Python 3.13
        - Extracted dependencies to /modules/
        - Updated PyYAML to safe_load
        - Reworked the project for 64-bit Galaxy client compatibility
    """,
    "0.55.5": """
        - Fix parsing club games during owned games fetch
    """,
    "0.55.4": """
        - Hotfix for club games API endpoint
    """,
    "0.55.3": """
        - Login window title update
        - Deprecated endpoint replacement
        - Game time fixes for Ubisoft titles
        - Improved gametime rounding logic
    """,
    "0.55.2": """
        - Updated galaxy.plugin.api for stable get_local_size
    """,
    "0.55.1": """
        - Fixed blocking issue in get_local_size method
    """,
}
