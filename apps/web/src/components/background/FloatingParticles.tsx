export function FloatingParticles() {
  const dots = Array.from({ length: 30 }, (_, i) => ({
    id: i,
    left: `${((i * 17 + 11) % 100)}%`,
    top: `${((i * 23 + 7) % 100)}%`,
    delay: `${(i * 0.7) % 4}s`,
    duration: `${4 + (i % 3)}s`,
  }));

  return (
    <div className="pointer-events-none fixed inset-0 overflow-hidden" aria-hidden="true">
      {dots.map((d) => (
        <div
          key={d.id}
          className="absolute rounded-full bg-white"
          style={{
            left: d.left,
            top: d.top,
            width: 2,
            height: 2,
            opacity: 0.15,
            animation: `pulseSoft ${d.duration} ease-in-out ${d.delay} infinite`,
          }}
        />
      ))}
    </div>
  );
}
