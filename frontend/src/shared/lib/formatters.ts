export function formatKrw(value: string | number): string {
  return `${Number(value).toLocaleString('ko-KR', { maximumFractionDigits: 0 })} KRW`;
}

export function formatNumber(value: string | number, digits = 8): string {
  return Number(value).toLocaleString('ko-KR', { maximumFractionDigits: digits });
}

export function formatPercent(value: string | number): string {
  return `${Number(value).toFixed(2)}%`;
}
