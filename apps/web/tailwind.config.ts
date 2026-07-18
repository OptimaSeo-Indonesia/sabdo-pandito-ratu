import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: ["./src/**/*.{ts,tsx}", "./index.html"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      colors: {
        border: "hsl(var(--border) / <alpha-value>)",
        input: "hsl(var(--input) / <alpha-value>)",
        ring: "hsl(var(--ring) / <alpha-value>)",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
        },
        success: {
          DEFAULT: "hsl(var(--success))",
        },
        warning: {
          DEFAULT: "hsl(var(--warning))",
        },
        danger: {
          DEFAULT: "hsl(var(--danger))",
        },
        card: "hsl(var(--card))",
        sidebar: "hsl(var(--sidebar))",
        elevated: "hsl(var(--elevated-card))",
        panel: "hsl(var(--panel))",
        "input-bg": "hsl(var(--input-bg))",
        "button-secondary": "hsl(var(--button-secondary))",
        "active-nav": "hsl(var(--active-nav))",
        "progress-track": "hsl(var(--progress-track))",
        "topbar-chip": "hsl(var(--topbar-chip))",
        destructive: {
          DEFAULT: "hsl(var(--danger))",
        },
      },
      borderRadius: {
        DEFAULT: "16px",
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
        xl: "calc(var(--radius) + 4px)",
        "2xl": "calc(var(--radius) + 8px)",
      },
      boxShadow: {
        card: "0 12px 32px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(108, 99, 255, 0.14)",
        "card-sm": "0 8px 24px rgba(0, 0, 0, 0.25)",
        nav: "0 0 0 1px rgba(108, 99, 255, 0.55), 0 8px 24px rgba(108, 99, 255, 0.18)",
        glow: "0 0 12px rgba(108, 99, 255, 0.5)",
        "glow-sm": "0 2px 8px rgba(108, 99, 255, 0.4)",
      },
      backgroundImage: {
        "grad-brand": "linear-gradient(90deg, #4A7BFF 0%, #7A52FF 48%, #FF58B8 100%)",
        "grad-primary-btn": "linear-gradient(90deg, #A44BFF 0%, #6C63FF 100%)",
        "grad-active-nav": "linear-gradient(180deg, rgba(108,99,255,0.2) 0%, rgba(108,99,255,0.1) 100%)",
        "grad-sage": "linear-gradient(90deg, #6C63FF 0%, #A44BFF 100%)",
        "grad-strategist": "linear-gradient(90deg, #3D6BFF 0%, #00CFFF 100%)",
        "grad-guardian": "linear-gradient(90deg, #F0B34A 0%, #FF8C00 100%)",
        "grad-analyst": "linear-gradient(90deg, #00C896 0%, #00CFFF 100%)",
        "grad-visionary": "linear-gradient(90deg, #3D6BFF 0%, #6C63FF 100%)",
        "grad-ethicist": "linear-gradient(90deg, #FF4FA3 0%, #C15BFF 100%)",
      },
    },
  },
  plugins: [],
};

export default config;
