"use server";
import { z } from "zod";
import type { MealState } from "@/types/meals";
import { getCalories } from "@/lib/api";

export async function mealFormAction(
  _prevState: MealState,
  formData: FormData
): Promise<MealState> {
  const dish_name = formData.get("dish_name") as string;
  const servings = formData.get("servings") !== null ? Number(formData.get("servings")) : NaN;
  const mealSchema = z.object({
    dish_name: z.string().min(1, { message: "Dish name is required" }),
    servings: z.number()
      .int({ message: "Servings must be a whole number" })
      .min(1, { message: "Servings must be at least 1" })
      .max(900, { message: "Servings must be at most 900" }),
  });

  const result = mealSchema.safeParse({ dish_name, servings });
  if (!result.success) {
    // console.log("Validation errors:", z.flattenError(result.error));
    return { success: false, error: z.flattenError(result.error), data: null };
  }

  const response = await getCalories(dish_name, servings);
  if (!response.success) {
    console.log("API error:", response.error);
    return { success: false, error: { formErrors: [response.error], fieldErrors: {} }, data: null };
  }

  return {
    success: true,
    error: null,
    data: {
      dish_name: response.data.dish_name,
      servings: response.data.servings,
      calories_per_serving: response.data.calories_per_serving,
      total_calories: response.data.total_calories,
      protein_per_serving: response.data.protein_per_serving,
      fat_per_serving: response.data.fat_per_serving,
      carbohydrates_per_serving: response.data.carbohydrates_per_serving,
      source: response.data.source,
      similar_items: response.data.similar_items,
    },
  };
}
