import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { getMarkets } from '../../entities/market/api/marketApi';
import { createTrainingSession } from '../../entities/trainingSession/api/trainingSessionApi';
import type { Timeframe } from '../../entities/candle/model/types';
import { Button } from '../../shared/ui/Button';
import { LoadingState } from '../../shared/ui/LoadingState';
import { WarningBanner } from '../../shared/ui/WarningBanner';

export function SetupPage() {
  const navigate = useNavigate();
  const marketsQuery = useQuery({ queryKey: ['markets'], queryFn: getMarkets });
  const [marketCode, setMarketCode] = useState('KRW-BTC');
  const [timeframe, setTimeframe] = useState<Timeframe>('MINUTE_60');
  const [startTimeUtc, setStartTimeUtc] = useState('2024-01-01T00:00:00Z');
  const [endTimeUtc, setEndTimeUtc] = useState('2024-02-01T00:00:00Z');
  const [initialCapital, setInitialCapital] = useState('10000000');
  const [feeRatePercent, setFeeRatePercent] = useState('0.05');
  const [initialVisibleCount, setInitialVisibleCount] = useState(80);
  const mutation = useMutation({ mutationFn: createTrainingSession, onSuccess: (data) => navigate(`/training/${data.session.id}`) });
  if (marketsQuery.isLoading) return <LoadingState />;
  return <section className="page setupPage">
    <WarningBanner />
    <div className="hero"><h1>Trader Is Training</h1><p>Replay historical Upbit KRW candles, trade without seeing the future, and review your decisions.</p></div>
    <div className="panel formGrid">
      <label>마켓<select value={marketCode} onChange={(event) => setMarketCode(event.target.value)}>{marketsQuery.data?.markets.map((market) => <option key={market.code} value={market.code}>{market.code}</option>)}</select></label>
      <label>타임프레임<select value={timeframe} onChange={(event) => setTimeframe(event.target.value as Timeframe)}><option value="MINUTE_60">60분</option><option value="DAY">일봉</option><option value="MINUTE_1">1분</option><option value="MINUTE_5">5분</option><option value="MINUTE_15">15분</option><option value="MINUTE_240">240분</option></select></label>
      <label>시작 UTC<input value={startTimeUtc} onChange={(event) => setStartTimeUtc(event.target.value)} /></label>
      <label>종료 UTC<input value={endTimeUtc} onChange={(event) => setEndTimeUtc(event.target.value)} /></label>
      <label>초기 자본<input value={initialCapital} onChange={(event) => setInitialCapital(event.target.value)} /></label>
      <label>수수료율(%)<input value={feeRatePercent} onChange={(event) => setFeeRatePercent(event.target.value)} /></label>
      <label>초기 표시 캔들<input type="number" value={initialVisibleCount} onChange={(event) => setInitialVisibleCount(Number(event.target.value))} /></label>
      <Button disabled={mutation.isPending} onClick={() => mutation.mutate({ marketCode, timeframe, startTimeUtc, endTimeUtc, initialCapital, feeRate: String(Number(feeRatePercent) / 100), initialVisibleCount, randomMode: false })}>시작하기</Button>
      {mutation.error ? <p className="error">{mutation.error.message}</p> : null}
    </div>
  </section>;
}
