import HeroSearch from '@/components/home/HeroSearch';
import MoversSection from '@/components/home/MoversSection';
import { getMarketMovers } from '@/lib/api/market';

export default async function Home() {
  const [gainers, losers, mostActive] = await Promise.all([
    getMarketMovers("gainers"),
    getMarketMovers("losers"),
    getMarketMovers("active"),
  ]);
  return (
    <div className="space-y-8">
      <HeroSearch />
      <MoversSection
        gainers={gainers}
        losers={losers}
        mostActive={mostActive}
      />
    </div>
  );
}
