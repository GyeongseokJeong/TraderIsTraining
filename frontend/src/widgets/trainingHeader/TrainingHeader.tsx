import type { TrainingSessionState } from '../../entities/trainingSession/model/types';

export function TrainingHeader({ state }: { state: TrainingSessionState }) {
  const current = state.visibleCandles.at(-1);
  return <header className="trainingHeader panel"><strong>{state.session.marketCode}</strong><span>{state.session.timeframe}</span><span>{current?.candleTimeUtc}</span><span>{state.session.currentIndex + 1} / {state.session.totalCandleCount}</span></header>;
}
