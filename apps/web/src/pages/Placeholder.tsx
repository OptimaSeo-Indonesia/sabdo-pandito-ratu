import { FileText } from "lucide-react";

export default function Placeholder({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-4 text-center">
      <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10 border border-primary/30">
        <FileText className="h-8 w-8 text-primary" />
      </div>
      <h1 className="text-2xl font-bold">{title}</h1>
      <p className="text-sm text-muted max-w-md">{subtitle}</p>
      <p className="text-xs text-muted/60 mt-2">
        Coming soon &mdash; this module is under development.
      </p>
    </div>
  );
}
