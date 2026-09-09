import { PlusIcon, LogoIcon } from "../icons/ChatIcons";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  onNewChat: () => void;
}

export function Sidebar({ isOpen, onClose, onNewChat }: SidebarProps) {
  return (
    <>
      <div
        className={`sidebar-backdrop${isOpen ? " sidebar-backdrop--visible" : ""}`}
        onClick={onClose}
        aria-hidden="true"
      />

      <aside
        className={`sidebar${isOpen ? " sidebar--open" : ""}`}
        aria-label="Chat navigation"
      >
        <div className="sidebar-top">
          <div className="sidebar-brand">
            <LogoIcon className="sidebar-brand-icon" />
            <span>MoinSystems</span>
          </div>

          <button
            type="button"
            className="sidebar-new-chat"
            onClick={() => {
              onNewChat();
              onClose();
            }}
          >
            <PlusIcon className="sidebar-new-chat-icon" />
            New chat
          </button>
        </div>

        <div className="sidebar-footer">
          <p>AI Assistant for software &amp; automation</p>
        </div>
      </aside>
    </>
  );
}
