interface CouncilCoreProps {
  style?: React.CSSProperties;
}

export function CouncilCore({ style }: CouncilCoreProps) {
  return (
    <div style={style}>
      <div className="flex flex-col items-center">
        <div
          className="flex flex-col items-center justify-center rounded-full"
          style={{
            width: "140px",
            height: "140px",
            border: "1.5px solid rgba(108, 99, 255, 0.5)",
            background: "radial-gradient(circle at 40% 35%, rgba(108,99,255,0.25) 0%, rgba(3,7,22,0.95) 70%)",
            boxShadow: "0 0 30px rgba(108,99,255,0.35), 0 0 60px rgba(108,99,255,0.15)",
          }}
        >
          <img
            src="https://c.animaapp.com/mrqrcjormMWdDO/img/council-core-emblem.png"
            alt="Council Core emblem"
            className="w-12 h-12 object-contain mb-1"
          />
          <span className="text-foreground font-semibold text-sm text-center leading-tight">
            Council Core
          </span>
        </div>
        <span className="mt-2 text-muted text-[10px] text-center leading-tight px-2">
          Balance &middot; Wisdom &middot; Truth
        </span>
        <button
          className="mt-2 rounded-[10px] px-4 py-2 text-sm font-semibold text-white"
          style={{
            background: "linear-gradient(90deg, #A44BFF 0%, #6C63FF 100%)",
            boxShadow: "0 2px 8px rgba(108,99,255,0.4)",
          }}
        >
          Ajukan Question
        </button>
      </div>
    </div>
  );
}
