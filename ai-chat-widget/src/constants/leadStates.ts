export const LEAD_STATES = {
  IDLE: "idle",
  COLLECTING_NAME: "collecting_name",
  COLLECTING_EMAIL: "collecting_email",
  COLLECTING_PHONE: "collecting_phone",
  COMPLETE: "complete",
} as const;

export type LeadState = (typeof LEAD_STATES)[keyof typeof LEAD_STATES];

export function isCollectingLead(leadState: string | null): boolean {
  if (!leadState) return false;
  return (
    leadState !== LEAD_STATES.IDLE &&
    leadState !== LEAD_STATES.COMPLETE
  );
}

export function mapLeadFieldForApi(field: string): string {
  const normalized = field
    .toLowerCase()
    .replace(/^awaiting[_-]?/, "")
    .replace(/^collecting[_-]?/, "")
    .replace(/^missing[_-]?/, "");

  const mapping: Record<string, string> = {
    name: "full_name",
    phone: "contact_number",
  };

  return mapping[normalized] ?? normalized;
}

export function getLeadStepIndex(leadState: string): number {
  switch (leadState) {
    case LEAD_STATES.COLLECTING_NAME:
      return 0;
    case LEAD_STATES.COLLECTING_EMAIL:
      return 1;
    case LEAD_STATES.COLLECTING_PHONE:
      return 2;
    case LEAD_STATES.COMPLETE:
      return 3;
    default:
      return -1;
  }
}
