import time
import sys

# Optional text-to-speech support
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


STATION_PHASES = [
    ("Reading time", 60, "Reading time begins now."),
    ("Doing time", 13 * 60, "Doing time begins now."),
    ("Final minute", 60, "One minute remaining."),
    ("Feedback", 3 * 60, "Feedback time begins now."),
    ("Changeover", 30, "Please change over to the next station."),
]


def speak(message: str, engine=None) -> None:
    """Speak a message if text-to-speech is available, otherwise print only."""
    print(f"\n>>> {message}")
    sys.stdout.flush()

    # Terminal bell
    print("\a", end="")
    sys.stdout.flush()

    if engine is not None:
        engine.say(message)
        engine.runAndWait()


def format_time(seconds: int) -> str:
    """Convert seconds into MM:SS format."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def countdown(phase_name: str, total_seconds: int) -> None:
    """Display a live countdown for the current phase."""
    for remaining in range(total_seconds, 0, -1):
        print(f"\r{phase_name:<15} | Time remaining: {format_time(remaining)}", end="")
        sys.stdout.flush()
        time.sleep(1)
    print(f"\r{phase_name:<15} | Time remaining: 00:00")


def run_station(station_number: int, total_stations: int, engine=None) -> None:
    """Run one complete OSCE station."""
    print("\n" + "=" * 60)
    print(f"Starting station {station_number} of {total_stations}")
    print("=" * 60)

    for phase_name, duration, announcement in STATION_PHASES:
        speak(announcement, engine)
        countdown(phase_name, duration)

    speak(f"Station {station_number} complete.", engine)


def get_positive_int(prompt: str, default: int) -> int:
    """Read a positive integer from input, falling back to default if blank."""
    user_input = input(f"{prompt} [{default}]: ").strip()
    if not user_input:
        return default

    value = int(user_input)
    if value < 1:
        raise ValueError("Value must be at least 1.")
    return value


def main() -> None:
    print("OSCE Circuit Timer")
    print("-" * 60)

    if TTS_AVAILABLE:
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
    else:
        engine = None
        print("Note: pyttsx3 is not installed, so spoken announcements are disabled.")
        print("Install it with: pip install pyttsx3\n")

    try:
        total_stations = get_positive_int("Enter number of stations", 1)
    except ValueError as exc:
        print(f"Invalid input: {exc}")
        return

    speak("The OSCE circuit will begin now.", engine)

    for station_number in range(1, total_stations + 1):
        run_station(station_number, total_stations, engine)

    speak("The OSCE circuit is now complete.", engine)
    print("\nAll stations finished.")


if __name__ == "__main__":
    main()