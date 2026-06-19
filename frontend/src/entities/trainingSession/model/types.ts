import type { Candle, Timeframe } from '../../candle/model/types';
import type { Trade } from '../../trade/model/types';

export interface TrainingSession { id: string; marketCode: string; timeframe: Timeframe; startTimeUtc: string; endTimeUtc: string; initialVisibleCount: number; currentIndex: number; totalCandleCount: number; initialCapital: string; feeRate: string; cash: string; positionQty: string; avgEntryPrice: string; realizedPnl: string; status: 'SETUP' | 'RUNNING' | 'FINISHED'; mode: 'PERSONAL_REVIEW'; finishedAt?: string | null; }
export interface AccountSummary { initialCapital: string; cash: string; positionQty: string; avgEntryPrice: string; currentPrice: string; realizedPnl: string; unrealizedPnl: string; totalEquity: string; returnPct: string; maxDrawdown: string; }
export interface TrainingSessionState { session: TrainingSession; visibleCandles: Candle[]; trades: Trade[]; accountSummary: AccountSummary; }
export interface TrainingSessionCreate { marketCode: string; timeframe: Timeframe; startTimeUtc: string; endTimeUtc: string; initialCapital: string; feeRate: string; initialVisibleCount: number; randomMode: boolean; }
