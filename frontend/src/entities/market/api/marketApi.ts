import { apiRequest } from '../../../shared/api/client';
import type { MarketsResponse } from '../model/types';

export function getMarkets(): Promise<MarketsResponse> { return apiRequest<MarketsResponse>('/markets'); }
