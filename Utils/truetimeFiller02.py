#!/usr/bin/env python3
"""
truetimeFiller.py

Compute two filler time windows around a user's work interval so that the total
accounted duration for the day is 10 hours.

Windows:
  1) 11:00 AM to one minute before work start
  2) one minute after work end to 9:0x PM (x is 2 or 3). We default to 9:02 PM.

Input (4 lines):
  start time (e.g., "12:28 PM")
  location (ignored)
  end time (e.g., "08:23 PM")
  location (ignored)

todo
- add some prints
- here some value should be 03 PM
Utils ➤ python truetimeFiller02.py                                                                                         git:main*
12:28 PM
PUN-CDC
08:23 PM
PUN-CDC
1. 11:00 AM - 12:27 PM
2. 08:24 PM - 09:02 PM
Utils ➤ python truetimeFiller02.py                                                                                         git:main*
12:01 PM
PUN-CDC
06:14 PM
PUN-CDC
1. 11:00 AM - 12:00 PM
2. 06:15 PM - 09:02 PM
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta

DAY_START_STR = "11:00 AM"
DAY_END_CANDIDATE_STRS = ("09:02 PM", "09:03 PM")
DEFAULT_DAY_END_INDEX = 0  # 0 => 09:02 PM, 1 => 09:03 PM


def ParseTime(timeStr: str) -> datetime:
    """Parse a 12-hour time like '12:28 PM' to a datetime on a reference date."""
    refDate = datetime(2000, 1, 1)
    try:
        parsed = datetime.strptime(timeStr.strip().upper(), "%I:%M %p")
        return refDate.replace(hour=parsed.hour, minute=parsed.minute, second=0, microsecond=0)
    except Exception as exc:
        raise ValueError(f"Invalid time format: '{timeStr}'. Expected like '12:28 PM'.") from exc


def FormatTime(dt: datetime) -> str:
    """Format datetime to 'HH:MM AM/PM' (e.g., '08:23 PM')."""
    return dt.strftime("%I:%M %p")


def FormatRange(startDt: datetime, endDt: datetime) -> str:
    """Format a time range 'HH:MM AM/PM - HH:MM AM/PM'."""
    return f"{FormatTime(startDt)} - {FormatTime(endDt)}"


def ChooseDayEndIndex() -> int:
    """Deterministically choose 9:02 PM to keep total duration exactly 10 hours."""
    return DEFAULT_DAY_END_INDEX


def ComputeWindows(workStart: datetime, workEnd: datetime) -> tuple[datetime, datetime, datetime, datetime]:
    """
    Compute:
      pre-window: [11:00 AM, workStart - 1 minute]
      post-window: [workEnd + 1 minute, 09:0x PM] (x=2 or 3; default 2)
    """
    dayStart = ParseTime(DAY_START_STR)
    dayEnd = ParseTime(DAY_END_CANDIDATE_STRS[ChooseDayEndIndex()])

    if workEnd <= workStart:
        raise ValueError("Work end time must be after work start time.")

    preStart = dayStart
    preEnd = workStart - timedelta(minutes=1)

    postStart = workEnd + timedelta(minutes=1)
    postEnd = dayEnd

    if preEnd < preStart:
        raise ValueError("Work start must be at least 1 minute after 11:00 AM to form the pre-window.")

    if postEnd < postStart:
        raise ValueError("Work end is too late to form the post-window up to 09:02 PM.")

    return preStart, preEnd, postStart, postEnd


def PrintResults(preStart: datetime, preEnd: datetime, postStart: datetime, postEnd: datetime) -> None:
    """Print the two required ranges."""
    print(f"1. {FormatRange(preStart, preEnd)}")
    print(f"2. {FormatRange(postStart, postEnd)}")


def main() -> None:
    """
    Read four lines: start time, location, end time, location (locations ignored).
    Then print the two filler windows.
    """
    try:
        startInput = input().strip()
        _location1 = input().strip()  # unused
        endInput = input().strip()
        _location2 = input().strip()  # unused

        workStart = ParseTime(startInput)
        workEnd = ParseTime(endInput)

        preStart, preEnd, postStart, postEnd = ComputeWindows(workStart, workEnd)
        PrintResults(preStart, preEnd, postStart, postEnd)

    except EOFError:
        print(
            "Error: Insufficient input. Provide four lines: start time, location, end time, location.",
            file=sys.stderr,
        )
        sys.exit(1)
    except ValueError as ve:
        print(f"Error: {ve}", file=sys.stderr)
        sys.exit(2)
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        sys.exit(99)


if __name__ == "__main__":
    main()
