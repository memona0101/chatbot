import { useState } from "react";
import type { FormEvent } from "react";
import { mapLeadFieldForApi } from "../../constants/leadStates";

interface LeadCaptureFormProps {
  leadState: string;
  isLoading: boolean;
  onSubmit: (
    field: string,
    value: string,
  ) => Promise<boolean>;
}

const fieldConfig: Record<
  string,
  {
    label: string;
    placeholder: string;
    type: string;
  }
> = {
  full_name: {
    label: "Full name",
    placeholder: "Enter your full name",
    type: "text",
  },
  email: {
    label: "Email address",
    placeholder: "you@example.com",
    type: "email",
  },
  contact_number: {
    label: "Contact number",
    placeholder: "+92 300 1234567",
    type: "tel",
  },
};

function normalizeLeadState(leadState: string): string {
  return leadState
    .toLowerCase()
    .replace(/^awaiting[_-]?/, "")
    .replace(/^collecting[_-]?/, "")
    .replace(/^missing[_-]?/, "");
}

function validateField(
  field: string,
  value: string,
): string | null {
  const trimmedValue = value.trim();
  const apiField = mapLeadFieldForApi(field);

  if (!trimmedValue) {
    return "This field is required.";
  }

  if (apiField === "email") {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(trimmedValue)) {
      return "Please enter a valid email address.";
    }
  }

  if (apiField === "contact_number") {
    const phonePattern = /^[+]?[0-9\s()-]{7,20}$/;
    const digitCount = (trimmedValue.match(/\d/g) ?? []).length;

    if (!phonePattern.test(trimmedValue) || digitCount < 7) {
      return "Please enter a valid contact number.";
    }
  }

  return null;
}

export function LeadCaptureForm({
  leadState,
  isLoading,
  onSubmit,
}: LeadCaptureFormProps) {
  const [value, setValue] = useState("");
  const [validationError, setValidationError] =
    useState<string | null>(null);

  const normalizedField = normalizeLeadState(leadState);
  const apiField = mapLeadFieldForApi(normalizedField);

  const config = fieldConfig[apiField] ?? {
    label: "Information",
    placeholder: "Enter your information",
    type: "text",
  };

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const error = validateField(normalizedField, value);

    if (error) {
      setValidationError(error);
      return;
    }

    setValidationError(null);

    const success = await onSubmit(apiField, value.trim());

    if (success) {
      setValue("");
    }
  }

  return (
    <form className="lead-capture-form" onSubmit={handleSubmit}>
      <div className="lead-capture-title">
        <strong>{config.label}</strong>
        <span>Required</span>
      </div>

      <label htmlFor="lead-field" className="sr-only">
        {config.label}
      </label>

      <input
        id="lead-field"
        type={config.type}
        value={value}
        onChange={(event) => {
          setValue(event.target.value);
          setValidationError(null);
        }}
        placeholder={config.placeholder}
        disabled={isLoading}
        autoComplete="off"
        aria-invalid={Boolean(validationError)}
        aria-describedby={
          validationError ? "lead-field-error" : undefined
        }
      />

      {validationError && (
        <div
          id="lead-field-error"
          className="lead-field-error"
          role="alert"
        >
          {validationError}
        </div>
      )}

      <button
        type="submit"
        disabled={isLoading || !value.trim()}
      >
        {isLoading ? "Saving..." : "Continue"}
      </button>
    </form>
  );
}
