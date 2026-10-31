from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests

@retry(
    stop=stop_after_attempt(5),  # Stop after 5 attempts
    wait=wait_exponential(multiplier=1, min=4, max=10), # Exponential backoff with min 4s, max 10s
    retry=retry_if_exception_type(requests.exceptions.ConnectionError) # Retry only on connection errors
)

def make_http_request(url):
    print(f"Attempting to access {url}...")
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    print(f"Successfully accessed {url}")
    return response.text

try:
    content = make_http_request("http://localhost:44777")
    # Process the content
except Exception as e:
    print(f"Failed to access URL after multiple retries: {e}")
