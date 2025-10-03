import MealForm from "@/components/MealForm";
import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "Calorie Lookup | Meal Calorie App",
  description:
    "Search and lookup calories for meals. Track your nutrition easily.",
  keywords: ["calorie", "meal", "nutrition", "lookup", "food", "health"],
};

export default function CaloriesPage() {
  return (
    <section className="flex flex-col gap-4">
      <MealForm />
    </section>
  );
}
