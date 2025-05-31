import requests


class APIClient:

    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            'X-Api-Token': token,
            'Content-Type': 'application/json'
        }

    def get_products(self, query='cat:0'):
        try:
            response = requests.post(
                f'{self.base_url}/search',
                headers=self.headers,
                json={'q': query},
            )
            response.raise_for_status()
            products = response.json().get('items', [])
            print(f"[APIClient] Fetched {len(products)} products.")
            return products
        except requests.exceptions.RequestException as e:
            print(f"[APIClient] Error fetching products: {e}")
            return []

    def get_categories(self):
        try:
            response = requests.post(
                f'{self.base_url}/categories',
                headers=self.headers
            )
            response.raise_for_status()
            return response.json().get('items', [])
        except requests.exceptions.RequestException as e:
            print(f"[APIClient] Error fetching categories: {e}")
            return []
