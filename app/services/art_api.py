import httpx

ART_API_URL = "https://api.artic.edu/api/v1/artworks"

def get_artwork(external_id: int):
    response = httpx.get(f"{ART_API_URL}/{external_id}")
    if response.status_code != 200:
        return None
    
    data = response.json()
    return data.get('data')