"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/authStore";

export default function Home() {
  const router = useRouter();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  useEffect(() => {
    if (isAuthenticated) {
      router.replace("/dashboard");
    } else {
      router.replace("/login");
    }
  }, [isAuthenticated, router]);

  return (
    <main className="flex items-center justify-center bg-background">
      <div className="flex flex-col items-center gap-3 text-center">
        <span
          className="h-8 w-8 animate-spin rounded-full border-2 border-muted border-t-primary"
          aria-hidden="true"
        />
        <p className="text-sm text-muted-foreground">
          Redirecting you to the right place, please hang tight.
        </p>
      </div>
    </main>
  );
}
