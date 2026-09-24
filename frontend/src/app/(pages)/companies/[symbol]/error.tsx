"use client";

export default function CompanyError({
    reset,
}: {
    error: Error & { digest?: string };
    reset: () => void;
}) {
    return (
        <div className="rounded-xl border border-red-900/50 bg-red-950/30 p-6 text-center">
            <h2 className="text-lg font-semibold text-red-300">
                Unable to load this company
            </h2>

            <button
                type="button"
                onClick={() => reset()}
                className="mt-4 rounded-lg bg-[#2E8B57] px-4 py-2 text-sm font-medium text-white hover:bg-[#267349]"
            >
                Try again
            </button>
        </div>
    );
}