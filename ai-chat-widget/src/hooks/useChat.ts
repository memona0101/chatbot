import { useCallback, useEffect, useState } from "react";
import {
  captureLead,
  createSession,
  sendMessage,
} from "../api/client";
import {
  clearSessionToken,
  getStoredSessionToken,
  storeSessionToken,
} from "../utils/session";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

interface UseChatReturn {
  messages: ChatMessage[];
  sessionToken: string | null;
  leadState: string | null;
  isLoading: boolean;
  error: string | null;
  initializeSession: () => Promise<void>;
  sendChatMessage: (message: string) => Promise<void>;
  submitLeadField: (
  field: string,
  value: string,
) => Promise<boolean>;
  retryLastMessage: () => Promise<void>;
  retryConnection: () => Promise<void>;
  startNewChat: () => Promise<void>;
  clearError: () => void;
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sessionToken, setSessionToken] = useState<string | null>(null);
  const [leadState, setLeadState] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUserMessage, setLastUserMessage] = useState<string | null>(null);

  const initializeSession = useCallback(async () => {
    const existingToken = getStoredSessionToken();

    if (existingToken) {
      setSessionToken(existingToken);
      return;
    }

    try {
      setIsLoading(true);
      setError(null);

      const response = await createSession();

      storeSessionToken(response.session_token);
      setSessionToken(response.session_token);
      setLeadState(response.lead_state);
    } catch (err) {
      const message =
        err instanceof Error &&
        err.message.includes("Unable to connect")
          ? "Cannot reach the server. Make sure the backend is running on port 8000."
          : "We couldn't start the chat. Please try again.";

      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void initializeSession();
  }, [initializeSession]);

  const sendChatMessage = useCallback(
    async (message: string) => {
      const trimmedMessage = message.trim();

      if (!trimmedMessage || !sessionToken || isLoading) {
        return;
      }

      const userMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "user",
        content: trimmedMessage,
        timestamp: new Date(),
      };

      setMessages((current) => [...current, userMessage]);
      setLastUserMessage(trimmedMessage);
      setIsLoading(true);
      setError(null);

      try {
        const response = await sendMessage({
          session_token: sessionToken,
          message: trimmedMessage,
        });

        const assistantMessage: ChatMessage = {
          id: crypto.randomUUID(),
          role: "assistant",
          content: response.message,
          timestamp: new Date(),
        };

        setMessages((current) => [...current, assistantMessage]);
        setLeadState(response.lead_state);
      } catch {
        setError(
          "We couldn't send your message. Please try again.",
        );
      } finally {
        setIsLoading(false);
      }
    },
    [sessionToken, isLoading],
  );

  const submitLeadField = useCallback(
    async (field: string, value: string) => {
      if (!sessionToken || isLoading) {
  return false;
}

      setIsLoading(true);
      setError(null);

      try {
        const response = await captureLead({
          session_token: sessionToken,
          field,
          value,
        });

        if (!response.success) {
          setError(response.message);
          return false;
        }

        setLeadState(response.lead_state);

        if (response.message) {
          const assistantMessage: ChatMessage = {
            id: crypto.randomUUID(),
            role: "assistant",
            content: response.message,
            timestamp: new Date(),
          };
          setMessages((current) => [...current, assistantMessage]);
        }

        return true;
      } catch {
        setError(
          "We couldn't save that information. Please try again.",
        );
        return false;
      } finally {
        setIsLoading(false);
      }
    },
    [sessionToken, isLoading],
  );

  const retryLastMessage = useCallback(async () => {
    if (!lastUserMessage || isLoading) {
      return;
    }

    await sendChatMessage(lastUserMessage);
  }, [lastUserMessage, isLoading, sendChatMessage]);

  const retryConnection = useCallback(async () => {
    if (isLoading) {
      return;
    }

    setError(null);

    if (lastUserMessage && sessionToken) {
      await sendChatMessage(lastUserMessage);
      return;
    }

    if (!sessionToken) {
      await initializeSession();
    }
  }, [
    isLoading,
    lastUserMessage,
    sessionToken,
    sendChatMessage,
    initializeSession,
  ]);

  const startNewChat = useCallback(async () => {
    clearSessionToken();
    setMessages([]);
    setSessionToken(null);
    setLeadState(null);
    setLastUserMessage(null);
    setError(null);

    try {
      setIsLoading(true);
      const response = await createSession();
      storeSessionToken(response.session_token);
      setSessionToken(response.session_token);
      setLeadState(response.lead_state);
    } catch {
      setError("We couldn't start a new chat. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    messages,
    sessionToken,
    leadState,
    isLoading,
    error,
    initializeSession,
    sendChatMessage,
    submitLeadField,
    retryLastMessage,
    retryConnection,
    startNewChat,
    clearError,
  };
}