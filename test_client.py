import json

import requests

BASE_URL = "http://localhost:8000"


def test_api():
    print("=== Testing Health Check ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        print("----------------------------\n")
    except Exception as e:
        print(f"Failed to connect to API: {e}")
        return

    print("=== Testing Clinical NER (Analyze Endpoint) ===")
    clinical_text = "Patient was diagnosed with Type 2 Diabetes Mellitus and prescribed Metformin 1000mg BID."
    payload = {"text": clinical_text}

    response = requests.post(f"{BASE_URL}/api/v1/analyze", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print("----------------------------\n")

    print("=== Testing Medical RAG (Query Endpoint) ===")
    query_payload = {
        "query": "What are the early signs and treatment for heart failure based on the recent chart?",
        "top_k": 2,
    }

    response = requests.post(f"{BASE_URL}/api/v1/query", json=query_payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print("----------------------------\n")


if __name__ == "__main__":
    test_api()
