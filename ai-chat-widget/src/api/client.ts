import type {
  ChatRequest,
  ChatResponse,
  CreateSessionResponse,
  LeadCaptureRequest,
  LeadCaptureResponse,
} from "../types/api";

const rawBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "";
const API_BASE_URL = rawBaseUrl.endsWith("/")
  ? rawBaseUrl.slice(0, -1)
  : rawBaseUrl;

class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });
  } catch {
    throw new ApiError(
      "Unable to connect to the server. Please check your connection.",
      0,
    );
  }

  let data: unknown = null;

  try {
    data = await response.json();
  } catch {
    // Response may not contain JSON.
  }

  if (!response.ok) {
    if (
      typeof data === "object" &&
      data !== null &&
      "detail" in data
    ) {
      const errorData = data as {
        detail?: Array<{ msg?: string }>;
      };

      const message =
        errorData.detail?.[0]?.msg ??
        "Something went wrong. Please try again.";

      throw new ApiError(message, response.status);
    }

    throw new ApiError(
      "Something went wrong. Please try again.",
      response.status,
    );
  }

  return data as T;
}

export async function createSession(): Promise<CreateSessionResponse> {
  return request<CreateSessionResponse>("/api/v1/sessions", {
    method: "POST",
  });
}

export async function sendMessage(
  payload: ChatRequest,
): Promise<ChatResponse> {
  return request<ChatResponse>("/api/v1/chat", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function captureLead(
  payload: LeadCaptureRequest,
): Promise<LeadCaptureResponse> {
  return request<LeadCaptureResponse>("/api/v1/lead-capture", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}