"use server";

import { z } from "zod";
import { cookies } from "next/headers";
import type { SignUpState } from "@/types/auth";
import { authSignup } from "@/lib/api";
import { config } from "@/lib/config";


export async function signUpAction(
  _prevState: SignUpState,
  formData: FormData,
): Promise<SignUpState> {
  const first_name = formData.get("first-name") as string;
  const last_name = formData.get("last-name") as string;
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;

  const signUpSchema = z.object({
    first_name: z.string().min(2, "First name is required"),
    last_name: z.string().min(2, "last name is required"),
    email: z.email({ message: "Invalid email address" }),
    password: z.string().min(6, "Password must be at least 6 characters"),
  });

  const result = signUpSchema.safeParse({ first_name, last_name, email, password });
  // console.log("Validation result:", result);
  // console.log("Form data received:", { first_name, last_name, email, password });

  if (!result.success) {
    // console.error("Validation failed", z.flattenError(result.error));
    return { success: false, error: z.flattenError(result.error) };
  }

  const response = await authSignup(first_name, last_name, email, password);
  if (!response.success) {
    return { success: false, error: { formErrors: [response.error || "Signup failed"], fieldErrors: {} } };
  }

  const cookieStore = await cookies();
  const isProduction = config.nodeEnv === "production";
  cookieStore.set({
    name: "meal_token",
    value: response.token,
    httpOnly: true,
    secure: isProduction,
  });

  return { success: true };
}
