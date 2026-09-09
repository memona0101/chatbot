import { useEffect, useRef, useState } from "react";
import { useChat } from "../../hooks/useChat";
import { isCollectingLead } from "../../constants/leadStates";
import { ChatComposer } from "./ChatComposer";
import { LeadCaptureForm } from "./LeadCaptureForm";
import { LeadProgress } from "./LeadProgress";
import { MessageList } from "./MessageList";
import { Sidebar } from "./Sidebar";
import { TypingIndicator } from "./TypingIndicator";
import { MenuIcon } from "../icons/ChatIcons";

export function ChatApp() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const chatBodyRef = useRef<HTMLDivElement>(null);

  const {
    messages,
    leadState,
    isLoading,
    error,
    sendChatMessage,
    submitLeadField,
    retryConnection,
    startNewChat,
  } = useChat();

  const collectingLead = isCollectingLead(leadState);
  const hasMessages = messages.length > 0;

  useEffect(() => {
    const chatBody = chatBodyRef.current;
    if (!chatBody || !hasMessages) return;

    chatBody.scrollTo({
      top: chatBody.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, isLoading, hasMessages]);

  function handleSend(message: string) {
    void sendChatMessage(message);
  }

  return (
    <div className="chat-app">
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onNewChat={() => void startNewChat()}
      />

      <main className="chat-main">
        <header className="chat-topbar">
          <button
            type="button"
            className="chat-topbar-menu"
            onClick={() => setSidebarOpen(true)}
            aria-label="Open menu"
          >
            <MenuIcon className="chat-topbar-menu-icon" />
          </button>
          <span className="chat-topbar-title">MoinSystems AI</span>
        </header>

        <div
          ref={chatBodyRef}
          className={`chat-body${hasMessages ? " chat-body--active" : ""}`}
        >
          <MessageList
            messages={messages}
            onSuggestionSelect={handleSend}
            suggestionsDisabled={isLoading}
          />

          {isLoading && hasMessages && <TypingIndicator />}
        </div>

        <div className="chat-footer">
          {collectingLead && leadState && (
            <div className="chat-footer-lead">
              <LeadProgress leadState={leadState} />
              <LeadCaptureForm
                leadState={leadState}
                isLoading={isLoading}
                onSubmit={submitLeadField}
              />
            </div>
          )}

          {error && (
            <div className="chat-error" role="alert">
              <span>{error}</span>
              <button type="button" onClick={() => void retryConnection()}>
                Retry
              </button>
            </div>
          )}

          <ChatComposer
            onSend={handleSend}
            disabled={isLoading}
            placeholder={
              collectingLead
                ? "Or type your answer here..."
                : "Message MoinSystems AI..."
            }
          />

          <p className="chat-disclaimer">
            AI can make mistakes. Verify important information.
          </p>
        </div>
      </main>
    </div>
  );
}
