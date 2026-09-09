import { useRef, type FormEvent, type KeyboardEvent } from "react";
import { SendIcon } from "../icons/ChatIcons";

interface ChatComposerProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export function ChatComposer({
  onSend,
  disabled = false,
  placeholder = "Message MoinSystems AI...",
}: ChatComposerProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  function submitMessage() {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const trimmedMessage = textarea.value.trim();
    if (!trimmedMessage || disabled) return;

    onSend(trimmedMessage);
    textarea.value = "";
    textarea.style.height = "auto";
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    submitMessage();
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      submitMessage();
    }
  }

  function handleInput() {
    const textarea = textareaRef.current;
    if (!textarea) return;

    textarea.style.height = "auto";
    textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
  }

  return (
    <form className="chat-composer" onSubmit={handleSubmit}>
      <label htmlFor="chat-message" className="sr-only">
        Message
      </label>

      <div className="chat-composer-border">
        <div className="chat-composer-box">
          <textarea
            ref={textareaRef}
            id="chat-message"
            name="chat-message"
            rows={1}
            placeholder={placeholder}
            disabled={disabled}
            autoComplete="off"
            onKeyDown={handleKeyDown}
            onInput={handleInput}
          />

          <button
            type="submit"
            className="chat-composer-send"
            disabled={disabled}
            aria-label="Send message"
          >
            <SendIcon className="chat-composer-send-icon" />
          </button>
        </div>
      </div>
    </form>
  );
}
