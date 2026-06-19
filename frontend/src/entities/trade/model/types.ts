export type TradeSide = 'BUY' | 'SELL';
export interface Trade { id: string; side: TradeSide; candleTimeUtc: string; price: string; quantity: string; grossAmount: string; fee: string; netAmount: string; realizedPnl?: string | null; cashAfter: string; positionQtyAfter: string; avgEntryPriceAfter: string; note?: string | null; createdAt: string; }
