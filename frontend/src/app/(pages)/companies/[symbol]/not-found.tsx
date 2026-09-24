import Link from "next/link";

export default function CompanyNotFound() {
    return (
        <main className="flex min-h-[60vh] items-center justify-center px-4">
            <div className="text-center">
                <div className="animate-bounce text-8xl font-black text-[#2E8B57]">
                    404
                </div>

                <h1 className="mt-6 text-2xl font-bold text-white">
                    Company not found
                </h1>

                <p className="mt-3 text-sm text-gray-400">
                    We could not find the company you are looking for.
                </p>

                <Link
                    href="/companies"
                    className="mt-6 inline-block rounded-lg bg-[#2E8B57] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#267349]"
                >
                    Browse companies
                </Link>
            </div>
        </main>
    );
}