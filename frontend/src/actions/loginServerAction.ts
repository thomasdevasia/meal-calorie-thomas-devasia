"use server";
import { z } from "zod";
import { cookies } from "next/headers";
import { type LoginState } from "@/types/auth";
import { authLogin } from "@/lib/api";
import { config } from "@/lib/config";

export async function loginAction(
  _prevState: LoginState,
  formData: FormData,
) {
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;

  const loginSchema = z.object({
    email: z.email({ message: "Invalid email address" }),
    password: z.string().min(6, "Password must be at least 6 characters"),
  });

  const result = loginSchema.safeParse({ email, password });
  // console.log("Validation result:", result);
  // console.log("Form data received:", { email, password });
  if (!result.success) {
    return { success: false, error: z.flattenError(result.error) };
  }

  const response = await authLogin(email, password);
  if (!response.success) {
    return { success: false, error: { formErrors: [response.error || "Login failed"], fieldErrors: {} } };
  }

  const cookieStore = await cookies();
  const isProduction = config.nodeEnv === "production";
  cookieStore.set({
    name: "meal_token",
    value: response.token,
    httpOnly: true,
    secure: isProduction,
  });

  return { success: true, error: null };
}