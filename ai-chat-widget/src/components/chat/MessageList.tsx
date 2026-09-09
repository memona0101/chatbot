import { MessageBubble } from "./MessageBubble";
import { QuickSuggestions } from "./QuickSuggestions";
import { SparkleIcon } from "../icons/ChatIcons";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

interface MessageListProps {
  messages: ChatMessage[];
  onSuggestionSelect?: (message: string) => void;
  suggestionsDisabled?: boolean;
}

export function MessageList({
  messages,
  onSuggestionSelect,
  suggestionsDisabled = false,
}: MessageListProps) {
  return (
    <div
      className="message-list"
      role="log"
      aria-live="polite"
      aria-label="Chat messages"
    >
      {messages.length === 0 ? (
        <div className="chat-welcome">
          <div className="chat-welcome-icon">
            <SparkleIcon className="chat-welcome-sparkle" />
          </div>
          <h1>What can I help you build?</h1>
          <p>
            Ask about custom software, AI agents, chatbots, pricing,
            or tell us about your project.
          </p>
          {onSuggestionSelect && (
            <QuickSuggestions
              onSelect={onSuggestionSelect}
              disabled={suggestionsDisabled}
            />
          )}
        </div>
      ) : (
        <div className="message-stream">
          {messages.map((message) => (
            <MessageBubble
              key={message.id}
              role={message.role}
              content={message.content}
              timestamp={message.timestamp}
            />
          ))}
        </div>
      )}
    </div>
  );
}
