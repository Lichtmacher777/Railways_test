def time_to_minutes(time: str) -> int:
    """Convert a time string ('%H:%M') to minutes since midnight."""
    time_parts = time.split(":")
    minutes = int(time_parts[0]) * 60 + int(time_parts[1])
    return minutes


def minutes_to_time(minutes: int) -> str:
    """Convert minutes since midnight to time string ('%H:%M')."""
    hours = int(minutes / 60)
    remaining_minutes = minutes - hours * 60
    return f"{hours:02}:{remaining_minutes:02}"
