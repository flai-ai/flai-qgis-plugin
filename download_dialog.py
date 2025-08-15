from typing import Dict, Tuple

from .download_worker import BatchDownloadWorker
from .constants       import TEXT_SIZE_INSIDE_MSG_BOX

from qgis.PyQt.QtCore    import QThreadPool, QEvent, Qt
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem, QProgressBar, QAbstractItemView



class DownloadDialog(QDialog):

    def __init__(self, task_list, parent=None):
        """
        task_list: list of dicts, each with keys:
           - folder_where_to_save: str
           - urls: list of (url) or (url, filename) tuples  (you pass url + file_names separately)
           - file_names: list[str]
           - semantic_schema: list/obj (your type)
           - srid: int
        """
        super().__init__(parent)
        self._main_dialog = parent

        self.setWindowTitle("Parallel Downloader")
        self.resize(800, 480)
        self.setStyleSheet(f"* {{ font-size: {TEXT_SIZE_INSIDE_MSG_BOX}pt; }}")

        self._tasks = task_list
        self._pool = QThreadPool.globalInstance()
        self._pool.setMaxThreadCount(len(self._tasks))
        self._workers = []  # keep references

        # tree with parent (worker) + child (files)
        self._tree = QTreeWidget()
        self._tree.setHeaderLabels(["Folder with files", "Progress"])
        self._tree.setRootIsDecorated(True)
        self._tree.setAlternatingRowColors(True)
        self._tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._tree.setFocusPolicy(Qt.NoFocus)
        self._tree.setUniformRowHeights(False)  # allow tall rows if needed

        self._statusLbl = QLabel("Ready")

        lay = QVBoxLayout(self)
        lay.addWidget(self._tree)
        bottom = QHBoxLayout()
        bottom.addStretch()
        bottom.addWidget(self._statusLbl)
        lay.addLayout(bottom)

        # maps to reach bars quickly
        self._overall_bars: Dict[int, QProgressBar] = {}
        self._file_bars: Dict[Tuple[int, int], QProgressBar] = {}

        # Populate workers/files
        for worker_idx, task in enumerate(self._tasks):
            folder = task["folder_where_to_save"]

            # parent item (no text in col 0; we'll insert a QLabel there)
            parent_item = QTreeWidgetItem(["", ""])
            self._tree.addTopLevelItem(parent_item)

            # right-aligned folder label in column 0 (like before)
            folder_lbl = QLabel(folder)
            folder_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            folder_lbl.setContentsMargins(4, 0, 4, 0)  # padding like your table code
            self._tree.setItemWidget(parent_item, 0, folder_lbl)

            # overall progress bar for this worker
            overall_bar = QProgressBar()
            overall_bar.setRange(0, 100)
            overall_bar.setValue(0)
            overall_bar.setTextVisible(True)
            self._tree.setItemWidget(parent_item, 1, overall_bar)
            self._overall_bars[worker_idx] = overall_bar

            # child rows: one per file
            for file_idx, fname in enumerate(task["file_names"]):
                child_item = QTreeWidgetItem([fname, ""])
                parent_item.addChild(child_item)

                bar = QProgressBar()
                # start "queued". We'll set real range/value on file_started
                bar.setRange(0, 100)
                bar.setValue(0)
                bar.setTextVisible(True)
                bar.setFormat("Queued")
                self._tree.setItemWidget(child_item, 1, bar)
                self._file_bars[(worker_idx, file_idx)] = bar

            parent_item.setExpanded(True)  # expand to show files

        # adjust column widths & keep ratio on resize
        self._adjust_column_widths()
        self._tree.viewport().installEventFilter(self)

        # download files
        self.start_downloads()


    def _adjust_column_widths(self):
        total = self._tree.viewport().width()
        if total <= 0:
            return
        self._tree.setColumnWidth(0, int(total * 0.65))
        self._tree.setColumnWidth(1, total - int(total * 0.65))


    def eventFilter(self, obj, event):
        if obj is self._tree.viewport() and event.type() == QEvent.Resize:
            self._adjust_column_widths()
        return super().eventFilter(obj, event)


    def start_downloads(self):
        self._statusLbl.setText("Downloading...")
        self._finished_workers = 0

        for idx, task in enumerate(self._tasks):
            worker = BatchDownloadWorker(
                worker_idx                       = idx,
                folder                           = task["folder_where_to_save"],
                urls                             = task["urls"],
                file_names                       = task["file_names"],
                semantic_schema_for_point_clouds = task['semantic_schema'],
                srid                             = task['srid'],
            )

            s = worker._signals
            s.progress.connect(self._on_worker_progress)
            s.file_started.connect(self._on_file_started)
            s.file_progress.connect(self._on_file_progress)
            s.file_done.connect(self._on_file_done)
            s.error.connect(self._on_error)
            s.finished.connect(self._on_finished)

            self._workers.append(worker)  # keep reference
            self._pool.start(worker)


    # signal handlers
    def _on_worker_progress(self, worker_idx: int, percent: int):
        bar: QProgressBar = self._overall_bars[worker_idx]
        bar.setValue(percent)
        bar.setFormat(f"{percent}%")


    def _on_file_started(self, worker_idx: int, file_idx: int, filename: str, total_bytes: int):
        bar: QProgressBar = self._file_bars[(worker_idx, file_idx)]
        if total_bytes > 0:
            bar.setRange(0, 100)
            bar.setValue(0)
            bar.setFormat(f"{filename} - 0% (0 / {self._main_dialog._human_readable(total_bytes)})")
        else:
            # Unknown size -> indeterminate but still show label
            bar.setRange(0, 0)
            bar.setFormat(f"{filename} - downloading... (size unknown)")


    def _on_file_progress(self, worker_idx: int, file_idx: int, bytes_done: int, total_bytes: int):
        bar: QProgressBar = self._file_bars[(worker_idx, file_idx)]
        if total_bytes > 0:
            pct = int(bytes_done * 100 / total_bytes)
            if bar.maximum() == 0:  # was indeterminate; switch to determinate
                bar.setRange(0, 100)
            bar.setValue(max(0, min(100, pct)))
            bar.setFormat(f"{pct}% ({self._main_dialog._human_readable(bytes_done)} / {self._main_dialog._human_readable(total_bytes)})")
        else:
            # keep indeterminate but update text with bytes downloaded
            if bar.maximum() != 0:
                bar.setRange(0, 0)
            bar.setFormat(f"{self._main_dialog._human_readable(bytes_done)} downloaded...")


    def _on_file_done(self, worker_idx, filepath, semantic_schema, srid):
        # mark file bar 100% if determinate, or switch to complete if indeterminate
        # find the bar by path -> we don't keep a reverse map, so just set text in load hook
        # (optional) you could also add a file_idx to file_done to target precisely.
        self._main_dialog.load_laz_with_schema(filepath, semantic_schema, srid)


    def _on_error(self, worker_idx, msg):
        self._statusLbl.setText(f"Error in worker {worker_idx+1}: {msg}")


    def _on_finished(self, worker_idx):
        self._finished_workers += 1
        self._statusLbl.setText(
            f"Worker {worker_idx+1} done ({self._finished_workers}/{len(self._tasks)})"
        )
        if self._finished_workers == len(self._tasks):
            self._statusLbl.setText("All downloads complete.")
