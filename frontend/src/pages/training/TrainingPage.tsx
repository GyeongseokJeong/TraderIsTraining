import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate, useParams } from 'react-router-dom';
import { advanceCandle, finishSession, getTrainingSession, placeTrade } from '../../entities/trainingSession/api/trainingSessionApi';
import { TrainingHeader } from '../../widgets/trainingHeader/TrainingHeader';
import { TradingPanel } from '../../widgets/tradingPanel/TradingPanel';
import { CandleChart } from '../../shared/ui/CandleChart';
import { LoadingState } from '../../shared/ui/LoadingState';
import { ErrorState } from '../../shared/ui/ErrorState';
import { formatKrw, formatNumber } from '../../shared/lib/formatters';

export function TrainingPage() {
  const { sessionId = '' } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const query = useQuery({ queryKey: ['trainingSession', sessionId], queryFn: () => getTrainingSession(sessionId), enabled: Boolean(sessionId) });
  const updateCache = (data: Awaited<ReturnType<typeof getTrainingSession>>) => queryClient.setQueryData(['trainingSession', sessionId], data);
  const nextMutation = useMutation({ mutationFn: () => advanceCandle(sessionId), onSuccess: updateCache });
  const tradeMutation = useMutation({ mutationFn: ({ side, percentage }: { side: 'BUY' | 'SELL'; percentage: number }) => placeTrade(sessionId, side, percentage), onSuccess: updateCache });
  const finishMutation = useMutation({ mutationFn: () => finishSession(sessionId), onSuccess: () => navigate(`/review/${sessionId}`) });
  if (query.isLoading) return <LoadingState />;
  if (query.error || !query.data) return <ErrorState message={query.error?.message ?? '세션을 찾을 수 없습니다.'} />;
  const state = query.data;
  const pending = nextMutation.isPending || tradeMutation.isPending || finishMutation.isPending;
  return <section className="page trainingPage">
    <TrainingHeader state={state} />
    <main className="trainingMain"><div className="panel"><CandleChart candles={state.visibleCandles} /></div><TradingPanel state={state} pending={pending} onTrade={(side, percentage) => tradeMutation.mutate({ side, percentage })} onNext={() => nextMutation.mutate()} onFinish={() => finishMutation.mutate()} /></main>
    <section className="panel"><h2>거래 내역</h2><table><thead><tr><th>시간</th><th>구분</th><th>가격</th><th>수량</th><th>수수료</th><th>실현손익</th></tr></thead><tbody>{state.trades.map((trade) => <tr key={trade.id}><td>{trade.candleTimeUtc}</td><td>{trade.side === 'BUY' ? '매수' : '매도'}</td><td>{formatKrw(trade.price)}</td><td>{formatNumber(trade.quantity)}</td><td>{formatKrw(trade.fee)}</td><td>{trade.realizedPnl ? formatKrw(trade.realizedPnl) : '-'}</td></tr>)}</tbody></table></section>
  </section>;
}
