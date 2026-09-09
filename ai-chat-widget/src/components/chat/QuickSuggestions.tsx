const SUGGESTIONS = [
  {
    title: "Explore services",
    prompt: "What services do you offer?",
  },
  {
    title: "AI chatbots",
    prompt: "Tell me about AI chatbots",
  },
  {
    title: "Project pricing",
    prompt: "How much does a project cost?",
  },
  {
    title: "Start a project",
    prompt: "I want to start a project",
  },
];

interface QuickSuggestionsProps {
  onSelect: (message: string) => void;
  disabled?: boolean;
}

export function QuickSuggestions({
  onSelect,
  disabled = false,
}: QuickSuggestionsProps) {
  return (
    <div className="quick-suggestions">
      {SUGGESTIONS.map((suggestion) => (
        <button
          key={suggestion.prompt}
          type="button"
          className="quick-suggestion-card"
          disabled={disabled}
          onClick={() => onSelect(suggestion.prompt)}
        >
          <span className="quick-suggestion-title">{suggestion.title}</span>
          <span className="quick-suggestion-prompt">{suggestion.prompt}</span>
        </button>
      ))}
    </div>
  );
}
