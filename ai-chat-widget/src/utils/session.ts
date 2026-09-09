const SESSION_STORAGE_KEY = "ai_chat_session_token";

export function getStoredSessionToken(): string | null {
  return sessionStorage.getItem(SESSION_STORAGE_KEY);
}

export function storeSessionToken(token: string): void {
  sessionStorage.setItem(SESSION_STORAGE_KEY, token);
}

export function clearSessionToken(): void {
  sessionStorage.removeItem(SESSION_STORAGE_KEY);
}