import timeit, time

class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.stoptime = None

    def reset(self):
        self.start_time = timeit.default_timer()
        self.stoptime = self.start_time

    def set(self, from_now: float):
        """
        Sets the stopwatch timer.

        Args:
            from_now (float): Time in seconds
        """
        self.start_time = timeit.default_timer()
        self.stoptime = self.start_time + from_now

    def remaining(self) -> float:
        """
        Returns remaining time.

        Returns:
            float: Remaining time in seconds.
        """
        if self.start_time is None:
            raise ValueError("Stopwatch has not been started. Call set() to start the stopwatch.")
        current = timeit.default_timer()
        return 0 if current > self.stoptime else self.stoptime - current
    
    def remaining_ms(self, min = 0):
        """
        Returns remaining time.

        Returns:
            int: Remaining time in milliseconds.
        """
        return int(max(min, self.remaining() * 1000 + 0.5))
    
    def elapsed(self):
        return timeit.default_timer() - self.start_time
    
    def has_elapsed(self):
        return self.remaining_ms() < 1
    
"""# Beispiel-Nutzung:
stopwatch = Stopwatch()

# Starten der Stoppuhr für 2 Sekunden
stopwatch.set(2)

# Simulieren von 1 Sekunde vergangener Zeit
time.sleep(0.5)

# Abrufen der verbleibenden Zeit
remaining_time = stopwatch.remaining()
print(f"Remaining time: {remaining_time} seconds")

print(f"Remaining time: {stopwatch.remaining_ms()} milliseconds")

# Abrufen der vergangenen Zeit
elapsed_time = stopwatch.elapsed()
print(f"Elapsed time: {elapsed_time} seconds")"""
