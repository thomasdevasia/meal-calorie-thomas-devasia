"use client";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";
import { loginAction } from "@/actions/loginServerAction";
import type { LoginState } from "@/types/auth";
import { useActionState, useEffect } from "react";
import { cn } from "@/lib/utils";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/authStore";
import { LoaderCircle } from "lucide-react";

const initialState: LoginState = {
  success: false,
  error: null,
};

export default function LoginCard() {
  const router = useRouter();
  const { setAuthenticated } = useAuthStore();
  const [state, formAction, isPending] = useActionState<LoginState, FormData>(
    loginAction,
    initialState
  );
  useEffect(() => {
    if (state.success) {
      console.log("Login successful, redirecting to dashboard...");
      setAuthenticated(true);
      router.push("/dashboard");
    }
  }, [router, setAuthenticated, state.success]);
  return (
    <Card className="w-full max-w-sm">
      <form action={formAction}>
        <CardHeader>
          <CardTitle>Login to your account</CardTitle>
          <CardDescription>
            Enter your email below to login to your account
          </CardDescription>
          <CardAction>
            <Button variant="link" className="cursor-pointer">
              <Link href="/signup">Sign Up</Link>
            </Button>
          </CardAction>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col gap-6">
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="m@example.com"
                required
                className={cn(
                  state.error?.fieldErrors.email?.length && "border-destructive"
                )}
                name="email"
              />
              {state.error?.fieldErrors.email?.map((message, index) => (
                <p key={index} className="text-destructive">
                  {message}
                </p>
              ))}
            </div>
            <div className="grid gap-2">
              <div className="flex items-center">
                <Label htmlFor="password">Password</Label>
              </div>
              <Input
                id="password"
                type="password"
                required
                className={cn(
                  state.error?.fieldErrors.password?.length &&
                    "border-destructive"
                )}
                name="password"
              />
              {state.error?.fieldErrors.password?.map((message, index) => (
                <p key={index} className="text-destructive">
                  {message}
                </p>
              ))}
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex-col gap-2">
          {state.error?.formErrors.length ? (
            <p className="text-sm text-destructive text-center mt-2">
              {state.error.formErrors.join(" ")}
            </p>
          ) : null}
          <Button
            type="submit"
            className="w-full cursor-pointer mt-2"
            disabled={isPending}
          >
            {isPending ? (
              <>
                <span>Logging in...</span>
                <LoaderCircle className="mr-2 h-4 w-4 animate-spin" />
              </>
            ) : (
              "Login"
            )}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}
