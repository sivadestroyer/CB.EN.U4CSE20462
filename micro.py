from flask import Flask, request, jsonify
import requests
import concurrent.futures

app = Flask(__name__)

def fetch_numbers(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            data = response.json()
            return data.get('numbers', [])
    except requests.exceptions.Timeout:
        pass  # Ignore URLs that take too long to respond
    except Exception as e:
        print(f"Error fetching numbers from {url}: {e}")
    return []

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')
    unique_numbers = set()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(fetch_numbers, urls)
        for numbers in results:
            unique_numbers.update(numbers)
    
    sorted_numbers = sorted(unique_numbers)
    response = {"numbers": sorted_numbers}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
