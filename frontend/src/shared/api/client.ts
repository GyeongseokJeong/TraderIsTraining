import { apiBaseUrl } from '../config/env';

export async function apiRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(options.headers ?? {}) },
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || 'API 요청에 실패했습니다.');
  }
  return response.json() as Promise<T>;
}
