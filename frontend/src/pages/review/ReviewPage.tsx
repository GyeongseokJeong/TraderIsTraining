import { useQuery } from '@tanstack/react-query';
import { Link, useParams } from 'react-router-dom';
import { getReview } from '../../entities/trainingSession/api/trainingSessionApi';
import { ReviewSummary } from '../../widgets/reviewSummary/ReviewSummary';
import { CandleChart } from '../../shared/ui/CandleChart';
import { LoadingState } from '../../shared/ui/LoadingState';
import { ErrorState } from '../../shared/ui/ErrorState';
import { formatKrw, formatNumber } from '../../shared/lib/formatters';

export function ReviewPage() {
  const { sessionId = '' } = useParams();
  const query = useQuery({ queryKey: ['review', sessionId], queryFn: () => getReview(sessionId), enabled: Boolean(sessionId) });
  if (query.isLoading) return <LoadingState />;
  if (query.error || !query.data) return <ErrorState message={query.error?.message ?? '복기 데이터를 찾을 수 없습니다.'} />;
  const review = query.data;
  return <section className="page reviewPage"><h1>복기</h1><ReviewSummary review={review} /><div className="panel"><CandleChart candles={review.candles} trades={review.trades} /></div><section className="panel"><h2>거래 내역</h2><table><thead><tr><th>시간</th><th>구분</th><th>가격</th><th>수량</th><th>실현손익</th><th>노트</th></tr></thead><tbody>{review.trades.map((trade) => <tr key={trade.id}><td>{trade.candleTimeUtc}</td><td>{trade.side === 'BUY' ? '매수' : '매도'}</td><td>{formatKrw(trade.price)}</td><td>{formatNumber(trade.quantity)}</td><td>{trade.realizedPnl ? formatKrw(trade.realizedPnl) : '-'}</td><td>{trade.note ?? ''}</td></tr>)}</tbody></table></section><div className="actions"><Link to="/">새 랜덤 세션 시작</Link><Link to="/">같은 설정으로 다시 시작</Link></div></section>;
}
