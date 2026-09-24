import { Mover } from "@/types/movers";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getMarketMovers(type: "gainers" | "losers" | "active"): Promise<Mover[]> {
  const url = `${API_URL}/api/v1/market_movers/?movers_type=${type}`;

  const response = await fetch(url,{cache: "no-store"});

  if (response.status === 404) {
    return [];
  }

  if (!response.ok) {
    const error = await response.text();
    console.log("API error:", error);
    throw new Error("Failed to fetch movers");
  }

  const data = await response.json();

  return data.movers;
}