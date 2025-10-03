import { z } from "zod";

const envSchema = z.object({
    NEXT_PUBLIC_BACKEND_URL: z.url(),
    NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
});

const parsedEnv = envSchema.safeParse(process.env);

if (!parsedEnv.success) {
    console.error("Invalid environment variables", z.flattenError(parsedEnv.error));
    console.log(process.env)

    throw new Error("Invalid environment variables");
}

export const config = {
    backendUrl: parsedEnv.data.NEXT_PUBLIC_BACKEND_URL,
    nodeEnv: parsedEnv.data.NODE_ENV,
};
