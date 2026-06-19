import time
from datetime import datetime
from typing import Any

import httpx

from app.core.config import get_settings
from app.features.candles.enums import Timeframe

_TIMEFRAME_ENDPOINTS = {
    Timeframe.minute_1: "/v1/candles/minutes/1",
    Timeframe.minute_5: "/v1/candles/minutes/5",
    Timeframe.minute_15: "/v1/candles/minutes/15",
    Timeframe.minute_60: "/v1/candles/minutes/60",
    Timeframe.minute_240: "/v1/candles/minutes/240",
    Timeframe.day: "/v1/candles/days",
}


class UpbitClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._last_request_at = 0.0

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        wait_seconds = self.settings.upbit_request_interval_seconds - elapsed
        if wait_seconds > 0:
            time.sleep(wait_seconds)
        self._last_request_at = time.monotonic()

    def get_candles(self, *, market_code: str, timeframe: Timeframe, to: datetime | None, count: int = 200) -> list[dict[str, Any]]:
        endpoint = _TIMEFRAME_ENDPOINTS[timeframe]
        params: dict[str, Any] = {"market": market_code, "count": min(count, 200)}
        if to is not None:
            params["to"] = to.strftime("%Y-%m-%dT%H:%M:%S")
        last_error: Exception | None = None
        for attempt in range(self.settings.upbit_max_retries):
            self._throttle()
            try:
                with httpx.Client(base_url=self.settings.upbit_base_url, timeout=10.0) as client:
                    response = client.get(endpoint, params=params)
                if response.status_code == 429:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                response.raise_for_status()
                return list(response.json())
            except (httpx.HTTPError, ValueError) as exc:
                last_error = exc
                time.sleep(0.3 * (attempt + 1))
        raise RuntimeError("failed to fetch Upbit candles") from last_error
