"use client";

import { useActionState, useEffect } from "react";
import { LoaderCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { logoutAction } from "@/actions/logoutAction";
import type { LogoutState } from "@/types/auth";
import { useAuthStore } from "@/stores/authStore";

const initialState: LogoutState = { success: false };

export function LogoutButton() {
  const logout = useAuthStore((state) => state.logout);
  const [state, formAction, isPending] = useActionState(
    logoutAction,
    initialState
  );

  useEffect(() => {
    if (state.success) {
      logout();
    }
  }, [state.success, logout]);

  return (
    <form action={formAction} className="flex items-center">
      <SubmitButton pending={isPending} />
    </form>
  );
}

type SubmitButtonProps = {
  pending: boolean;
};

function SubmitButton({ pending }: SubmitButtonProps) {
  return (
    <Button type="submit" variant="secondary" disabled={pending}>
      Logout
      {pending ? (
        <>
          <LoaderCircle className="mr-2 h-4 w-4 animate-spin" />
        </>
      ) : (
        ""
      )}
    </Button>
  );
}

export default LogoutButton;
