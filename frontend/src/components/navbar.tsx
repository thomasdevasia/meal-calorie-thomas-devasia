"use client";
import Link from "next/link";
import { Sun, Moon } from "lucide-react";
import { useTheme } from "next-themes";

import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
} from "@/components/ui/navigation-menu";
import { Button } from "@/components/ui/button";
import { LogoutButton } from "@/components/logoutButton";
import { useAuthStore } from "@/stores/authStore";
import { useEffect, useState } from "react";

const navLinks = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/calories", label: "Calories" },
];

export function Navbar() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }
  return (
    <header className="flex items-center justify-between bg-background px-4 py-3 shadow-sm">
      <Link href="/" className="text-sm md:text-lg font-semibold">
        Meal Calorie
      </Link>

      <NavigationMenu>
        <NavigationMenuList className="gap-4">
          {navLinks.map((link) => (
            <NavigationMenuItem key={link.href}>
              <NavigationMenuLink asChild>
                <Link
                  href={link.href}
                  className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
                >
                  {link.label}
                </Link>
              </NavigationMenuLink>
            </NavigationMenuItem>
          ))}
        </NavigationMenuList>
      </NavigationMenu>

      <div className="flex items-center gap-2">
        <Button
          type="button"
          variant="ghost"
          size="icon"
          aria-label={
            theme === "dark" ? "Activate light mode" : "Activate dark mode"
          }
          aria-pressed={theme === "dark"}
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        >
          {theme === "dark" ? (
            <Sun className="h-5 w-5" aria-hidden="true" />
          ) : (
            <Moon className="h-5 w-5" aria-hidden="true" />
          )}
        </Button>

        {isAuthenticated ? (
          <LogoutButton />
        ) : (
          <Button asChild>
            <Link href="/login">Login</Link>
          </Button>
        )}
      </div>
    </header>
  );
}

export default Navbar;
