export type MealFormValues = {
    dish_name: string;
    servings: string;
};

type MealFieldErrors = {
    [K in keyof MealFormValues]?: string[];
};

export type MealState = {
    success: boolean;
    error: {
        formErrors: string[];
        fieldErrors: MealFieldErrors;
    } | null;
    data: {
        dish_name: string;
        servings: number;
        calories_per_serving: number;
        total_calories: number;
        protein_per_serving: number;
        fat_per_serving: number;
        carbohydrates_per_serving: number;
        source: string;
        similar_items: {
            dish_name: string;
            servings: number;
            calories_per_serving: number;
            total_calories: number;
            protein_per_serving: number;
            fat_per_serving: number;
            carbohydrates_per_serving: number;
            source: string;
            brand: string;
            ingredients: string
        }[];
    } | null;
};

type MealSearchHistoryItem = {
    search_id: number;
    search_keyword: string;
    dish_name: string;
    calories_per_serving: number;
    total_calories: number;
    protein_per_serving: number;
    fat_per_serving: number;
    carbohydrates_per_serving: number;
    source: string;
    timestamp: string;
};

export type MealSearchHistoryProps = MealSearchHistoryItem[];