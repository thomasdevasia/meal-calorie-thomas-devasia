import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  isAuthenticated: boolean
  setAuthenticated: (value: boolean) => void
  logout: () => void
}

export const useAuthStore = create(
  persist<AuthState>(
    (set) => ({
      isAuthenticated: false,
      setAuthenticated: (value) => set({ isAuthenticated: value }),
      logout: () => set({ isAuthenticated: false }),
    }),
    { name: 'auth-storage' }
  )
)
