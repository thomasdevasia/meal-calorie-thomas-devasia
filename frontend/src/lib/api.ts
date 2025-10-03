"use server";
import { config } from "@/lib/config";
import { cookies } from "next/headers";


export async function authLogin(email: string, password: string) {
    try {
        const response = await fetch(`${config.backendUrl}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
            cache: "no-store",
        });
        if (response.status === 401) {
            const body = await response.json();
            return { success: false, error: body.detail, token: null };
        }
        if (response.status === 429) {
            return { success: false, error: "Rate limit exceeded. Please try again in 1 minute.", token: null };
        }
        if (!response.ok) {
            console.error("Login request failed with status:", response.status);
            console.error("Response text:", await response.text());
            return { success: false, error: "Login failed due to server error", token: null };
        }
        const body = await response.json();
        return { success: true, token: body.token, error: null };
    } catch (error) {
        console.error("Error during login:", error);
        return { success: false, error: "Login failed due to server error", token: null };
    }
}

export async function authSignup(first_name: string, last_name: string, email: string, password: string) {
    try {
        const response = await fetch(`${config.backendUrl}/auth/signup`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ first_name, last_name, email, password }),
            cache: "no-store",
        });
        if (response.status === 400) {
            const body = await response.json();
            return { success: false, error: body.detail, token: null };
        }
        if (response.status === 429) {
            return { success: false, error: "Rate limit exceeded. Please try again in 1 minute.", token: null };
        }
        if (!response.ok) {
            return {
                success: false,
                error: "Signup failed due to server error",
                token: null,
            };
        }
        const body = await response.json();
        if (!body.token) {
            return { success: false, error: "Signup failed", token: null };
        }
        return { success: true, token: body.token, error: null };
    } catch (error) {
        console.error("Error during signup:", error);
        return { success: false, error: "Signup failed due to server error", token: null };
    }
}

export async function getCalories(dish_name: string, servings: number) {
    try {
        const cookiesList = await cookies();
        const response = await fetch(`${config.backendUrl}/get-calories`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${cookiesList.get("meal_token")?.value}`,
            },
            body: JSON.stringify({ dish_name, servings }),
            cache: "no-store",
        });

        if (response.status === 429) {
            const error = await response.json();
            console.log("Rate limit exceeded", error);
            return { success: false, error: "Rate limit exceeded. Please try again in 1 minute.", data: null };
        }

        if (!response.ok) {
            const error = await response.json();
            console.log("Failed to fetch calories", error);
            console.log("Response status:", response.status);
            return { success: false, error: error.detail.detail, data: null };
        }

        const body = await response.json();
        return { success: true, error: null, data: body };
    } catch (error) {
        console.error("Error during fetching calories:", error);
        return { success: false, error: "Fetching calories failed due to server error", data: null };
    }
}


export async function getMealSearchHistory() {
    const cookiesList = await cookies();
    const token = cookiesList.get("meal_token")?.value;

    if (!token) {
        console.error("No authentication token found");
        return { status: "error", detail: "No authentication token found.", history: [] };
    }

    try {
        const response = await fetch(`${config.backendUrl}/search-history`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            cache: "no-store", // Ensure we always get the latest data
        });

        if (response.status === 429) {
            return { status: "error", detail: "Too many requests. Please try again in 1 minute.", history: [] };
        }
        if (response.status === 401) {
            const body = await response.json();
            console.error("Unauthorized access", body);
            return { status: "error", detail: "Unauthorized access. Please log in again.", history: [] };
        }
        if (!response.ok) {
            console.error("Failed to fetch meal search history", await response.text());
            return { status: "error", detail: "Failed to fetch meal search history.", history: [] };
        }

        const data = await response.json();
        // console.log("Fetched meal search history:", data);
        return { status: "success", history: data.history || [], detail: "success" };
    } catch (error) {
        console.error("Error fetching meal search history:", error);
        return { status: "error", detail: "Failed to fetch meal search history.", history: [] };
    }
}

// old code
// export async function getMealSearchHistory() {
//     const response = await fetch(`${process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'}/api/search-history`, {
//         method: "GET",
//         cache: "no-store",
//     });

//     if (!response.ok) {
//         console.error("Failed to fetch meal search history");
//         return [];
//     }

//     const data = await response.json();
//     console.log("Fetched meal search history:", data);
//     return data.history || [];
// }

// export async function performLogout() {
//     try {
//         const cookieStore = await cookies();
//         cookieStore.delete("meal_token");
//         return { success: true };
//     } catch (error) {
//         console.error("Error during logout:", error);
//         return { success: false, error: "Something went wrong while logging out. Please try again." };
//     }
// }