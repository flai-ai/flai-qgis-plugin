import requests
from pathlib import Path
from typing  import Optional

from qgis.PyQt.QtCore import QRunnable, pyqtSignal, QObject



class WorkerSignals(QObject):
    # overall worker progress: % of files completed (0–100)
    progress       = pyqtSignal(int, int)                 # worker_idx, percent
    # per-file lifecycle/progress
    file_started   = pyqtSignal(int, int, str, int)       # worker_idx, file_idx, filename, total_bytes (-1 if unknown)
    file_progress  = pyqtSignal(int, int, int, int)       # worker_idx, file_idx, bytes_done, total_bytes (-1 if unknown)
    file_done      = pyqtSignal(int, str, list, int)      # worker_idx, filepath, semantic schema, srid
    error          = pyqtSignal(int, str)                 # worker_idx, error message
    finished       = pyqtSignal(int)                      # worker_idx


class BatchDownloadWorker(QRunnable):

    def __init__(self, worker_idx, folder, urls, file_names, semantic_schema_for_point_clouds, srid):
        super().__init__()
        self._worker_idx     = worker_idx
        self._folder         = Path(folder)
        self._urls           = urls
        self._file_names     = file_names
        self._sematic_schema = semantic_schema_for_point_clouds  # (spelling kept to match your code)
        self._srid           = srid
        self._signals        = WorkerSignals()


    @staticmethod
    def find_existing_file_by_stem(folder: Path, stem: str) -> Optional[Path]:
        """
        Search recursively under `folder` for any file whose stem (name without extension)
        matches `stem`. Returns the first match or None if not found.
        """
        if not folder.exists():
            return None
        for candidate in folder.rglob('*'):
            if candidate.is_file() and candidate.stem == stem:
                return candidate
        return None


    def run(self):
        total_files = len(self._urls)
        files_done  = 0

        for file_idx, (url, fname) in enumerate(zip(self._urls, self._file_names)):
            try:
                dest = self._folder / fname
                dest.parent.mkdir(parents=True, exist_ok=True)

                # Skip if a file with the same stem already exists
                existing = self.find_existing_file_by_stem(self._folder, Path(fname).stem)
                if existing:
                    # Pretend it started & instantly finished
                    self._signals.file_started.emit(self._worker_idx, file_idx, fname, -1)
                    self._signals.file_progress.emit(self._worker_idx, file_idx, 1, -1)
                    self._signals.file_done.emit(self._worker_idx, str(existing), self._sematic_schema, self._srid)

                    files_done += 1
                    pct = int(files_done / total_files * 100)
                    self._signals.progress.emit(self._worker_idx, pct)
                    continue

                # download since not already present
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()

                    # If content-length is missing, treat as unknown (-1)
                    total_bytes = r.headers.get("Content-Length")
                    total_bytes = int(total_bytes) if total_bytes and total_bytes.isdigit() else -1

                    self._signals.file_started.emit(self._worker_idx, file_idx, fname, total_bytes)

                    bytes_done = 0
                    with open(dest, "wb") as f:
                        for chunk in r.iter_content(8192):
                            if not chunk:
                                continue
                            f.write(chunk)
                            bytes_done += len(chunk)
                            self._signals.file_progress.emit(self._worker_idx, file_idx, bytes_done, total_bytes)

                # per-file completion + overall update
                self._signals.file_done.emit(self._worker_idx, str(dest), self._sematic_schema, self._srid)

                files_done += 1
                pct = int(files_done / total_files * 100)
                self._signals.progress.emit(self._worker_idx, pct)

            except Exception as e:
                self._signals.error.emit(self._worker_idx, f"{fname}: {e}")

        self._signals.finished.emit(self._worker_idx)


