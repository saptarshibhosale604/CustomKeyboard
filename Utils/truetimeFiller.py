#!/usr/bin/env python3
"""
truetimeFiller.py

A simple, production-ready utility that computes two filler time windows around a user's
actual work interval so that the total accounted duration is 10 hours.

Logic
-----
Given a fixed day window that starts at 11:00 AM and ends at 09:0x PM, where x is 2 or parsed = datetime.strptime(timeStr.strip().upper(), "%I:%M %p")Given a fixed day window that starts at 11:00 AM and ends at 09:0x PM, where x is 2 or 3,
        return refDate.replace(hour=parsed.hour, minute=parsed.minute, second=0, microsecond=0)
    except Exception as exc:
        raise ValueError(f"Invalid time format: '{timeStr}'. Expected like '12:28 PM'.") from exc


def FormatTime(dt: datetime) -> str:
    """Format a datetime to 'HH:MM AM/PM' with leading zero for hour (e.g., '08:23 PM')."""
    return dt.strftime("%I:%M %p")


def FormatRange(startDt: datetime, endDt: datetime) -> str:
    """Format a time range 'HH:MM AM/PM - HH:MM AM/PM'."""
    return f"{FormatTime(startDt)} - {FormatTime(endDt)}"


def ChooseDayEndIndex() -> int:
    # Choose the day-end index (0 => 09:02 PM, 1 => 09:03 PM).
    # Choose the day-end index: 0 = 09:02 PM, 1 = 09:03 PM.
    # Choose the day-end index (0 = 09:02 PM, 1 = 09:03 PM).
    # Choose the day-end index (0 = 09-02 PM, 1 = 09-03 PM).
    """

    The requirement says x should be 2 or 3 so that the total duration is 10 hours.
    Using exclusive interval math, o09:02 PM yields exactly 10 hours total.
    We keep the logic simple and deterministic by returning 0 (09:02 PM).
    """
    return DEFAULT_DAY_END_INDEX


def ComputeWindows(workStart: datetime, workEnd: datetime) -> tuple[datetime, datetime, datetime, datetime]:
    """Compute the two filler windows around the work interval.

    Window 1: [11:00 AM, workStart - 1 minute]
    Window 2: [workEnd + 1 minute, 09:0x PM]

    Args:
        workStart: Start of work interval.
        workEnd: End of work interval.

    Returns:
        A tuple: (preStart, preEnd, postStart, postEnd)

    Raises:
        ValueError: If computed windows are invalid (negative durations or out of bounds).
    """
    dayStart = ParseTime(DAY_START_STR)
    dayEnd = ParseTime(DAY_END_CANDIDATE_STRS[ChooseDayEndIndex()])

    if workEnd <= workStart:
        raise ValueError("Work end time must be after work start time.")

    # Compute pre-window
    preStart = dayStart
    preEnd = workStart - timedelta(minutes=1)

    # Compute post-window
    postStart = workEnd + timedelta(minutes=1)
    postEnd = dayEnd

    # Validate windows fall within the day bounds
    if preEnd < preStart:
        raise ValueError(
            "Work start time must be at least 1 minute after 11:00 AM to form a valid pre-window."
        )

    if postEnd < postStart:
        raise ValueError(
            "Work end time is too late to form a valid post-window with the chosen day end (09:02 PM)."
        )

    return preStart, preEnd, postStart, postEnd


def PrintResults(preStart: datetime, preEnd: datetime, postStart: datetime, postEnd: datetime) -> None:
    """Print the two required ranges in the specified format."""
    print(f"1. {FormatRange(preStart, preEnd)}")
    print(f"2. {FormatRange(postStart, postEnd)}")


def main() -> None:
    """Entry point for the script.

    Interactively reads four lines (time, location, time, location), ignoring the two
    location lines, then prints the two filler time windows.
    """
    try:
        # Read inputs (compatible with the provided example)
        startInput = input().strip()
        _location1 = input().strip()  # Accepted but unused
        endInput = input().strip()
        _location2 = input().strip()  # Accepted but unused

        workStart = ParseTime(startInput)
        workEnd = ParseTime(endInput)

        preStart, preEnd, postStart, postEnd = ComputeWindows(workStart, workEnd)
        PrintResults(preStart, preEnd, postStart, postEnd)

    except EOFError:
        # Handle cases where fewer lines are provided
        print(
            "Error: Insufficient input. Please provide four lines: start time, location, end time, location.",
            file=sys.stderr,
        )
        sys.exit(1)
    except ValueError as ve:
        print(f"Error: {ve}", file=sys.stderr)
        sys.exit(2)
    except Exception as exc:
        # Catch-all for unexpected errors
        print(f"Unexpected error: {exc}", file=sys.stderr)
        sys.exit(99)


if __name__ == "__main__":
    main()
we output two ranges:
  1) From 11:00 AM to (work_start - 1 minute)
  2) From (work_end + 1 minute) to 09:0x PM

To keep the logic simple and to ensure the total accounted duration is 10 hours, this
script defaults the end-of-day to 09:02 PM. With exclusive interval math, this yields
exactly 10 hours total across:
  pre-window + work-window + post-window

Notes
-----
- Input times must be in 12-hour format like "12:28 PM" (case-insensitive).
- Locations lines are accepted (as in the example) but are not used in calculations.
- All errors are handled gracefully with informative messages.

Examples
--------
Input (four separate lines):
  12:28 PM
  PUN-CDC
  08:23 PM
  PUN-CDC

Output:
  1. 11:00 AM - 12:27 PM
  2. 08:24 PM - 09:02 PM

(The sample above ensures exactly 10 hours total across the three windows.)

Author: M365 Copilot
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta

# Constants
DAY_START_STR = "11:00 AM"
# To make total accounted duration exactly 10 hours (600 minutes), we choose 09:02 PM by default.
DAY_END_CANDIDATE_STRS = ("09:02 PM", "09:03 PM")
DEFAULT_DAY_END_INDEX = 0  # 0 -> 09:02 PM, 1 -> 09:03 PM


def ParseTime(timeStr: str) -> datetime:
    """Parse a time string like '12:28 PM' into a datetime anchored to an arbitrary date.

    Args:
        timeStr: Time string in 12-hour format with AM/PM (case-insensitive).

    Returns:
        datetime: A datetime object on an arbitrary reference date.

    Raises:
        ValueError: If the time string cannot be parsed.
    """
    # Use a fixed reference date to make arithmetic straightforward.
    refDate = datetime(2000, 1, 1)
    try:

