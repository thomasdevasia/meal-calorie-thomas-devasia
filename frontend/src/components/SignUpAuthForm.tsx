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
import { signUpAction } from "@/actions/signUpServerAction";
import type { SignUpState } from "@/types/auth";
import { useActionState, useEffect } from "react";
import { cn } from "@/lib/utils";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/authStore";
import { LoaderCircle } from "lucide-react";

const initialState: SignUpState = {};

export default function SignUpCard() {
  const router = useRouter();
  const { setAuthenticated } = useAuthStore();

  const [state, formAction, isPending] = useActionState<SignUpState, FormData>(
    signUpAction,
    initialState
  );
  useEffect(() => {
    if (state.success) {
      console.log("Signup successful, redirecting to dashboard...");
      setAuthenticated(true);
      router.push("/dashboard");
    }
  }, [router, setAuthenticated, state.success]);
  return (
    <Card className="w-full max-w-sm">
      <form action={formAction}>
        <CardHeader>
          <CardTitle>Signup for an account</CardTitle>
          <CardDescription>
            Enter your details below to create a new account
          </CardDescription>
          <CardAction>
            <Button variant="link" className="cursor-pointer">
              <Link href="/login">Login</Link>
            </Button>
          </CardAction>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col gap-6 mt-2">
            <div className="grid gap-2">
              <Label htmlFor="first-name">First Name</Label>
              <Input
                id="first-name"
                name="first-name"
                type="text"
                placeholder="John"
                required
                className={cn(
                  state.error?.fieldErrors.firstName?.length &&
                    "border-destructive"
                )}
              />
              {state.error?.fieldErrors.firstName?.map((message, index) => (
                <p key={message + index} className="text-sm text-destructive">
                  {message}
                </p>
              ))}
            </div>
            <div className="grid gap-2">
              <Label htmlFor="last-name">Last Name</Label>
              <Input
                id="last-name"
                name="last-name"
                type="text"
                placeholder="Doe"
                required
                className={cn(
                  state.error?.fieldErrors.lastName?.length &&
                    "border-destructive"
                )}
              />
              {state.error?.fieldErrors.lastName?.map((message, index) => (
                <p key={message + index} className="text-sm text-destructive">
                  {message}
                </p>
              ))}
            </div>
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="m@example.com"
                required
                className={cn(
                  state.error?.fieldErrors.email?.length && "border-destructive"
                )}
              />
              {state.error?.fieldErrors.email?.map((message, index) => (
                <p key={message + index} className="text-sm text-destructive">
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
                name="password"
                type="password"
                required
                className={cn(
                  state.error?.fieldErrors.password?.length &&
                    "border-destructive"
                )}
              />
              {state.error?.fieldErrors.password?.map((message, index) => (
                <p key={message + index} className="text-sm text-destructive">
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
                <span>Signing Up...</span>
                <LoaderCircle className="mr-2 h-4 w-4 animate-spin" />
              </>
            ) : (
              "Sign Up"
            )}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}
