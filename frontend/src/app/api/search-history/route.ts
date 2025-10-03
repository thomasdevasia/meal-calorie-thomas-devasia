import { config } from "@/lib/config";
import { cookies } from "next/headers";
import { NextResponse } from "next/server";

export async function GET() {
    try {
        const cookiesList = await cookies();
        const token = cookiesList.get("meal_token")?.value;

        if (!token) {
            return NextResponse.json(
                { error: "Unauthorized" },
                { status: 401 }
            );
        }

        const response = await fetch(`${config.backendUrl}/search-history`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            return NextResponse.json(
                { error: "Failed to fetch meal search history", details: errorData },
                { status: response.status }
            );
        }

        const data = await response.json();
        console.log("Meal search history data:", data);
        return NextResponse.json(data);
    } catch (error) {
        console.error("Error fetching meal search history:", error);
        return NextResponse.json(
            { error: "Internal server error" },
            { status: 500 }
        );
    }
}
