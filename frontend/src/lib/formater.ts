export function formatPrice(value: number | null): string {
    if (value == null) return "—";

    const abs = Math.abs(value);

    if (abs < 1) {
        return `$${abs.toFixed(4)}`;
    }

    return `$${abs.toFixed(2)}`;
}

export function formatChange(value: number | null): string {
    if (value == null) return "—";

    const abs = Math.abs(value);
    const sign = value < 0 ? "-" : value > 0 ? "+" : "";

    return `${sign}$${abs.toFixed(2)}`;
}

export function formatPercentage(value?: number | null): string {
    if (value == null) return "—";

    const abs = Math.abs(value);
    const sign = value < 0 ? "-" : value > 0 ? "+" : "";

    return `${sign}${abs.toFixed(2)}%`;
}

export function formatVolume(value: number | null): string {
    if (value == null) return "—";

    return new Intl.NumberFormat("en-US").format(value);
}

export function formatCurrency(value?: number | null): string {
    if (value == null) return "—";

    const abs = Math.abs(value);
    const sign = value < 0 ? "-" : "";

    if (abs >= 1_000_000_000) {
        return `${sign}$${(abs / 1_000_000_000).toFixed(2)}B`;
    }

    if (abs >= 1_000_000) {
        return `${sign}$${(abs / 1_000_000).toFixed(2)}M`;
    }

    return `${sign}$${abs.toLocaleString("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    })}`;
}

export function normalize(value?: string | null): string {
    return value?.trim().toLowerCase() ?? "";
}