import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#f0f4ff",
          900: "#1e3a5f",
        },
      },
    },
  },
  plugins: [],
};

export default config;
