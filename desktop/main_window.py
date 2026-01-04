from pathlib import Path
import sys
import logging
import traceback
from typing import Type, Any, List, Dict
from contextlib import contextmanager

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QListWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QFormLayout, QMessageBox, QHeaderView, QDialog, QDialogButtonBox
)
from PyQt5.QtCore import Qt, pyqtSlot, QRunnable, QThreadPool, pyqtSignal, QObject

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# --- Project Base Path ---
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

# --- Import Database ---
from kskapp.database.session import engine, SessionLocal
from kskapp.database.base import Base

# --- Import Models ---
from kskapp.models.models import (
    Object, Material, Organization, LineType, Contractor, Document, FieldData
)

# --- Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("ksk-main")

# --- Worker for Async ---
class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.result.emit(result)
        except Exception:
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()

# --- Repository ---
class GenericRepository:
    def __init__(self, session_factory=sessionmaker(bind=engine)):
        self.session_factory = session_factory

    @contextmanager
    def session_scope(self):
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"DB Error: {e}")
            raise
        finally:
            session.close()

    def get_all(self, model: Type[Base]) -> List[Any]:
        with self.session_scope() as session:
            items = session.query(model).all()
            session.expunge_all()
            return items

    def save(self, item: Base):
        with self.session_scope() as session:
            session.add(item)

    def update(self, model: Type[Base], item_id: int, updates: Dict[str, Any]):
        with self.session_scope() as session:
            obj = session.query(model).get(item_id)
            if obj:
                for key, value in updates.items():
                    setattr(obj, key, value)

    def delete(self, model: Type[Base], item_id: int):
        with self.session_scope() as session:
            obj = session.query(model).get(item_id)
            if obj:
                session.delete(obj)

# --- Base Tab ---
class BaseTab(QWidget):
    def __init__(self, title: str):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.threadpool = QThreadPool()
        if title:
            header = QLabel(title)
            header.setAlignment(Qt.AlignCenter)
            header.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
            self.layout.addWidget(header)

    def show_error(self, err_tuple):
        msg = f"Error: {err_tuple[1]}"
        QMessageBox.critical(self, "System Error", msg)
        logger.error(msg)

    def execute_async(self, func, callback=None):
        worker = Worker(func)
        if callback:
            worker.signals.result.connect(callback)
        worker.signals.error.connect(self.show_error)
        self.threadpool.start(worker)

# --- CRUD Table Widget ---
class CrudTableWidget(BaseTab):
    def __init__(self, title: str, headers: List[str], repository: GenericRepository, model_class: Type[Base]):
        super().__init__(title)
        self.headers = headers
        self.repo = repository
        self.model_class = model_class
        self.data_items = []

        # Filter input
        filter_layout = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Search...")
        self.filter_input.textChanged.connect(self.apply_filter)
        filter_layout.addWidget(QLabel("Filter:"))
        filter_layout.addWidget(self.filter_input)
        self.layout.addLayout(filter_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        # Actions layout
        self.actions_layout = QHBoxLayout()
        self.layout.addLayout(self.actions_layout)

        self.refresh_data()

    def add_action_button(self, text: str, callback):
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        self.actions_layout.addWidget(btn)

    def refresh_data(self):
        self.table.setEnabled(False)
        self.execute_async(lambda: self.repo.get_all(self.model_class), self.on_data_loaded)

    def on_data_loaded(self, items):
        self.table.setEnabled(True)
        self.data_items = items
        self.populate_table(items)
        self.apply_filter()

    def populate_table(self, items):
        self.table.setRowCount(len(items))
        for i, item in enumerate(items):
            self.fill_row(i, item)
            self.create_row_buttons(i, item.id)

    def fill_row(self, row_idx, item):
        pass  # Override in subclasses

    def create_row_buttons(self, row_index, item_id):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2,2,2,2)

        btn_edit = QPushButton("Edit")
        btn_edit.clicked.connect(lambda _, oid=item_id: self.edit_item(oid))
        btn_del = QPushButton("Delete")
        btn_del.clicked.connect(lambda _, oid=item_id: self.delete_item(oid))

        layout.addWidget(btn_edit)
        layout.addWidget(btn_del)
        self.table.setCellWidget(row_index, len(self.headers)-1, widget)

    def apply_filter(self):
        text = self.filter_input.text().lower()
        for row in range(self.table.rowCount()):
            visible = False
            for col in range(self.table.columnCount()-1):  # exclude Actions
                item = self.table.item(row, col)
                if item and text in item.text().lower():
                    visible = True
                    break
            self.table.setRowHidden(row, not visible)

    def delete_item(self, item_id):
        if QMessageBox.question(self, "Confirm", "Delete this item?") == QMessageBox.Yes:
            self.execute_async(lambda: self.repo.delete(self.model_class, item_id), lambda _: self.refresh_data())

    def edit_item(self, item_id):
        pass  # Override in subclasses

# --- Generic Dialog Mixin ---
class DialogMixin:
    def open_dialog(self, item_id=None, fields=None, title="Edit Item"):
        dialog = QDialog(self)
        dialog.setWindowTitle(title if item_id else f"New {title}")
        layout = QFormLayout(dialog)
        edits = {}
        for field in fields:
            edit = QLineEdit()
            edits[field] = edit
            layout.addRow(field.capitalize(), edit)

        # Pre-fill if editing
        if item_id:
            obj = next((x for x in self.data_items if x.id==item_id), None)
            if obj:
                for field in fields:
                    edits[field].setText(str(getattr(obj, field, "")))

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(dialog.accept)
        btns.rejected.connect(dialog.reject)
        layout.addRow(btns)

        if dialog.exec_() == QDialog.Accepted:
            data = {field: edits[field].text() for field in fields}
            if item_id:
                self.execute_async(lambda: self.repo.update(self.model_class, item_id, data), lambda _: self.refresh_data())
            else:
                self.execute_async(lambda: self.repo.save(self.model_class(**data)), lambda _: self.refresh_data())

# --- Implement Tabs ---
class ObjectsTab(CrudTableWidget, DialogMixin):
    def __init__(self, repo):
        super().__init__("Objects", ["ID", "Name", "Location", "Actions"], repo, Object)
        self.add_action_button("Add Object", self.add_object)

    def fill_row(self, row_idx, obj):
        self.table.setItem(row_idx, 0, QTableWidgetItem(str(obj.id)))
        self.table.setItem(row_idx, 1, QTableWidgetItem(obj.name))
        self.table.setItem(row_idx, 2, QTableWidgetItem(obj.location))

    def add_object(self):
        self.open_dialog(fields=["name","location"], title="Object")

    def edit_item(self, item_id):
        self.open_dialog(item_id=item_id, fields=["name","location"], title="Object")

# --- MaterialsTab ---
class MaterialsTab(CrudTableWidget, DialogMixin):
    def __init__(self, repo):
        super().__init__("Materials", ["ID","Name","Unit","Norm","Stock","Actions"], repo, Material)
        self.add_action_button("Add Material", self.add_material)

    def fill_row(self, row_idx, mat):
        self.table.setItem(row_idx, 0, QTableWidgetItem(str(mat.id)))
        self.table.setItem(row_idx, 1, QTableWidgetItem(mat.name))
        self.table.setItem(row_idx, 2, QTableWidgetItem(mat.unit))
        self.table.setItem(row_idx, 3, QTableWidgetItem(str(mat.norm)))
        self.table.setItem(row_idx, 4, QTableWidgetItem(str(mat.current_stock)))

    def add_material(self):
        self.open_dialog(fields=["name","unit","norm","current_stock"], title="Material")

    def edit_item(self, item_id):
        self.open_dialog(item_id=item_id, fields=["name","unit","norm","current_stock"], title="Material")

# --- OrganizationsTab ---
class OrganizationsTab(CrudTableWidget, DialogMixin):
    def __init__(self, repo):
        super().__init__("Organizations", ["ID","Name","Address","Actions"], repo, Organization)
        self.add_action_button("Add Organization", self.add_org)

    def fill_row(self, row_idx, org):
        self.table.setItem(row_idx, 0, QTableWidgetItem(str(org.id)))
        self.table.setItem(row_idx, 1, QTableWidgetItem(org.name))
        self.table.setItem(row_idx, 2, QTableWidgetItem(org.address))

    def add_org(self):
        self.open_dialog(fields=["name","address"], title="Organization")

    def edit_item(self, item_id):
        self.open_dialog(item_id=item_id, fields=["name","address"], title="Organization")

# --- LineTypesTab ---
class LineTypesTab(CrudTableWidget, DialogMixin):
    def __init__(self, repo):
        super().__init__("LineTypes", ["ID","Name","Width","MaterialID","Actions"], repo, LineType)
        self.add_action_button("Add LineType", self.add_line)

    def fill_row(self, row_idx, line):
        self.table.setItem(row_idx, 0, QTableWidgetItem(str(line.id)))
        self.table.setItem(row_idx, 1, QTableWidgetItem(line.name))
        self.table.setItem(row_idx, 2, QTableWidgetItem(str(line.width)))
        self.table.setItem(row_idx, 3, QTableWidgetItem(str(line.material_id)))

    def add_line(self):
        self.open_dialog(fields=["name","width","material_id"], title="LineType")

    def edit_item(self, item_id):
        self.open_dialog(item_id=item_id, fields=["name","width","material_id"], title="LineType")

# --- ContractorsTab ---
class ContractorsTab(CrudTableWidget, DialogMixin):
    def __init__(self, repo):
        super().__init__("Contractors", ["ID","Name","INN","Actions"], repo, Contractor)
        self.add_action_button("Add Contractor", self.add_contractor)

    def fill_row(self, row_idx, con):
        self.table.setItem(row_idx, 0, QTableWidgetItem(str(con.id)))
        self.table.setItem(row_idx, 1, QTableWidgetItem(con.name))
        self.table.setItem(row_idx, 2, QTableWidgetItem(con.inn))

    def add_contractor(self):
        self.open_dialog(fields=["name","inn"], title="Contractor")

    def edit_item(self, item_id):
        self.open_dialog(item_id=item_id, fields=["name","inn"], title="Contractor")

# --- DocumentsTab ---
class DocumentsTab(CrudTableWidget, DialogMixin):
    def __init__(self, repo):
        super().__init__("Documents", ["ID","ObjectID","Type","Path","Created","Actions"], repo, Document)
        self.add_action_button("Add Document", self.add_doc)

    def fill_row(self, row_idx, doc):
        self.table.setItem(row_idx, 0, QTableWidgetItem(str(doc.id)))
        self.table.setItem(row_idx, 1, QTableWidgetItem(str(doc.object_id)))
        self.table.setItem(row_idx, 2, QTableWidgetItem(doc.type))
        self.table.setItem(row_idx, 3, QTableWidgetItem(doc.path))
        self.table.setItem(row_idx, 4, QTableWidgetItem(str(doc.created)))

    def add_doc(self):
        self.open_dialog(fields=["object_id","type","path","created"], title="Document")

    def edit_item(self, item_id):
        self.open_dialog(item_id=item_id, fields=["object_id","type","path","created"], title="Document")

# --- FieldDataTab ---
class FieldDataTab(CrudTableWidget, DialogMixin):
    def __init__(self, repo):
        super().__init__("FieldData", ["ID","ObjectID","LineTypeID","Length","Width","MaterialUsed","Date","Notes","Actions"], repo, FieldData)
        self.add_action_button("Add FieldData", self.add_field)

    def fill_row(self, row_idx, fd):
        self.table.setItem(row_idx, 0, QTableWidgetItem(str(fd.id)))
        self.table.setItem(row_idx, 1, QTableWidgetItem(str(fd.object_id)))
        self.table.setItem(row_idx, 2, QTableWidgetItem(str(fd.line_type_id)))
        self.table.setItem(row_idx, 3, QTableWidgetItem(str(fd.length)))
        self.table.setItem(row_idx, 4, QTableWidgetItem(str(fd.width)))
        self.table.setItem(row_idx, 5, QTableWidgetItem(fd.material_used))
        self.table.setItem(row_idx, 6, QTableWidgetItem(str(fd.date)))
        self.table.setItem(row_idx, 7, QTableWidgetItem(fd.notes))

    def add_field(self):
        self.open_dialog(fields=["object_id","line_type_id","length","width","material_used","date","notes"], title="FieldData")

    def edit_item(self, item_id):
        self.open_dialog(item_id=item_id, fields=["object_id","line_type_id","length","width","material_used","date","notes"], title="FieldData")

# --- ChartTab ---
class ChartTab(BaseTab):
    def __init__(self, repo):
        super().__init__("Analytics")
        self.repo = repo
        self.figure = Figure(figsize=(6,4))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        btn = QPushButton("Refresh Chart")
        btn.clicked.connect(self.update_plot)
        self.layout.addWidget(btn)

    def update_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        try:
            data = self.repo.get_all(FieldData)
            lengths = [fd.length for fd in data]
            ax.plot(range(len(lengths)), lengths, marker='o')
            ax.set_title("Field Data Lengths")
            ax.set_xlabel("Entry")
            ax.set_ylabel("Length")
        except Exception as e:
            logger.error(f"Chart Error: {e}")
        self.canvas.draw()

# --- MainWindow ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KSK Shop")
        self.resize(1200,700)

        self.repo = GenericRepository(SessionLocal)

        main_layout = QHBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.nav_list = QListWidget()
        self.nav_list.setFixedWidth(200)
        self.nav_list.currentRowChanged.connect(self.switch_page)
        main_layout.addWidget(self.nav_list)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        self.pages = {}
        self.setup_pages()

    def setup_pages(self):
        self.pages = {
            "Objects": ObjectsTab(self.repo),
            "Materials": MaterialsTab(self.repo),
            "Organizations": OrganizationsTab(self.repo),
            "LineTypes": LineTypesTab(self.repo),
            "Contractors": ContractorsTab(self.repo),
            "Documents": DocumentsTab(self.repo),
            "FieldData": FieldDataTab(self.repo),
            "Charts": ChartTab(self.repo)
        }

        for name, widget in self.pages.items():
            self.nav_list.addItem(name)
            self.stacked_widget.addWidget(widget)

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
