import { BotAvatarIcon } from "../icons/ChatIcons";

export function TypingIndicator() {
  return (
    <div className="typing-indicator-row">
      <div className="message-row-inner">
        <div className="message-avatar message-avatar-assistant" aria-hidden="true">
          <BotAvatarIcon className="message-avatar-icon" />
        </div>
        <div
          className="typing-indicator"
          role="status"
          aria-live="polite"
          aria-label="Assistant is typing"
        >
          <span className="typing-dot" />
          <span className="typing-dot" />
          <span className="typing-dot" />
          <span className="sr-only">Assistant is typing...</span>
        </div>
      </div>
    </div>
  );
}
