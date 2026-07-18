export function FloatingParticles() {
  const dots = Array.from({ length: 30 }, (_, i) => ({
    id: i,
    left: `${((i * 17 + 11) % 100)}%`,
    top: `${((i * 23 + 7) % 100)}%`,
    delay: `${(i * 0.7) % 4}s`,
    size: (i % 3) + 1,
    opacity: 0.1 + (i % 5) * 0.05,
  }));

  return (
    <div className="pointer-events-none fixed inset-0 overflow-hidden" aria-hidden="true">
      {dots.map((d) => (
        <div
          key={d.id}
          className="absolute rounded-full bg-primary"
          style={{
            left: d.left,
            top: d.top,
            width: d.size,
            height: d.size,
            opacity: d.opacity,
            animation: `pulseSoft ${2 + (d.id % 3)}s ease-in-out ${d.delay} infinite`,
          }}
        />
      ))}
    </div>
  );
}
