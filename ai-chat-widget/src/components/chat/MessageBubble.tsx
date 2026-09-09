import { BotAvatarIcon, UserIcon } from "../icons/ChatIcons";

interface MessageBubbleProps {
  role: "user" | "assistant";
  content: string;
  timestamp?: Date;
}

export function MessageBubble({
  role,
  content,
  timestamp,
}: MessageBubbleProps) {
  const isAssistant = role === "assistant";

  return (
    <article
      className={`message-row message-row-${role}`}
      aria-label={`${role} message`}
    >
      <div className="message-row-inner">
        <div className={`message-avatar message-avatar-${role}`} aria-hidden="true">
          {isAssistant ? (
            <BotAvatarIcon className="message-avatar-icon" />
          ) : (
            <UserIcon className="message-avatar-icon" />
          )}
        </div>

        <div className="message-content">
          <div className="message-role">{isAssistant ? "MoinSystems AI" : "You"}</div>
          <div className="message-text">{content}</div>
          {timestamp && (
            <time dateTime={timestamp.toISOString()} className="message-time">
              {timestamp.toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </time>
          )}
        </div>
      </div>
    </article>
  );
}
