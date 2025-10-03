"use client";

import { useAuthGuard } from "@/hooks/useAuthGuard";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { mealFormAction } from "@/actions/mealFormServerAction";
import type { MealState } from "@/types/meals";
import { useActionState, useState } from "react";
import { cn } from "@/lib/utils";
import { LoaderCircle } from "lucide-react";
import { MealInfoCard } from "@/components/mealInfoCard";
import { Skeleton } from "@/components/ui/skeleton";

const initialState = {
  success: false,
  error: null,
  data: null,
};

export default function MealForm() {
  const { isAuthenticated } = useAuthGuard();
  const [state, formAction, isPending] = useActionState<MealState, FormData>(
    mealFormAction,
    initialState
  );
  const [dish_name, setDishName] = useState("");
  const [servings, setServings] = useState(0);
  if (!isAuthenticated) {
    return null;
  }
  return (
    <main className="mb-5">
      <div className="w-full flex flex-col">
        <form action={formAction} className="w-full flex justify-center">
          <Card className="w-full max-w-xl">
            <CardHeader>
              <CardTitle>Meal Calorie Search</CardTitle>
              <CardDescription>
                Search for calorie information of various foods.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-6">
                <div className="grid gap-2">
                  <Label htmlFor="dish_name">Dish Name</Label>
                  <Input
                    id="dish_name"
                    name="dish_name"
                    type="text"
                    placeholder="e.g., Apple, Chicken Breast"
                    className={cn(
                      state.error?.fieldErrors?.dish_name &&
                        "border-destructive"
                    )}
                    value={dish_name}
                    onChange={(e) => setDishName(e.target.value)}
                  />
                  {state.error?.fieldErrors?.dish_name && (
                    <p className="text-destructive">
                      {state.error.fieldErrors.dish_name.join(", ")}
                    </p>
                  )}
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="servings">Servings</Label>
                  <Input
                    id="servings"
                    name="servings"
                    type="number"
                    placeholder="e.g., 1 medium, 200g"
                    className={cn(
                      state.error?.fieldErrors?.servings && "border-destructive"
                    )}
                    value={servings}
                    onChange={(e) => setServings(Number(e.target.value))}
                  />
                  {state.error?.fieldErrors?.servings && (
                    <p className="text-destructive">
                      {state.error.fieldErrors.servings.join(", ")}
                    </p>
                  )}
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex flex-col gap-2 justify-start items-start">
              <Button type="submit" disabled={isPending}>
                Search
                {isPending && (
                  <LoaderCircle className="ml-2 h-4 w-4 animate-spin" />
                )}
              </Button>
              {!isPending && !state.success && state.error && (
                <p className="text-destructive">
                  {state.error.formErrors.join(" ") || "Error occurred"}
                </p>
              )}
            </CardFooter>
          </Card>
        </form>
        {isPending && (
          <div className="w-full flex flex-col mt-8 gap-5">
            <h1 className="font-semibold text-lg">Search Result:</h1>
            <Skeleton className="h-48 w-full rounded-md" />
          </div>
        )}
        {!isPending && state.success && state.data && (
          <div className="w-full flex flex-col mt-8 gap-5">
            <h1 className="font-semibold text-lg">Search Results:</h1>
            <MealInfoCard data={state.data} />
          </div>
        )}
        {!isPending &&
          state.success &&
          state.data?.similar_items &&
          state.data.similar_items.length > 0 && (
            <div className="w-full flex flex-col mt-8 gap-5">
              <h1 className="font-semibold text-lg">Similar Items:</h1>
              <div className="grid md:grid-cols-2 gap-5">
                {state.data.similar_items.map((item, index) => (
                  <MealInfoCard
                    key={index}
                    data={item}
                    showBrandAndIngredients={true}
                  />
                ))}
              </div>
            </div>
          )}
      </div>
    </main>
  );
}
