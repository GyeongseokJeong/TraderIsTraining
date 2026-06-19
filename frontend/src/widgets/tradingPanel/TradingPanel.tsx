import { Button } from '../../shared/ui/Button';
import { formatKrw, formatNumber, formatPercent } from '../../shared/lib/formatters';
import type { TrainingSessionState } from '../../entities/trainingSession/model/types';

export function TradingPanel({ state, onTrade, onNext, onFinish, pending }: { state: TrainingSessionState; onTrade: (side: 'BUY' | 'SELL', percentage: number) => void; onNext: () => void; onFinish: () => void; pending: boolean; }) {
  const summary = state.accountSummary;
  const percentages = [25, 50, 75, 100];
  return <aside className="panel tradingPanel">
    <h2>계좌</h2>
    <dl><dt>현금</dt><dd>{formatKrw(summary.cash)}</dd><dt>보유수량</dt><dd>{formatNumber(summary.positionQty)}</dd><dt>평균단가</dt><dd>{formatKrw(summary.avgEntryPrice)}</dd><dt>평가금액</dt><dd>{formatKrw(summary.totalEquity)}</dd><dt>실현손익</dt><dd>{formatKrw(summary.realizedPnl)}</dd><dt>미실현손익</dt><dd>{formatKrw(summary.unrealizedPnl)}</dd><dt>최대낙폭</dt><dd>{formatPercent(Number(summary.maxDrawdown) * 100)}</dd><dt>수익률</dt><dd>{formatPercent(summary.returnPct)}</dd></dl>
    <h2>주문</h2>
    <div className="buttonGrid">{percentages.map((p) => <Button key={`buy-${p}`} disabled={pending || Number(summary.cash) <= 0} onClick={() => onTrade('BUY', p)}>매수 {p}%</Button>)}</div>
    <div className="buttonGrid">{percentages.map((p) => <Button key={`sell-${p}`} disabled={pending || Number(summary.positionQty) <= 0} onClick={() => onTrade('SELL', p)}>매도 {p}%</Button>)}</div>
    <Button disabled={pending || state.session.currentIndex >= state.session.totalCandleCount - 1} onClick={onNext}>관망 / 다음 캔들</Button>
    <Button disabled={pending} onClick={onFinish}>세션 종료</Button>
  </aside>;
}
