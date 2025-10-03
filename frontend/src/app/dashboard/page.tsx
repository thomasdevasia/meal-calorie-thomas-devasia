"use client";

import { useAuthGuard } from "@/hooks/useAuthGuard";
import { getMealSearchHistory } from "@/lib/api";
import { useEffect, useState } from "react";
import { MealInfoCard } from "@/components/mealInfoCard";
import { Skeleton } from "@/components/ui/skeleton";
import type { MealSearchHistoryProps } from "@/types/meals";

export default function DashboardPage() {
  const { isAuthenticated } = useAuthGuard();

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="flex flex-col gap-4">
      <header>
        <h1 className="text-3xl font-semibold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome to your dashboard! Here you can view your recent activity.
        </p>
      </header>
      <main className="mb-8">
        <div className="w-full max-w-4xl flex flex-col gap-4">
          <div>
            <MealSearchHistory />
          </div>
        </div>
      </main>
    </div>
  );
}

const MealSearchHistory = () => {
  const [data, setData] = useState<MealSearchHistoryProps | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    const fetchHistory = async () => {
      const response = await getMealSearchHistory();
      // console.log("Meal Search History:", history);

      if (response.status === "success" && response.history) {
        setData(response.history);
      } else {
        setError(response.detail || "Failed to fetch meal search history.");
      }
      setLoading(false);
    };
    fetchHistory();
  }, []);
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-3">
          <div className="w-full max-w-xl border rounded-lg p-6 space-y-4">
            <div className="space-y-2">
              <Skeleton className="h-8 w-3/4" />
              <Skeleton className="h-4 w-1/2" />
            </div>
            <div className="space-y-3">
              <Skeleton className="h-6 w-full" />
              <Skeleton className="h-6 w-full" />
              <Skeleton className="h-8 w-full" />
              <div className="space-y-2 pt-2">
                <Skeleton className="h-4 w-1/3" />
                <Skeleton className="h-5 w-full" />
                <Skeleton className="h-5 w-full" />
                <Skeleton className="h-5 w-full" />
              </div>
            </div>
            <Skeleton className="h-4 w-2/3" />
          </div>
          <Skeleton className="h-4 w-full" />
        </div>
      </div>
    );
  }
  if (error) {
    return <div className="text-red-500">Error: {error}</div>;
  } else {
    if (!data || data.length === 0) {
      return (
        <div>
          No meal search history found. Start searching for meals to see your
          history.
        </div>
      );
    }
    if (data.length > 0) {
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.map((item) => (
            <div key={item.search_id}>
              <MealInfoCard
                data={{
                  dish_name: item.dish_name,
                  servings: Math.round(
                    item.total_calories / item.calories_per_serving
                  ),
                  calories_per_serving: item.calories_per_serving,
                  total_calories: item.total_calories,
                  protein_per_serving: item.protein_per_serving,
                  fat_per_serving: item.fat_per_serving,
                  carbohydrates_per_serving: item.carbohydrates_per_serving,
                  source: item.source,
                  brand: "",
                  ingredients: "",
                }}
              />
              <p className="text-xs text-muted-foreground mt-2">
                Searched for: {item.search_keyword} on{" "}
                {new Date(item.timestamp).toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      );
    }
  }
};
