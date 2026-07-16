import { create } from "zustand";

export interface AppNotification {
  id: string;
  title: string;
  description?: string;
  read: boolean;
  createdAt: string;
}

interface NotificationState {
  notifications: AppNotification[];
  unreadCount: number;
  push: (notification: Omit<AppNotification, "id" | "read" | "createdAt">) => void;
  markAllRead: () => void;
}

export const useNotificationStore = create<NotificationState>((set, get) => ({
  notifications: [],
  unreadCount: 0,
  push: (notification) =>
    set({
      notifications: [
        {
          ...notification,
          id: crypto.randomUUID(),
          read: false,
          createdAt: new Date().toISOString(),
        },
        ...get().notifications,
      ].slice(0, 50),
      unreadCount: get().unreadCount + 1,
    }),
  markAllRead: () =>
    set({
      notifications: get().notifications.map((n) => ({ ...n, read: true })),
      unreadCount: 0,
    }),
}));
