interface IconProps {
  className?: string;
}

export function LogoIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <rect x="3" y="3" width="18" height="18" rx="5" fill="url(#logoGrad)" />
      <path
        d="M8 12h8M12 8v8"
        stroke="white"
        strokeWidth="1.75"
        strokeLinecap="round"
      />
      <defs>
        <linearGradient id="logoGrad" x1="3" y1="3" x2="21" y2="21">
          <stop stopColor="#c084fc" />
          <stop offset="1" stopColor="#6366f1" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export function MenuIcon({ className }: IconProps) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      aria-hidden="true"
    >
      <path d="M4 7h16M4 12h16M4 17h16" />
    </svg>
  );
}

export function PlusIcon({ className }: IconProps) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      aria-hidden="true"
    >
      <path d="M12 5v14M5 12h14" />
    </svg>
  );
}

export function SendIcon({ className }: IconProps) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="m5 12 7-7 7 7M12 5v14" />
    </svg>
  );
}

export function UserIcon({ className }: IconProps) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="currentColor"
      aria-hidden="true"
    >
      <path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm0 2c-4.42 0-8 2.24-8 5v1h16v-1c0-2.76-3.58-5-8-5Z" />
    </svg>
  );
}

export function BotAvatarIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <rect x="3" y="4" width="18" height="14" rx="4" fill="url(#botGrad)" />
      <circle cx="9" cy="11" r="1.5" fill="#0c0c0e" />
      <circle cx="15" cy="11" r="1.5" fill="#0c0c0e" />
      <path d="M9 15h6" stroke="#0c0c0e" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M12 2v2" stroke="url(#botGrad)" strokeWidth="2" strokeLinecap="round" />
      <defs>
        <linearGradient id="botGrad" x1="3" y1="4" x2="21" y2="18">
          <stop stopColor="#c084fc" />
          <stop offset="1" stopColor="#6366f1" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export function SparkleIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M12 2l1.2 3.6L17 7l-3.6 1.2L12 12l-1.2-3.8L7 7l3.8-1.4L12 2z" />
    </svg>
  );
}
