import { useEffect, useRef } from 'react';
import { createChart, type IChartApi } from 'lightweight-charts';
import type { Candle } from '../../entities/candle/model/types';
import type { Trade } from '../../entities/trade/model/types';

export function CandleChart({ candles, trades = [] }: { candles: Candle[]; trades?: Trade[] }) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    if (!containerRef.current) return;
    let chart: IChartApi | null = createChart(containerRef.current, { height: 420, layout: { background: { color: '#111827' }, textColor: '#e5e7eb' }, grid: { vertLines: { color: '#1f2937' }, horzLines: { color: '#1f2937' } } });
    const series = chart.addCandlestickSeries({ upColor: '#22c55e', downColor: '#ef4444', borderVisible: false, wickUpColor: '#22c55e', wickDownColor: '#ef4444' });
    series.setData(candles.map((candle) => ({ time: candle.candleTimeUtc.slice(0, 10), open: Number(candle.open), high: Number(candle.high), low: Number(candle.low), close: Number(candle.close) })));
    series.setMarkers(trades.map((trade) => ({ time: trade.candleTimeUtc.slice(0, 10), position: trade.side === 'BUY' ? 'belowBar' : 'aboveBar', color: trade.side === 'BUY' ? '#38bdf8' : '#f97316', shape: trade.side === 'BUY' ? 'arrowUp' : 'arrowDown', text: trade.side === 'BUY' ? '매수' : '매도' })));
    chart.timeScale().fitContent();
    return () => { chart?.remove(); chart = null; };
  }, [candles, trades]);
  return <div ref={containerRef} className="chart" />;
}
