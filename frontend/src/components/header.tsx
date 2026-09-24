import Link from "next/link";

const navItems = [
  { label: "Overview", href: "/" },
  { label: "Companies", href: "/companies" },
  { label: "Market Movers", href: "/market" },
];

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-900 backdrop-blur-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-4 py-3 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-black text-white">
            <span className="text-lg font-black italic">FIP</span>
          </div>

          <div>
            <p className="text-[10px] font-medium uppercase tracking-[0.22em] text-slate-500">
              Finance
            </p>
            <Link href="/" className="text-lg font-semibold tracking-tight text-gray-50">
              MarketPulse
            </Link>
          </div>
        </div>

        <nav aria-label="Main navigation" className="hidden items-center gap-2 md:flex">
          {navItems.map((item) => (
            <Link
              key={item.label}
              href={item.href}
              className="rounded-full px-3 py-2 text-sm font-medium text-gray-50 transition hover:bg-slate-100 hover:text-black"
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          <button
            type="button"
            className="hidden rounded-full border border-slate-300 bg-slate-100 px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200 sm:inline-flex"
          >
            Search
          </button>
        </div>
      </div>
    </header>
  );
}
