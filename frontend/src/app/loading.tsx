export default function Loading(): React.ReactElement {
    return (
        <div className="space-y-8 animate-pulse">
            <div className="h-40 rounded-xl bg-gray-900" />

            <div className="flex flex-col gap-6 lg:flex-row">
                <div className="h-[420px] w-full rounded-xl bg-gray-900 lg:flex-1" />

                <div className="h-[420px] w-full rounded-xl bg-gray-900 lg:w-80" />
            </div>

            <div className="space-y-4">
                <div className="flex items-center justify-between">
                    <div className="h-7 w-32 rounded bg-gray-900" />
                    <div className="h-10 w-32 rounded bg-gray-900" />
                </div>

                <div className="flex flex-col gap-6 lg:flex-row">
                    <div className="h-96 w-full rounded-xl bg-gray-900 lg:w-80" />

                    <div className="h-96 w-full rounded-xl bg-gray-900 lg:flex-1" />
                </div>
            </div>
        </div>
    );
}