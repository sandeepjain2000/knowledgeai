"""
watcher.py — Watch the BRDs folder for new/modified files and auto-ingest them.
Uses the watchdog library to monitor filesystem events.
"""
import asyncio
import logging
import os

from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent
from watchdog.observers import Observer

from backend.config import BRD_FOLDER

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt", ".md", ".rst"}


class BRDEventHandler(FileSystemEventHandler):
    """Handle file system events in the BRDs folder."""

    def __init__(self, loop: asyncio.AbstractEventLoop):
        super().__init__()
        self._loop = loop

    def _schedule_ingest(self, path: str):
        from backend.ingestion.orchestrator import enqueue
        fname = os.path.basename(path)
        ext   = os.path.splitext(fname)[1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            return
        logger.info("Watcher detected change: %s", fname)
        asyncio.run_coroutine_threadsafe(
            enqueue(path, folder="BRDs", original_name=fname),
            self._loop,
        )

    def on_created(self, event):
        if not event.is_directory:
            self._schedule_ingest(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self._schedule_ingest(event.src_path)


def start_watcher(loop: asyncio.AbstractEventLoop):
    """Start the watchdog observer in a background thread."""
    if not os.path.isdir(BRD_FOLDER):
        logger.warning("BRD folder not found, watcher not started: %s", BRD_FOLDER)
        return

    handler  = BRDEventHandler(loop)
    observer = Observer()
    observer.schedule(handler, BRD_FOLDER, recursive=True)
    observer.start()
    logger.info("Watching BRDs folder: %s", BRD_FOLDER)
    return observer
