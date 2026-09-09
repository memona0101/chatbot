import { getLeadStepIndex } from "../../constants/leadStates";

const STEPS = ["Name", "Email", "Phone"];

export function LeadProgress({ leadState }: { leadState: string }) {
  const currentStep = getLeadStepIndex(leadState);

  if (currentStep < 0) return null;

  return (
    <div className="lead-progress" aria-label="Lead capture progress">
      <div className="lead-progress-track">
        {STEPS.map((step, index) => {
          const isComplete = index < currentStep;
          const isActive = index === currentStep;

          return (
            <div
              key={step}
              className={`lead-progress-step${
                isComplete ? " lead-progress-step--done" : ""
              }${isActive ? " lead-progress-step--active" : ""}`}
            >
              <div className="lead-progress-dot">
                {isComplete ? (
                  <svg viewBox="0 0 12 12" fill="none" aria-hidden="true">
                    <path
                      d="M2 6l3 3 5-5"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                ) : (
                  <span>{index + 1}</span>
                )}
              </div>
              <span className="lead-progress-label">{step}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
