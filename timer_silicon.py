import subprocess
import sys
import time

# OSCE timings in seconds
PHASES = [
    ("Reading time", 60, "Reading time begins now."),
    ("Doing time", 13 * 60, "Doing time begins now."),
    ("Final minute", 60, "One minute remaining."),
    ("Feedback", 3 * 60, "Feedback time begins now."),
    ("Changeover", 30, "Please change over to the next station."),
]

# Set to None to use your Mac's default voice, or a specific voice like "Samantha", "Daniel", etc.
VOICE = None

# Optional speech rate for macOS "say" command
RATE = 185


def speak(text: str) -> None:
    print(f"\n>>> {text}")
    sys.stdout.flush()

    cmd = ["say", "-r", str(RATE)]
    if VOICE:
        cmd += ["-v", VOICE]
    cmd.append(text)

    try:
        subprocess.run(cmd, check=False)
    except Exception as e:
        print(f"[Speech failed: {e}]")


def format_time(seconds: int) -> str:
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def countdown(label: str, total_seconds: int) -> None:
    for remaining in range(total_seconds, 0, -1):
        print(f"\r{label:<15} | {format_time(remaining)}", end="", flush=True)
        time.sleep(1)
    print(f"\r{label:<15} | 00:00")


def run_station(station_num: int, total_stations: int) -> None:
    print("\n" + "=" * 60)
    print(f"Station {station_num} of {total_stations}")
    print("=" * 60)

    for phase_name, duration, announcement in PHASES:
        speak(announcement)
        countdown(phase_name, duration)

    speak(f"Station {station_num} complete.")


def get_positive_int(prompt: str, default: int) -> int:
    raw = input(f"4{prompt} [{default}]: ").strip()
    if not raw:
        return default
    value = int(raw)
    if value < 1:
        raise ValueError("Value must be at least 1.")
    return value


def main() -> None:
    print("OSCE Circuit Timer for macOS")
    print("-" * 60)
    print("Tip: leave blank to accept defaults.\n")

    try:
        total_stations = get_positive_int("Number of stations", 1)
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    speak("The OSCE circuit will begin now.")

    for i in range(1, total_stations + 1):
        run_station(i, total_stations)

    speak("The OSCE circuit is now complete.")
    print("\nAll stations finished.")


if __name__ == "__main__":
    main()