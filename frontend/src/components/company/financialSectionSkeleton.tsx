export default function FinancialSectionSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="mb-6 flex items-center justify-between">
        <div className="h-8 w-32 rounded bg-gray-800" />
        <div className="h-10 w-32 rounded bg-gray-800" />
      </div>

      <div className="flex flex-col gap-6 lg:flex-row">
        <div className="h-64 w-full rounded bg-gray-800 lg:w-80" />

        <div className="h-64 min-w-0 flex-1 rounded bg-gray-800" />
      </div>

      <div className="mt-6 h-32 w-full rounded bg-gray-800" />
    </div>
  );
}