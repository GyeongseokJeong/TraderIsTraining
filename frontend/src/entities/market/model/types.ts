export interface Market { code: string; baseCurrency: string; quoteCurrency: string; isActive: boolean; }
export interface MarketsResponse { markets: Market[]; }
