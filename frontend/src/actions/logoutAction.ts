"use server";

import { cookies } from "next/headers";
import { type LogoutState } from "@/types/auth";

export async function logoutAction(
    prevState: LogoutState,
    formData: FormData,
): Promise<LogoutState> {
    // add a small delay to simulate network latency
    // await new Promise((resolve) => setTimeout(resolve, 500));
    try {
        void prevState;
        void formData;
        const cookieStore = await cookies();
        cookieStore.delete("meal_token");

        return { success: true };
    } catch (error) {
        void error;
        return {
            success: false,
            error: "Something went wrong while logging out. Please try again.",
        };
    }
}
