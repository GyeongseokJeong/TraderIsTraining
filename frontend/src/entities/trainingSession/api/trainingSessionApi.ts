import { apiRequest } from '../../../shared/api/client';
import type { TradeSide } from '../../trade/model/types';
import type { TrainingSessionCreate, TrainingSessionState } from '../model/types';
import type { Candle } from '../../candle/model/types';
import type { EquitySnapshot } from '../../equitySnapshot/model/types';
import type { Trade } from '../../trade/model/types';

export interface ReviewResponse { session: TrainingSessionState['session']; candles: Candle[]; trades: Trade[]; equityCurve: EquitySnapshot[]; performance: { finalEquity: string; finalReturnPct: string; realizedPnl: string; unrealizedPnl: string; maxDrawdown: string; tradeCount: number; winRate?: string | null; averageWinningTrade?: string | null; averageLosingTrade?: string | null; profitFactor?: string | null; buyAndHoldReturn: string; excessReturnVsBuyAndHold: string; }; }

export function createTrainingSession(payload: TrainingSessionCreate): Promise<TrainingSessionState> { return apiRequest('/training-sessions', { method: 'POST', body: JSON.stringify(payload) }); }
export function getTrainingSession(sessionId: string): Promise<TrainingSessionState> { return apiRequest(`/training-sessions/${sessionId}`); }
export function advanceCandle(sessionId: string): Promise<TrainingSessionState> { return apiRequest(`/training-sessions/${sessionId}/next`, { method: 'POST' }); }
export function placeTrade(sessionId: string, side: TradeSide, percentage: number, note?: string): Promise<TrainingSessionState> { return apiRequest(`/training-sessions/${sessionId}/trade`, { method: 'POST', body: JSON.stringify({ side, percentage, note }) }); }
export function finishSession(sessionId: string): Promise<ReviewResponse> { return apiRequest(`/training-sessions/${sessionId}/finish`, { method: 'POST' }); }
export function getReview(sessionId: string): Promise<ReviewResponse> { return apiRequest(`/training-sessions/${sessionId}/review`); }
