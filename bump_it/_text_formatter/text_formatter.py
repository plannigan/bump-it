"""
Central place for performing text formatting.
"""
from datetime import date
from typing import Optional

from semantic_version import Version

from bump_it._error import FormatKeyError, FormatPatternError
from bump_it._text_formatter import keys


class TextFormatter:
    def __init__(
        self,
        current_version: Version,
        new_version: Version,
        today: Optional[date] = None,
    ) -> None:
        """
        Initialize an instance.

        :param current_version: Software version that is currently in use.
        :param new_version: Updated software version that is intended to be used as a replacement.
        :param today: The current date. If not provided `date.today()` will be used.
        """
        self._current_version = current_version
        self._new_version = new_version
        self._today = today or date.today()

    def format(self, format_pattern: str) -> str:
        """
        Perform string formatting on the given pattern.

        :param format_pattern: Pattern to be formatted.
        :return: Result of string formatting.
        :raises FormatError: Format pattern was invalid or attempted to use an invalid key.
        """
        # NOTE: pre-release and build may not exist for a version. If that is the case and the
        # pattern uses those keys, the resultant value will be an empty string.
        values = {
            keys.CURRENT_VERSION: self._current_version,
            keys.CURRENT_MAJOR: self._current_version.major,
            keys.CURRENT_MINOR: self._current_version.minor,
            keys.CURRENT_PATCH: self._current_version.patch,
            keys.CURRENT_PRERELEASE: _merge_parts(self._current_version.prerelease),
            keys.CURRENT_BUILD: _merge_parts(self._current_version.build),
            keys.NEW_VERSION: self._new_version,
            keys.NEW_MAJOR: self._new_version.major,
            keys.NEW_MINOR: self._new_version.minor,
            keys.NEW_PATCH: self._new_version.patch,
            keys.NEW_PRERELEASE: _merge_parts(self._new_version.prerelease),
            keys.NEW_BUILD: _merge_parts(self._new_version.build),
            keys.TODAY: self._today,
        }

        try:
            return format_pattern.format(**values)
        except KeyError:
            raise FormatKeyError(format_pattern, values.keys())
        except ValueError as ex:
            raise FormatPatternError(format_pattern, str(ex))


def _merge_parts(parts: tuple[str]) -> str:
    return ".".join(parts)
