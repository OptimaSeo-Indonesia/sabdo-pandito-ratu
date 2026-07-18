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
      <body className="min-h-screen bg-gray-50 text-gray-900">
        <nav className="border-b bg-white shadow-sm">
          <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-3">
            <a href="/" className="text-lg font-bold tracking-tight">
              Sabdo Pandito Ratu
            </a>
            <div className="flex gap-4 text-sm text-gray-500">
              <a href="/" className="hover:text-gray-900">Home</a>
              <a href="/sessions" className="hover:text-gray-900">History</a>
            </div>
          </div>
        </nav>
        {children}
        <footer className="border-t bg-white py-6 text-center text-sm text-gray-400">
          Sabdo Pandito Ratu &mdash; Open Source Deliberation Engine
        </footer>
      </body>
    </html>
  );
}
