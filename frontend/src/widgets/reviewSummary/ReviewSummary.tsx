import type { ReviewResponse } from '../../entities/trainingSession/api/trainingSessionApi';
import { formatKrw, formatPercent } from '../../shared/lib/formatters';

export function ReviewSummary({ review }: { review: ReviewResponse }) {
  const p = review.performance;
  return <div className="panel summaryGrid"><div>최종 평가금액<br />{formatKrw(p.finalEquity)}</div><div>수익률<br />{formatPercent(p.finalReturnPct)}</div><div>실현손익<br />{formatKrw(p.realizedPnl)}</div><div>미실현손익<br />{formatKrw(p.unrealizedPnl)}</div><div>최대낙폭<br />{formatPercent(Number(p.maxDrawdown) * 100)}</div><div>거래수<br />{p.tradeCount}</div><div>승률<br />{p.winRate ? formatPercent(p.winRate) : '-'}</div><div>Buy & Hold<br />{formatPercent(p.buyAndHoldReturn)}</div><div>초과수익<br />{formatPercent(p.excessReturnVsBuyAndHold)}</div></div>;
}
