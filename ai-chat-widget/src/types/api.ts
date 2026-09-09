export interface CreateSessionResponse {
  session_token: string;
  lead_state: string;
}

export interface ChatRequest {
  session_token: string;
  message: string;
}

export interface ChatResponse {
  session_token: string;
  message: string;
  lead_state: string;
}

export interface LeadCaptureRequest {
  session_token: string;
  field: string;
  value: string;
}

export interface LeadCaptureResponse {
  success: boolean;
  message: string;
  lead_state: string;
}

export interface ApiValidationError {
  loc: Array<string | number>;
  msg: string;
  type: string;
}

export interface ApiErrorResponse {
  detail?: ApiValidationError[];
}