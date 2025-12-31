import time

class TokenBucket:
    def __init__(self, tokens, time_unit, forward_callback=None, drop_callback=None):
        self.tokens = tokens
        self.time_unit = time_unit
        self.forward_callback = forward_callback
        self.drop_callback = drop_callback
        self.bucket = tokens
        self.last_check = time.time()

    def handle(self):
        current = time.time()
        time_passed = current - self.last_check
        self.last_check = current

        # Calculate how many tokens to add based on time passed
        refill_amount = time_passed * (self.tokens / self.time_unit)
        self.bucket = self.bucket + refill_amount

        # Ensure bucket doesn't exceed max capacity
        if self.bucket > self.tokens:
            self.bucket = self.tokens

        print(f"--- Bucket Status ---")
        print(f"Refilled: +{refill_amount:.4f} tokens")
        print(f"Current Bucket Level: {self.bucket:.4f}")

        if self.bucket < 1:
            print("Result: [REJECTED] - Not enough tokens.")
            return False
        else:
            self.bucket -= 1
            print(f"Result: [ACCEPTED] - 1 token consumed. Remaining: {self.bucket:.4f}")
            return True

def forward(packet):
    print(f"Forwarded packet: {packet}")

def drop(packet):
    print(f"Dropped packet: {packet}")