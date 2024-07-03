# Uncomment the imports below before you add the function code
import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Define backend URL and sentiment analyzer URL from environment variables
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url', default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    """
    Send a GET request to specified endpoint with optional query parameters.

    Args:
        endpoint (str): The endpoint to append to the backend URL.
        **kwargs: Optional query parameters for the GET request.

    Returns:
        dict: The JSON response from the request.
    """
    params = ""
    if kwargs:
        params = "&".join(f"{key}={value}" for key, value in kwargs.items())

    request_url = f"{backend_url}{endpoint}?{params}"

    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Network exception occurred: {e}")
        return {"error": "Network exception occurred"}


def analyze_review_sentiments(text):
    """
    Send a GET request to sentiment analyzer URL to analyze review sentiments.

    Args:
        text (str): The text of the review to analyze.

    Returns:
        dict: The JSON response from the sentiment analysis.
    """
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Network exception occurred: {e}")
        return {"sentiment": "unknown"}


def post_review(data_dict):
    """
    Send a POST request to insert a review into the backend.

    Args:
        data_dict (dict): The review data to post.

    Returns:
        dict: The JSON response from the request.
    """
    request_url = f"{backend_url}/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        print(response.json())
        return response.json()
    except requests.RequestException as e:
        print(f"Network exception occurred: {e}")
        return {"error": "Network exception occurred"}
