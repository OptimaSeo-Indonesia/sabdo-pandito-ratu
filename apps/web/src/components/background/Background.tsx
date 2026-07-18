import { GununganBg } from "./GununganBg";
import { FloatingParticles } from "./FloatingParticles";

export function Background() {
  return (
    <>
      {/* Layer 1-2: Dark gradient + aurora */}
      <div className="aurora-bg pointer-events-none fixed inset-0" />

      {/* Layer 3: Neural network pattern (subtle grid) */}
      <div
        className="pointer-events-none fixed inset-0 opacity-[0.015] dark:opacity-[0.03]"
        style={{
          backgroundImage: `
            radial-gradient(circle at 1px 1px, hsl(var(--primary)) 0.5px, transparent 0.5px)
          `,
          backgroundSize: "60px 60px",
        }}
        aria-hidden="true"
      />

      {/* Layer 4: Gunungan outline */}
      <GununganBg />

      {/* Layer 5: Floating particles */}
      <FloatingParticles />

      {/* Layer 6: Soft radial glow around council */}
      <div
        className="pointer-events-none fixed inset-0"
        aria-hidden="true"
      >
        <div
          className="absolute left-1/2 top-1/3 h-[60vh] w-[60vh] -translate-x-1/2 -translate-y-1/2 rounded-full opacity-[0.04] dark:opacity-[0.06]"
          style={{
            background: `radial-gradient(circle, hsl(var(--primary)) 0%, transparent 70%)`,
          }}
        />
      </div>
    </>
  );
}
