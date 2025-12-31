import requests
import time

def test_app2_endpoint(iteration):
    response = requests.get("http://localhost:8000/")
    print(f"Req #{iteration} | Status: {response.status_code} | Body: {response.json()}")

counter = 1
print("Starting rate limit test...")
while counter <= 20:
    # Small sleep to simulate fast but not instantaneous requests
    time.sleep(0.2) 
    test_app2_endpoint(counter)
    counter += 1