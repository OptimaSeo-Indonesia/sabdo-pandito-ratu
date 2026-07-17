import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sabdo Pandito Ratu",
  description: "Open source deliberation engine for multi-AI decision making",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 text-gray-900">{children}</body>
    </html>
  );
}
