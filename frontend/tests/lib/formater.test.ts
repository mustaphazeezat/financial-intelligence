import { describe, expect, it } from "vitest";
import {
    formatPrice,
    formatChange,
    formatPercentage,
    formatVolume,
    formatCurrency,
    normalize,
} from "@/lib/formater";

describe("formatPrice", () => {
    it("returns a dash for null", () => {
        expect(formatPrice(null)).toBe("—");
    });

    it("formats values with 2 decimals for values >= 1", () => {
        expect(formatPrice(123.45)).toBe("$123.45");
    });

    it("formats values with 4 decimals for values < 1", () => {
        expect(formatPrice(0.1234)).toBe("$0.1234");
    });
});

describe("formatChange", () => {
    it("adds a plus sign to positive values", () => {
        expect(formatChange(3.5)).toBe("+$3.50");
    });

    it("keeps negative sign for negative values", () => {
        expect(formatChange(-3.5)).toBe("-$3.50");
    });

    it("returns a dash for null", () => {
        expect(formatChange(null)).toBe("—");
    });
});

describe("formatPercentage", () => {
    it("adds a plus sign to positive values", () => {
        expect(formatPercentage(2.5)).toBe("+2.50%");
    });

    it("keeps a minus sign for negative values", () => {
        expect(formatPercentage(-2.5)).toBe("-2.50%");
    });

    it("returns a dash for null", () => {
        expect(formatPercentage(null)).toBe("—");
    });
});

describe("formatVolume", () => {
    it("formats numbers with comma separators", () => {
        expect(formatVolume(1234567)).toBe("1,234,567");
    });

    it("returns a dash for null", () => {
        expect(formatVolume(null)).toBe("—");
    });
});

describe("formatCurrency", () => {
    it("returns a dash for null", () => {
        expect(formatCurrency(null)).toBe("—");
    });

    it("formats values under 1M as USD", () => {
        expect(formatCurrency(2500)).toBe("$2,500.00");
    });

    it("formats values in millions", () => {
        expect(formatCurrency(1500000)).toBe("$1.50M");
    });

    it("formats values in billions", () => {
        expect(formatCurrency(1500000000)).toBe("$1.50B");
    });

    it("handles negative values", () => {
        expect(formatCurrency(-1500000)).toBe("-$1.50M");
    });
});

describe("normalize", () => {
    it("returns empty string for nullish values", () => {
        expect(normalize(null)).toBe("");
        expect(normalize(undefined)).toBe("");
    });

    it("trims and lowercases values", () => {
        expect(normalize("  Technology  ")).toBe("technology");
    });
});