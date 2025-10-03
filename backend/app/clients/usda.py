from httpx import AsyncClient
from rapidfuzz import process, fuzz

class UsdaClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.nal.usda.gov/fdc/v1"
        self.client = AsyncClient(timeout=10.0)

    async def search_foods(self, query: str):
        params = {
            "api_key": self.api_key,
            "query": query,
        }
        url = f"{self.base_url}/foods/search"
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()


def parse_usda_food_item(item: dict) -> dict:
        return {
            "id": item.get("fdcId"),
            "name": item.get("description"),
            "brand": item.get("brandOwner"),
            "ingredients": item.get("ingredients"),
            "nutrients": {
                nutrient["nutrientName"]: {
                    "amount": nutrient.get("value") or 0,
                    "unit": nutrient.get("unitName") or "",
                }
                for nutrient in item.get("foodNutrients", [])
            },
        }


def parse_usda_search_results(results: dict) -> list:
    parsed_results = []
    for item in results.get("foods", []):
        parsed_results.append(parse_usda_food_item(item))
    return parsed_results


def fuzzy_search_one(query: str, results: list) -> tuple[dict, int] | tuple[None, None]:
    if not results:
        return None, None
    
    def normalize(text: str) -> str:
        return text.lower().strip()

    choices = [normalize(result["name"]) for result in results]

    for n, choice in enumerate(choices):
        if choice == normalize(query):
            # Return exact match and a dummy best_match tuple
            return results[n], n

    best_match = process.extractOne(
        normalize(query), choices, scorer=fuzz.token_sort_ratio
    )
    # print(best_match)
    if best_match:
        return results[best_match[2]], best_match[2]
    return None, None

def fuzzy_search_all(query: str, results: list, result_index: int | None, threshold: int = 80) -> list:
    if not results:
        return []
    
    def normalize(text: str) -> str:
        return text.lower().strip()

    choices = [normalize(result["name"]) for result in results]

    matches = process.extract(
        normalize(query), choices, scorer=fuzz.token_sort_ratio, score_cutoff=threshold
    )

    if result_index is not None:
        filtered_matches = [results[match[2]] for match in matches if match[2] != result_index]
    else:
        filtered_matches = [results[match[2]] for match in matches]
    return filtered_matches