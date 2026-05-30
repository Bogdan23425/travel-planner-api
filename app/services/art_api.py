import httpx

ART_API_URL = "https://api.artic.edu/api/v1/artworks"


class ArtApiUnavailable(Exception):
    pass


def get_artwork(external_id: int):
    try:
        response = httpx.get(
            f"{ART_API_URL}/{external_id}",
            timeout=5.0,
        )
    except httpx.RequestError as exc:
        raise ArtApiUnavailable("Art Institute API is unavailable") from exc

    if response.status_code == 404:
        return None

    if response.status_code >= 500:
        raise ArtApiUnavailable("Art Institute API returned an error")

    if response.status_code != 200:
        return None

    try:
        data = response.json()
    except ValueError as exc:
        raise ArtApiUnavailable("Invalid Art Institute API response") from exc

    return data.get("data")
