import type { ReactNode } from "react";
import { Link } from "react-router-dom";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <>
      <nav className="border-b bg-white shadow-sm">
        <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-3">
          <Link to="/" className="text-lg font-bold tracking-tight">
            Sabdo Pandito Ratu
          </Link>
          <div className="flex gap-4 text-sm text-gray-500">
            <Link to="/" className="hover:text-gray-900">Home</Link>
            <Link to="/sessions" className="hover:text-gray-900">History</Link>
          </div>
        </div>
      </nav>
      {children}
      <footer className="border-t bg-white py-6 text-center text-sm text-gray-400">
        Sabdo Pandito Ratu &mdash; Open Source Deliberation Engine
      </footer>
    </>
  );
}
