#!/usr/bin/env python3
"""ESP32-CAM stream viewer (laptop-side)

Usage
~~~~~
  ./z_streaming_client_1.py --url http://192.168.0.105/username/password  \
                            --avg-n 10 --wait-ms 1

  Exit: press 'x' in the video window.

Notes
~~~~~
- Reads MJPEG/HTTP video stream from an ESP32-CAM (or any OpenCV-readable URL)
- Displays the stream via OpenCV
- Prints frame time statistics as a runtime average over the last N frames

- OpenCV's VideoCapture over HTTP can be finicky depending on the stream format
- For best results, ESP32-CAM endpoint should provide a continuous MJPEG stream
"""

from __future__ import annotations

import sys
import time
from collections import deque
from dataclasses import dataclass
from typing import Deque, Optional, Tuple

import click
import cv2

@dataclass
class Stats:
    """Tracks per-frame timing and reports rolling averages."""

    window: int
    dt_s: Deque[float]

    def __init__(self, window: int) -> None:
        self.window = max(1, int(window))
        self.dt_s = deque(maxlen=self.window)

    def add(self, dt_s: float) -> None:
        if dt_s <= 0 or dt_s > 10:
            return
        self.dt_s.append(dt_s)

    def mean_dt(self) -> Optional[float]:
        if not self.dt_s:
            return None
        return sum(self.dt_s) / len(self.dt_s)

    def mean_fps(self) -> Optional[float]:
        m = self.mean_dt()
        if not m or m <= 0:
            return None
        return 1.0 / m

def open_capture(url: str) -> cv2.VideoCapture:
    video = cv2.VideoCapture(url)
    return video

def try_read_frame(video: cv2.VideoCapture) -> Tuple[bool, Optional["cv2.Mat"]]:
    ret, frame = video.read()
    if frame is None:
        return False, None
    return ret, frame

@click.command(context_settings={"show_default": True})
@click.option(
    "--url",
    type=str,
    default="http://192.168.0.105/username/password",
    help="OpenCV VideoCapture URL, e.g MJPEG stream endpoint"
)
@click.option(
    "--window-title",
    type=str,
    default="ESP32-CAM",
    help="OpenCV window title.",
)
@click.option(
    "--avg-n",
    type=int,
    default=10,
    help="Rolling window size for average frame time/FPS.",
)
@click.option(
    "--wait-ms",
    type=int,
    default=20,
    help="cv2.waitKey delay in ms (also influences UI responsiveness).",
)
@click.option(
    "--dropped-limit",
    type=int,
    default=100,
    help="Consecutive dropped frames before forcing reconnect.",
)
@click.option(
    "--reconnect-sleep",
    type=float,
    default=1.0,
    help="Seconds to sleep between reconnect attempts.",
)
@click.option(
    "--print-every",
    type=int,
    default=10,
    help="Print timing stats every N displayed frames.",
)
@click.option(
    "--overlay-stats/--no-overlay-stats",
    default=True,
    help="Overlay timing stats on the video frame.",
)
@click.option(
    "--verbose/--quiet",
    default=True,
    help="Print reconnect and timing messages.",
)
def main(
    url: str,
    window_title: str,
    avg_n: int,
    wait_ms: int,
    dropped_limit: int,
    reconnect_sleep: float,
    print_every: int,
    overlay_stats: bool,
    verbose: bool,
) -> None:
    """Display an ESP32-CAM stream and report rolling average frame times."""

    stats = Stats(window=avg_n)

    frame_count = 0
    last_t = time.perf_counter()

    while True:
        video = open_capture(url)
        if verbose:
            print(f"Connecting: {url}")

        dropped = 0

        while True:
            now = time.perf_counter()
            ok, frame = try_read_frame(video)
            t_after_read = time.perf_counter()

            if frame is None:
                dropped += 1
                if dropped == 1 and verbose:
                    print("Dropped frame(s)...")

                if dropped >= dropped_limit:
                    if verbose:
                        print(f"Dropped {dropped} frames; reconnecting...")
                    break

                time.sleep(0.01)
                continue

            dropped = 0
            frame_count += 1

            dt = t_after_read - last_t
            last_t = t_after_read
            stats.add(dt)

            mean_dt = stats.mean_dt()
            mean_fps = stats.mean_fps()

            if overlay_stats and mean_dt is not None:
                text = f"avg({len(stats.dt_s)}/{stats.window}) {mean_dt*1000.0:6.1f} ms  {mean_fps:5.1f} fps"
                cv2.putText(
                    frame,
                    text,
                    (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                    cv2.LINE_AA,
                )

            cv2.imshow(window_title, frame)

            if verbose and print_every > 0 and (frame_count % print_every == 0):
                if mean_dt is not None:
                    print(
                        f"frames={frame_count:8d}  avg_dt({len(stats.dt_s)}/{stats.window})={mean_dt*1000.0:7.2f} ms"
                        f"  avg_fps={mean_fps:6.2f}"
                    )

            key = cv2.waitKey(max(1, wait_ms)) & 0xFF
            if key == ord("x"):
                video.release()
                cv2.destroyAllWindows()
                if verbose:
                    print("Quit")
                return

        video.release()
        if reconnect_sleep > 0:
            time.sleep(reconnect_sleep)


if __name__ == "__main__":
    try:
        main(standalone_mode=True)
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        sys.exit(130)
