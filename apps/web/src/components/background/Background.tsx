import { GununganBg } from "./GununganBg";
import { FloatingParticles } from "./FloatingParticles";

export function Background() {
  return (
    <>
      {/* Layer 1: Dark gradient #0B1020 → #04060A */}
      <div
        className="pointer-events-none fixed inset-0"
        style={{
          background: "linear-gradient(180deg, #0B1020 0%, #04060A 100%)",
        }}
        aria-hidden="true"
      />

      {/* Layer 2: Aurora — soft blue/purple, 15% opacity, large blur */}
      <div
        className="pointer-events-none fixed inset-0"
        style={{
          background: `
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(79, 140, 255, 0.15), transparent),
            radial-gradient(ellipse 60% 40% at 80% 30%, rgba(124, 92, 255, 0.10), transparent),
            radial-gradient(ellipse 50% 30% at 20% 60%, rgba(0, 212, 255, 0.05), transparent)
          `,
        }}
        aria-hidden="true"
      />

      {/* Layer 3: Neural grid — thin lines, 3% opacity */}
      <div
        className="pointer-events-none fixed inset-0"
        style={{
          opacity: 0.03,
          backgroundImage: `
            linear-gradient(rgba(255,255,255,0.3) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.3) 1px, transparent 1px)
          `,
          backgroundSize: "80px 80px",
        }}
        aria-hidden="true"
      />

      {/* Layer 4: Gunungan */}
      <GununganBg />

      {/* Layer 5: Floating particles */}
      <FloatingParticles />

      {/* Layer 6: Radial glow — blue to purple, center, behind council */}
      <div
        className="pointer-events-none fixed inset-0 flex items-center justify-center"
        aria-hidden="true"
      >
        <div
          className="h-[60vh] w-[60vh] opacity-[0.08]"
          style={{
            background: "radial-gradient(circle, #4F8CFF 0%, #7C5CFF 40%, transparent 70%)",
            filter: "blur(60px)",
          }}
        />
      </div>
    </>
  );
}
