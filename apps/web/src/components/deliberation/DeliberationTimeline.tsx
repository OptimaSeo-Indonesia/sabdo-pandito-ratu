import { cn } from "../../lib/utils";

interface Step {
  name: string;
  label: string;
  status: "pending" | "in_progress" | "completed" | "failed";
}

interface DeliberationTimelineProps {
  steps: Step[];
  className?: string;
}

function StatusIcon({ status }: { status: Step["status"] }) {
  if (status === "completed") {
    return (
      <svg className="h-4 w-4" viewBox="0 0 16 16" fill="none">
        <circle cx="8" cy="8" r="7" fill="rgba(108,99,255,0.15)" stroke="rgba(108,99,255,0.5)" strokeWidth="0.5" />
        <path d="M5 8.5L7 10.5L11 6" stroke="#4ADE80" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    );
  }
  if (status === "in_progress") {
    return (
      <div className="relative flex h-4 w-4 items-center justify-center">
        <div className="h-4 w-4 rounded-full border-2 border-primary shadow-[0_0_12px_rgba(108,99,255,0.6)]" />
        <div className="absolute h-1.5 w-1.5 rounded-full bg-primary" />
      </div>
    );
  }
  return (
    <svg className="h-4 w-4" viewBox="0 0 16 16" fill="none">
      <circle cx="8" cy="8" r="7" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.12)" strokeWidth="0.5" />
    </svg>
  );
}

export function DeliberationTimeline({ steps, className }: DeliberationTimelineProps) {
  return (
    <div className={cn("flex flex-col gap-0", className)}>
      {steps.map((step, i) => {
        const isInProgress = step.status === "in_progress";
        const isCompleted = step.status === "completed";

        return (
          <div key={step.name}>
            <div className="flex items-center gap-3 py-2">
              <StatusIcon status={step.status} />
              <div>
                <p
                  className={cn(
                    "text-sm font-medium leading-tight",
                    isInProgress && "text-foreground font-semibold",
                    isCompleted && "text-foreground",
                    !isInProgress && !isCompleted && "text-muted"
                  )}
                >
                  {step.label}
                </p>
                <p className="text-[11px] text-muted mt-0.5">
                  {isInProgress && <span className="text-primary">In Progress</span>}
                  {isCompleted && "Completed"}
                  {!isInProgress && !isCompleted && "Pending"}
                </p>
              </div>
            </div>

            {/* Connector */}
            {i < steps.length - 1 && (
              <div className="ml-2 pl-[7px]">
                <div
                  className={cn(
                    "w-[2px] h-3",
                    isInProgress
                      ? "bg-[linear-gradient(180deg,rgba(108,99,255,0.7)_0%,rgba(108,99,255,0.3)_100%)]"
                      : isCompleted
                        ? "bg-[rgba(108,99,255,0.5)]"
                        : "border-l-2 border-dashed border-[rgba(255,255,255,0.12)]"
                  )}
                />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
