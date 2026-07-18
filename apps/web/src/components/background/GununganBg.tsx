export function GununganBg() {
  return (
    <div className="pointer-events-none fixed inset-0 flex items-center justify-center opacity-[0.03] dark:opacity-[0.04]">
      <svg
        viewBox="0 0 400 600"
        className="h-[80vh] w-auto blur-[2px]"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        {/* Gunungan (Kekayon) — Javanese cosmic tree/mountain silhouette */}
        <g
          stroke="#C9A84C"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        >
          {/* Central peak */}
          <path d="M200 30 C195 60, 190 90, 188 120 C185 150, 183 170, 185 190" />
          <path d="M200 30 C205 60, 210 90, 212 120 C215 150, 217 170, 215 190" />

          {/* Left wing */}
          <path d="M185 190 C170 200, 140 210, 110 230 C80 250, 50 280, 35 320 C25 350, 30 380, 40 400" />
          <path d="M185 220 C160 235, 130 255, 105 280 C80 305, 60 340, 55 370" />

          {/* Right wing */}
          <path d="M215 190 C230 200, 260 210, 290 230 C320 250, 350 280, 365 320 C375 350, 370 380, 360 400" />
          <path d="M215 220 C240 235, 270 255, 295 280 C320 305, 340 340, 345 370" />

          {/* Central trunk */}
          <path d="M185 190 C188 220, 190 250, 192 280 C194 310, 196 340, 197 370" />
          <path d="M215 190 C212 220, 210 250, 208 280 C206 310, 204 340, 203 370" />

          {/* Trunk fill suggestions */}
          <path d="M197 370 C198 390, 198 410, 197 430" />
          <path d="M203 370 C202 390, 202 410, 203 430" />

          {/* Base */}
          <path d="M197 430 C170 440, 130 445, 100 450" />
          <path d="M203 430 C230 440, 270 445, 300 450" />
          <path d="M100 450 C120 460, 180 465, 200 465 C220 465, 280 460, 300 450" />

          {/* Left ornamental curves */}
          <path d="M110 230 C95 240, 78 260, 70 290" strokeWidth="1" />
          <path d="M80 250 C65 265, 50 290, 48 320" strokeWidth="1" />

          {/* Right ornamental curves */}
          <path d="M290 230 C305 240, 322 260, 330 290" strokeWidth="1" />
          <path d="M320 250 C335 265, 350 290, 352 320" strokeWidth="1" />

          {/* Inner decorative elements */}
          <path d="M190 120 C192 140, 195 160, 197 180" strokeWidth="0.8" />
          <path d="M210 120 C208 140, 205 160, 203 180" strokeWidth="0.8" />

          {/* Small wing tips */}
          <path d="M40 400 C30 410, 25 420, 28 430" strokeWidth="1" />
          <path d="M360 400 C370 410, 375 420, 372 430" strokeWidth="1" />
        </g>
      </svg>
    </div>
  );
}
