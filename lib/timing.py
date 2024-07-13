from datetime import datetime, timedelta

class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = timedelta(0)
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = datetime.now() - self.elapsed_time
            self.running = True

    def pause(self):
        if self.running:
            self.elapsed_time = datetime.now() - self.start_time
            self.running = False

    def reset(self):
        self.start_time = None
        self.elapsed_time = timedelta(0)
        self.running = False
    
    def get_raw_time(self):
        if self.running:
            current_time = datetime.now() - self.start_time
        else:
            current_time = self.elapsed_time
        
        return current_time

    def get_time(self):
        if self.running:
            current_time = datetime.now() - self.start_time
        else:
            current_time = self.elapsed_time
        
        hours, remainder = divmod(current_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = (seconds - int(seconds)) * 1000
        seconds = int(seconds)
        
        return int(hours), int(minutes), int(seconds), int(milliseconds)

    def get_string_time(self):
        hours, minutes, seconds, milliseconds = self.get_time()
        return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"
    
    def get_dict_time(self):
        hours, minutes, seconds, milliseconds = self.get_time()
        return {
            "h": hours,
            "m": minutes,
            "s": seconds,
            "ms": milliseconds
        }