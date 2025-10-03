import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { MealState } from "@/types/meals";

type SimilarItem = NonNullable<MealState["data"]>["similar_items"][number];
type MainData = NonNullable<MealState["data"]>;

interface MealInfoCardProps {
  data: MainData | SimilarItem;
  showBrandAndIngredients?: boolean;
}

export function MealInfoCard({
  data,
  showBrandAndIngredients = false,
}: MealInfoCardProps) {
  return (
    <Card className="w-full max-w-xl">
      <CardHeader>
        <CardTitle className="text-2xl capitalize">
          {data?.dish_name.toLowerCase()}
        </CardTitle>
        <CardDescription>Nutritional Information</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4">
          {showBrandAndIngredients && "brand" in data && data.brand && (
            <div className="flex justify-between items-center border-b pb-2">
              <span className="font-medium">Brand:</span>
              <span className="text-lg">{data.brand}</span>
            </div>
          )}
          <div className="flex justify-between items-center border-b pb-2">
            <span className="font-medium">Servings:</span>
            <span className="text-lg">{data?.servings}</span>
          </div>
          <div className="flex justify-between items-center border-b pb-2">
            <span className="font-medium">Calories per Serving:</span>
            <span className="text-lg font-semibold">
              {data?.calories_per_serving} kcal
            </span>
          </div>
          <div className="flex justify-between items-center border-b pb-2 bg-primary/5 -mx-4 px-4 py-2">
            <span className="font-bold">Total Calories:</span>
            <span className="text-xl font-bold text-primary">
              {data?.total_calories} kcal
            </span>
          </div>
          <div className="grid gap-2 mt-2">
            <h4 className="font-semibold text-sm text-muted-foreground">
              Per Serving Macros:
            </h4>
            <div className="flex justify-between items-center">
              <span className="text-sm">Protein:</span>
              <span className="font-medium">{data?.protein_per_serving}g</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">Fat:</span>
              <span className="font-medium">{data?.fat_per_serving}g</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">Carbohydrates:</span>
              <span className="font-medium">
                {data?.carbohydrates_per_serving}g
              </span>
            </div>
          </div>
          {showBrandAndIngredients &&
            "ingredients" in data &&
            data.ingredients && (
              <div className="grid gap-2 mt-2">
                <h4 className="font-semibold text-sm text-muted-foreground">
                  Ingredients:
                </h4>
                <p className="text-sm">{data.ingredients}</p>
              </div>
            )}
        </div>
      </CardContent>
      <CardFooter className="text-xs text-muted-foreground">
        Source: {data?.source}
      </CardFooter>
    </Card>
  );
}
