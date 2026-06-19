export type Timeframe = 'MINUTE_1' | 'MINUTE_5' | 'MINUTE_15' | 'MINUTE_60' | 'MINUTE_240' | 'DAY';

export interface Candle {
  marketCode: string;
  timeframe: Timeframe;
  candleTimeUtc: string;
  candleTimeKst: string;
  open: string;
  high: string;
  low: string;
  close: string;
  volume: string;
  tradePriceVolume?: string | null;
}
