import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_current_user
from app.routers.get_calories import get_usda_client


def get_auth_token():
	login_payload = {
		"email": "john.doe@example.com",
		"password": "securepassword"
	}
	response = client.post("/auth/login", json=login_payload)
	assert response.status_code == 200
	return response.json()["token"]

client = TestClient(app)

def test_get_calories_success_mac_and_cheese():
	token = get_auth_token()
	payload = {"dish_name": "macaroni and cheese", "servings": 2}
	headers = {"Authorization": f"Bearer {token}"}
	response = client.post("/get-calories", json=payload, headers=headers)
	print("get_calories_success:", response.status_code, response.json())
	assert response.status_code == 200
	expected = {
		"dish_name": "MACARONI AND CHEESE",
		"servings": 2,
		"calories_per_serving": 102.0,
		"total_calories": 204.0,
		"protein_per_serving": 3.4,
		"fat_per_serving": 3.4,
		"carbohydrates_per_serving": 0.0,
		"source": "USDA FoodData Central",
		"similar_items": [
			{
				"dish_name": "MACARONI AND CHEESE",
				"servings": 2,
				"calories_per_serving": 110.0,
				"total_calories": 220.0,
				"protein_per_serving": 3.53,
				"fat_per_serving": 2.35,
				"carbohydrates_per_serving": 0.0,
				"source": "USDA FoodData Central",
				"brand": "Milton G. Waldbaum Company",
				"ingredients": "COOKED MACARONI (WATER, DURUM WHEAT SEMOLINA [ENRICHED WITH IRON (FERROUS SULFATE) AND B VITAMINS (NIACIN, THIAMIN MONONITRATE, RIBOFLAVIN, FOLIC ACID)]), WATER, SKIM MILK, MALTODEXTRIN, CHEDDAR CLUB CHEESE [CHEDDAR CHEESE (PASTEURIZED MILK, CHEESE CULTURE, SALT, ENZYMES), WATER, SALT, ANNATTO (COLOR)], SOYBEAN OIL, MODIFIED CORN STARCH, SALT, WHEY POWDER, WHEY PROTEIN CONCENTRATE, NATURAL FLAVORS, LECITHIN (SOY), XANTHAN GUM,POTASSIUM SORBATE,MUSTARD FLOUR, ONION POWDER, TURMERIC OLEORESIN, EXTRACTIVES OF PAPRIKA, SPICE."
			},
			{
				"dish_name": "MACARONI AND CHEESE",
				"servings": 2,
				"calories_per_serving": 101.0,
				"total_calories": 202.0,
				"protein_per_serving": 5.73,
				"fat_per_serving": 2.2,
				"carbohydrates_per_serving": 0.0,
				"source": "USDA FoodData Central",
				"brand": "Conagra Foodservice Frozen Prepared Foods",
				"ingredients": "WATER, COOKED ENRICHED PASTA (WATER, ENRICHED PASTA (DURUM WHEAT SEMOLINA, EGG WHITE, NIACIN, IRON [FERROUS SULFATE], THIAMINE MONONITRATE, RIBOFLAVIN, FOLIC ACID]), REDUCED FAT CHEDDAR CHEESE (PASTEURIZED PART SKIM MILK, CHEESE CULTURES, SALT, ENZYMES, ANNATTO AND VITAMIN A [COLOR]), NONFAT DRY MILK, CONTAINS LESS THAN 2% OF: CHEDDAR CLUB CHEESE (PASTEURIZED CULTURED MILK, SALT, ENZYMES, ANNATTO [COLOR]), WHEAT FLOUR, WHEY, MARGARINE (LIQUID AND HYDROGENATED SOYBEAN OIL, WATER, SALT, CONTAINS LESS THAN 2% OF VEGETABLE MONO & DIGLYCERIDES, SOY LECITHIN, SODIUM BENZOATE [A PRESERVATIVE], CITRIC ACID, NATURAL & ARTIFICIAL FLAVOR, CALCIUM DISODIUM EDTA ADDED TO PROTECT FLAVOR, BETA CAROTENE [COLOR], VITAMIN A PALMITATE ADDED), MODIFIED RICE STARCH, CHEESE FLAVOR (CREAM, CHEDDAR AND BLEU CHEESE [MILK, STARTER CULTURES, SALT, ENZYMES, WATER, NONFAT DRY MILK, DISODIUM PHOSPHATE, SODIUM CITRATE], CHEDDAR CHEESE [MILK, STARTER CULTURES, SALT, ENZYMES, WATER, DISODIUM PHOSPHATE, XANTHAN GUM, POTASSIUM SORBATE], CHEESE [MILK, SALT, STARTER CULTURES, ENZYMES, WATER, WHEY POWDER, NONFAT DRY MILK, SALT, DISODIUM PHOSPHATE], MALTODEXTRIN, AUTOLYZED YEAST EXTRACT), MODIFIED CORN STARCH, SALT, POTASSIUM CHLORIDE, SOYBEAN OIL, ANNATTO EXTRACT (REFINED SOY BEAN OIL, ANNATTO EXTRACT, MONO & DI-GLYCERIDES), SPICE, CITRIC ACID."
			},
			{
				"dish_name": "MACARONI AND CHEESE",
				"servings": 2,
				"calories_per_serving": 199.0,
				"total_calories": 398.0,
				"protein_per_serving": 8.64,
				"fat_per_serving": 12.3,
				"carbohydrates_per_serving": 0.0,
				"source": "USDA FoodData Central",
				"brand": "7-Eleven, Inc.",
				"ingredients": "THREE CHEESE MACARONI AND CHEESE (WATER, NOODLES (SEMOLINA, EGG WHITES, NIACIN, IRON (FERROUS SULFATE), THIAMIN MONONITRATE, RIBOFLAVIN, FOLIC ACID), WHIPPING CREAM, PASTEURIZED PROCESS WHITE CHEDDAR CHEESE (CHEDDAR CHEESE (PASTEURIZED MILK, CHEESE CULTURE, SALT, ENZYMES), WATER, SODIUM PHOSPHATE, MILKFAT, SALT), HAVARTI CHEESE (PASTEURIZED MILK, CHEESE CULTURE, SALT, ENZYMES), PARMESAN/ROMANO CHEESE BLEND (PASTEURIZED MILK, CHEESE CULTURES, SALT, ENZYMES, POWDERED CELLULOSE TO PREVENT CAKING), CREAM CHEESE (PASTEURIZED MILK AND CREAM, CHEESE CULTURE, SALT, STABILIZERS (CAROB BEAN AND/OR XANTHAN AND/OR GUAR GUMS)), MODIFIED CORN STARCH, EMULSIFIER (SODIUM POLYPHOSPHATE, SODIUM PHOSPHATE), SALT, SOY LECITHIN), CHEDDAR CHEESE (CHEDDAR CHEESE (PASTEURIZED MILK, CHEESE CULTURE, SALT, ENZYMES, ANNATTO (VEGETABLE COLOR), POTATO STARCH AND POWDERED CELLULOSE (TO PREVENT CAKING), NATAMYCIN (A NATURAL MOLD INHIBITOR)), BREADCRUMBS (WHEAT FLOUR, ROMANO AND PARMESAN CHEESE (PART SKIM COW'S MILK, CULTURES, ENZYMES, SALT), SOYBEAN OIL, SUGAR, SALT, YEAST, DEHYDRATED GARLIC, DEHYDRATED ONION, SPICES, MALTODEXTRIN, DEHYDRATED PARSLEY, UNSALTED BUTTER (PASTEURIZED CREAM, NATURAL FLAVOR), ENZYME MODIFIED BUTTER, NATURAL FLAVORS)"
			},
			{
				"dish_name": "MACARONI AND CHEESE",
				"servings": 2,
				"calories_per_serving": 171.0,
				"total_calories": 342.0,
				"protein_per_serving": 6.25,
				"fat_per_serving": 10.0,
				"carbohydrates_per_serving": 0.0,
				"source": "USDA FoodData Central",
				"brand": "Fresh Food Manufacturing",
				"ingredients": "COOKED PASTA (SEMOLINA, ENRICHED WITH NIACIN, FERROUS SULFATE, THIAMIN MONONITRATE, RIBOFLAVIN, FOLIC ACID), MILK, VITAMIN D3), PASTEURIZED PROCESSED CHEDDAR CHEESE (CHEDDAR CHEESE [CULTURED MILK, SALT, ENZYMES], CREAM, SODIUM PHOSPHATE, NATURAL FLAVOR, SALT, ANNATTO), WATER, BUTTERMILK (CULTURED LOWFAT MILK, NONFAT DRY MILK, SALT, SODIUM CITRATE, VITAMIN A PALMITATE, VITAMIN D3), CANOLA OIL, BUTTER (CREAM, NATURAL FLAVORS), CONTAINS 2% OR LESS OF CORN STARCH, SPICE, SALT, MUSTARD (WATER, VINEGAR, MUSTARD SEED, SALT, WHITE WINE, FRUIT PECTIN, CITRIC ACID, TARTARIC ACID, SUGAR, SPICE), MUSTARD POWDER, VEGETABLE BASE (VEGETABLES (CARROT, ONION, CELERY), SALT, CANE JUICE, CANOLA OIL, CARROT POWDER, POTATO FLOUR, ONION POWDER, BLACK PEPPER)."
			}
		]
	}
	data = response.json()
	assert data == expected

def test_get_calories_invalid_input():
	token = get_auth_token()
	payload = {"dish_name": "", "servings": 2}
	headers = {"Authorization": f"Bearer {token}"}
	response = client.post("/get-calories", json=payload, headers=headers)
	print("get_calories_invalid_input:", response.status_code, response.json())
	assert response.status_code == 400

def test_get_calories_invalid_servings():
	token = get_auth_token()
	payload = {"dish_name": "Chicken Curry", "servings": 0}
	headers = {"Authorization": f"Bearer {token}"}
	response = client.post("/get-calories", json=payload, headers=headers)
	print("get_calories_invalid_servings:", response.status_code, response.json())
	assert response.status_code == 400

def test_search_history_success():
	token = get_auth_token()
	headers = {"Authorization": f"Bearer {token}"}
	response = client.get("/search-history", headers=headers)
	print("search_history_success:", response.status_code, response.json())
	assert response.status_code == 200 or response.status_code == 500

def test_get_calories_grilled_salmon():
	token = get_auth_token()
	payload = {"dish_name": "grilled salmon", "servings": 3}
	headers = {"Authorization": f"Bearer {token}"}
	response = client.post("/get-calories", json=payload, headers=headers)
	print("get_calories_grilled_salmon:", response.status_code, response.json())
	assert response.status_code == 200
	expected = {
		"dish_name": "GRILLED SALMON",
		"servings": 3,
		"calories_per_serving": 103.0,
		"total_calories": 309.0,
		"protein_per_serving": 18.1,
		"fat_per_serving": 3.45,
		"carbohydrates_per_serving": 0.0,
		"source": "USDA FoodData Central",
		"similar_items": [
			{
				"dish_name": "GRILLED SALMON",
				"servings": 3,
				"calories_per_serving": 114.0,
				"total_calories": 342.0,
				"protein_per_serving": 7.86,
				"fat_per_serving": 3.21,
				"carbohydrates_per_serving": 0.0,
				"source": "USDA FoodData Central",
				"brand": "Ahold USA, Inc. ",
				"ingredients": "GRILLED SALMON (PINK AND/OR KETA SALMON, WATER, CONTAINS 2% OR LESS OF SALT, SUGAR, SODIUM PHOSPHATES, MALTODEXTRIN, DEHYDRATED GARLIC AND ONION, SPICES, XANTHAN GUM, PAPRIKA, NATURAL FLAVOR, SPICE EXTRACTIVES), STEAMED BROCCOLI (WATER, BROCCOLI FLORETS), BROWN RICE AND RED QUINOA (COOKED BROWN RICE [WATER, BROWN RICE], COOKED RED QUINOA [WATER, RED QUINOA]), COOKED WHITE RICE (ENRICHED LONG GRAIN PARBOILED RICE, THIAMIN, [THIAMIN MONONITRATE], NIACIN, IRON, [FERRIC PHOSPHATE], FOLIC ACID), FIRE ROASTED EDAMAME, RED BELL PEPPER, ROASTED CORN, CHIVE & GARLIC BUTTER (BUTTER [CREAM AND SALT], CHIVES, CANOLA & OLIVE OIL BLEND [75% CANOLA OIL, 25% EXTRA VIRGIN OLIVE OIL], GARLIC, SEA SALT, PEPPER)."
			},
			{
				"dish_name": "GRILLED SALMON",
				"servings": 3,
				"calories_per_serving": 196.0,
				"total_calories": 588.0,
				"protein_per_serving": 24.6,
				"fat_per_serving": 9.42,
				"carbohydrates_per_serving": 0.0,
				"source": "USDA FoodData Central",
				"brand": "Ukrop's Homestyle Foods, LLC",
				"ingredients": "SALMON, CANOLA OIL, SEA SALT, PEPPER; GARNISHED WITH FRESH LEMON AND PARSLEY."
			},
			{
				"dish_name": "GRILLED SALMON",
				"servings": 3,
				"calories_per_serving": 141.0,
				"total_calories": 423.0,
				"protein_per_serving": 8.1,
				"fat_per_serving": 5.33,
				"carbohydrates_per_serving": 0.0,
				"source": "USDA FoodData Central",
				"brand": "Preferred Meal Systems, Inc.",
				"ingredients": "ASIAN STICKY RICE (STICKY RICE (COOKED WHITE RICE (OR COOKED MEDIUM GRAIN WHITE RICE), CANOLA OIL, SUNFLOWER LECITHIN), FIRE ROASTED DICED RED PEPPER, HMR VEGETABLE SAUCE (WATER, MARGARINE (LIQUID SOYBEAN OIL, PARTIALLY HYDROGENATED SOYBEAN OIL, WATER, SALT, VEGETABLE MONO AND DIGLYCERIDES, VEGETABLE LECITHIN, SODIUM BENZOATE ADDED AS A PRESERVATIVE, ARTIFICIALLY FLAVORED, COLORED WITH BETA CAROTENE, VITAMIN A PALMITATE ADDED), FOOD STARCH-MODIFIED, SALT, ONION POWDER), TOASTED SESAME OIL (SESAME OIL (MADE FROM TOASTED WHITE SESAME SEEDS)), CHIVES, BLACK SESAME SEEDS, WHITE SESAME SEEDS, RICE WINE VINEGAR (DISTILLED VINEGAR, RICE VINEGAR, HIGH FRUCTOSE CORN SYRUP, SALT AND CARAMEL COLOR), GARLIC POWDER, BLACK PEPPER, GROUND GINGER), SAUTEED SESAME GINGER EDAMAME (EDAMAME BEANS, HMR VEGETABLE SAUCE (WATER, MARGARINE (LIQUID SOYBEAN OIL, PARTIALLY HYDROGENATED SOYBEAN OIL, WATER, SALT, VEGETABLE MONO AND DIGLYCERIDES, VEGETABLE LECITHIN, SODIUM BENZOATE ADDED AS A PRESERVATIVE, ARTIFICIALLY FLAVORED, COLORED WITH BETA CAROTENE, VITAMIN A PALMITATE ADDED), FOOD STARCH-MODIFIED, SALT, ONION POWDER), FIRE ROASTED DICED RED ONIONS, SCALLIONS, GINGER PUREE, TOASTED SESAME OIL (SESAME OIL (MADE FROM TOASTED WHITE SESAME SEEDS)), RICE WINE VINEGAR (DISTILLED VINEGAR, RICE VINEGAR, HIGH FRUCTOSE CORN SYRUP, SALT AND CARAMEL COLOR), WHITE SESAME SEEDS, BLACK PEPPER), FULLY COOKED SALMON GRILL MARKED PORTIONS BONELESS-SKINLESS (PINK AND/OR KETA SALMON, WATER, CONTAINS 2% OR LESS OF SALT, SUGAR, SODIUM PHOSPHATES, MALTODEXTRIN, DEHYDRATED GARLIC AND ONION, SPICES, XANTHAN GUM, PAPRIKA, NATURAL FLAVOR, SPICE EXTRACTIVES), SWEET CHILI GLAZE (SUGAR, WATER, LEMON JUICE (FILTERED WATER, LEMON JUICE CONCENTRATE, SODIUM BISULFITE (PRESERVATIVE), SODIUM BENZOATE (PRESERVATIVE), AND LEMON OIL), CHILI PASTE (CHILI, SALT, DISTILLED VINEGAR, POTASSIUM SORBATE AND SODIUM BISULFITE AS PRESERVATIVE), GARLIC PUREE (GARLIC, WATER, PHOSPHORIC ACID, XANTHAN GUM, SORBIC ACID, GARLIC EXTRACT), SRIRACHA CHILI SAUCE (CHILI, SUGAR, GARLIC, DISTILLED VINEGAR, POTASSIUM SORBATE, SODIUM BISULFITE AS PRESERVATIVES AND XANTHAN GUM), SALT, XANTHAN GUM, AQUARESIN PAPRIKA (NATURAL EXTRACTIVES OF PAPRIKA WITH MONO- AND DIGLYCERIDES, LECITHIN, AND SOYBEAN OIL)), SCALLIONS."
			},
			{
				"dish_name": "Fish, salmon, grilled",
				"servings": 3,
				"calories_per_serving": 259.0,
				"total_calories": 777.0,
				"protein_per_serving": 25.92,
				"fat_per_serving": 16.48,
				"carbohydrates_per_serving": 0.0,
				"source": "USDA FoodData Central",
				"brand": None,
				"ingredients": None
			}
		]
	}
	data = response.json()
	assert data == expected

def test_get_calories_paneer_butter_masala():
	token = get_auth_token()
	payload = {"dish_name": "paneer butter masala", "servings": 7}
	headers = {"Authorization": f"Bearer {token}"}
	response = client.post("/get-calories", json=payload, headers=headers)
	print("get_calories_paneer_butter_masala:", response.status_code, response.json())
	assert response.status_code == 200
	expected = {
		"dish_name": "PANEER BUTTER MASALA",
		"servings": 7,
		"calories_per_serving": 300.0,
		"total_calories": 2100.0,
		"protein_per_serving": 10.0,
		"fat_per_serving": 20.0,
		"carbohydrates_per_serving": 0.0,
		"source": "USDA FoodData Central",
		"similar_items": [
			{
				"dish_name": "BUTTER MASALA SAUCE",
				"servings": 7,
				"calories_per_serving": 88.0,
				"total_calories": 616.0,
				"protein_per_serving": 1.75,
				"fat_per_serving": 7.02,
				"carbohydrates_per_serving": 0.0,
				"source": "USDA FoodData Central",
				"brand": "Fuego Living LLC",
				"ingredients": "ONION, TOMATOES, WATER BUTTER (CREAM, SALT, MILK), KETCHUP, GARLIC, GREEN CHILI PEPPERS, GINGER, LEMON JUICE, BELL PEPPERS, SALT, SPICES (CHILI, CUMIN, TURMERIC, BLACK PEPPER, CORIANDER)."
			}
		]
	}
	data = response.json()
	assert data == expected
