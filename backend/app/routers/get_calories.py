from functools import lru_cache
from typing import Any

from fastapi import APIRouter, Depends, Request, HTTPException, status
from ..config import Settings
from typing_extensions import Annotated
from app.clients.usda import UsdaClient, parse_usda_search_results, fuzzy_search_one, fuzzy_search_all
from app.dependencies import get_current_user
from app.schemas.get_calories import dish, get_calories_response, get_calories_response_error, similar_result_item
from app.helpers.search_history import add_to_search_history
from fastapi.responses import JSONResponse
from app.helpers.search_history import get_search_history
from app.helpers.cache import get_cached_item, set_cached_item
from fastapi_limiter.depends import RateLimiter

router = APIRouter()


@lru_cache()
def get_settings():
    return Settings()


async def get_usda_client():
    client = UsdaClient(api_key=get_settings().usda_api_key)
    try:
        yield client
    finally:
        await client.close()


@router.post("/get-calories", dependencies=[Depends(RateLimiter(times=15, seconds=60))])
async def get_calories(
    dish: dish,
    usda_client: Annotated[UsdaClient, Depends(get_usda_client)],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)]
):
    try:
        if not dish.dish_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"detail": "Invalid input. Please provide a valid dish name", "status": "error"},
            )
        if dish.servings <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"detail": "Invalid Servings.", "status": "error"},
            )
        
        cache_response = get_cached_item(dish.dish_name.lower().strip())
        if cache_response and  cache_response.get("best_match") and cache_response.get("similar_items"):
                # print("Cache hit:")
                best_match = cache_response["best_match"]
                similar_results = cache_response["similar_items"]
        else:
            search_results = await usda_client.search_foods(dish.dish_name)
            if not search_results.get("foods"):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"detail": "No foods found for the given dish name.", "status": "error"},
                )
            parsed_results = parse_usda_search_results(search_results)
            best_match, result_index = fuzzy_search_one(dish.dish_name, parsed_results)
            if not best_match:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"detail": "No suitable match found for the given dish name.", "status": "error"},
                )
            similar_results = fuzzy_search_all(dish.dish_name, parsed_results, result_index)
            set_cached_item(dish.dish_name.lower().strip(), {"best_match": best_match, "similar_items": similar_results})
            # print("Cache miss. Data cached.")
        
        calories_info = best_match["nutrients"].get("Energy")
        if not calories_info:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"detail": "Calorie information not available for the matched food item.", "status": "error"},
            )

        user_email = current_user.get('email')
        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"detail": "User email missing from token.", "status": "error"},
            )
            
        similar_items = [
            similar_result_item(
                dish_name=item["name"],
                servings=dish.servings,
                calories_per_serving=item["nutrients"].get("Energy", {}).get("amount", 0),
                total_calories=item["nutrients"].get("Energy", {}).get("amount", 0) * dish.servings,
                protein_per_serving=item["nutrients"].get("Protein", {}).get("amount", 0),
                fat_per_serving=item["nutrients"].get("Total lipid (fat)", {}).get("amount", 0),
                carbohydrates_per_serving=item["nutrients"].get("Carbohydrates", {}).get("amount", 0),
                source="USDA FoodData Central",
                brand=item.get("brand"),
                ingredients=item.get("ingredients")
            )
            for item in similar_results
        ]
       
        response_data = get_calories_response(
            dish_name=best_match["name"],
            servings=dish.servings,
            calories_per_serving=calories_info["amount"],
            total_calories=calories_info["amount"] * dish.servings,
            protein_per_serving=best_match["nutrients"].get("Protein", {}).get("amount", 0),
            fat_per_serving=best_match["nutrients"].get("Total lipid (fat)", {}).get("amount", 0),
            carbohydrates_per_serving=best_match["nutrients"].get("Carbohydrates", {}).get("amount", 0),
            source="USDA FoodData Central",
            similar_items=similar_items
        )
        
        add_to_search_history_response = add_to_search_history(
            response_data=response_data,
            user_email=user_email,
            search_keyword=dish.dish_name
        )
        if add_to_search_history_response is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"detail": "Failed to log search history.", "status": "error"},
            )

        
        return response_data
    except HTTPException:
        raise 
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"detail": "Failed to get Info. Please try again in sometime!", "status": "error"},
        )

@router.get("/search-history", dependencies=[Depends(RateLimiter(times=15, seconds=60))])
async def search_history(
    current_user: Annotated[dict[str, Any], Depends(get_current_user)]
):
    try:
        user_email = current_user.get('email')
        if not user_email:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "User email missing from token.", "status": "error"},
            )
        
        history = get_search_history(user_email)
        if history is None:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Failed to retrieve search history.", "status": "error"},
            )
        
        history_list = [
            {
                "search_id": entry.id,
                "search_keyword": entry.search_keyword,
                "dish_name": entry.dish_name,
                "calories_per_serving": entry.calories_per_serving,
                "total_calories": entry.total_calories,
                "protein_per_serving": entry.protein_per_serving,
                "fat_per_serving": entry.fat_per_serving,
                "carbohydrates_per_serving": entry.carbohydrates_per_serving,
                "source": entry.source,
                "timestamp": entry.searched_at.isoformat()
            }
            for entry in history
        ]
        
        return {"status": "success", "history": history_list}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An error occurred while retrieving search history.", "status": "error"},
        )