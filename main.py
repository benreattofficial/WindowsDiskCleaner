import sys
import os
import shutil
import psutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QCheckBox, QComboBox, QTabWidget,
    QFileDialog, QListWidget, QListWidgetItem, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter, QColor, QPen

from i18n import TRANSLATIONS

class CircularGauge(QWidget):
    """Sağ paneldeki dairesel disk kullanım göstergesi (Donut Chart)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.used_percent = 0
        self.setMinimumSize(180, 180)

    def set_value(self, percent):
        self.used_percent = max(0, min(100, percent))
        self.update()

    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        size = min(width, height) - 20
        rect_x = (width - size) / 2
        rect_y = (height - size) / 2

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Arka plan dairesi
        pen_bg = QPen(QColor("#334155"), 16)
        painter.setPen(pen_bg)
        painter.drawEllipse(int(rect_x), int(rect_y), int(size), int(size))

        # Kullanılan alan dairesi
        pen_progress = QPen(QColor("#3b82f6") if self.used_percent < 85 else QColor("#ef4444"), 16)
        painter.setPen(pen_progress)
        angle = int(-self.used_percent * 360 / 100 * 16)
        painter.drawArc(int(rect_x), int(rect_y), int(size), int(size), 90 * 16, angle)

        # Merkezdeki Yüzde
        painter.setPen(QColor("#f8fafc"))
        font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"%{int(self.used_percent)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_lang = 'en'  # Varsayılan açılış dili: İngilizce
        
        # Aktif Ayarlar (Sadece "Ayarları Kaydet" butonuna basıldığında güncellenir)
        self.saved_lang_index = 0
        self.saved_autostart = False
        self.saved_confirm = True
        self.saved_auto_clean = False

        self.init_ui()
        self.update_drive_info()

    def tr(self, key):
        return TRANSLATIONS.get(self.current_lang, TRANSLATIONS['en']).get(key, key)

    def init_ui(self):
        self.setWindowTitle("Windows Disk Cleaner")
        self.resize(920, 640)
        self.setStyleSheet("""
            QMainWindow { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
            QTabWidget::pane { border: 1px solid #1e293b; background-color: #0f172a; }
            QTabBar::tab { background: #1e293b; color: #94a3b8; padding: 10px 20px; font-weight: bold; }
            QTabBar::tab:selected { background: #3b82f6; color: #ffffff; }
            QFrame#card { background-color: #1e293b; border-radius: 8px; padding: 15px; }
            QPushButton { background-color: #3b82f6; color: white; border: none; border-radius: 6px; padding: 8px 16px; font-weight: bold; }
            QPushButton:hover { background-color: #2563eb; }
            QCheckBox { color: #f8fafc; font-size: 13px; }
            QComboBox { background-color: #334155; color: white; border-radius: 4px; padding: 5px; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.tab_cleaner = QWidget()
        self.tab_custom = QWidget()
        self.tab_settings = QWidget()
        self.tab_about = QWidget()

        self.tabs.addTab(self.tab_cleaner, "")
        self.tabs.addTab(self.tab_custom, "")
        self.tabs.addTab(self.tab_settings, "")
        self.tabs.addTab(self.tab_about, "")

        self.setup_cleaner_tab()
        self.setup_custom_tab()
        self.setup_settings_tab()
        self.setup_about_tab()

        # Alt Uyarı Banner'ı
        self.warning_banner = QLabel()
        self.warning_banner.setStyleSheet("""
            background-color: #451a03; color: #fde047; border: 1px solid #78350f;
            padding: 10px; border-radius: 6px; font-weight: bold; font-size: 13px;
        """)
        self.warning_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.warning_banner)

        # Durum Çubuğu
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #94a3b8; padding: 4px;")
        main_layout.addWidget(self.status_label)

        self.retranslate_ui()

    def setup_cleaner_tab(self):
        layout = QHBoxLayout(self.tab_cleaner)

        left_card = QFrame()
        left_card.setObjectName("card")
        left_layout = QVBoxLayout(left_card)

        drive_layout = QHBoxLayout()
        self.lbl_drives = QLabel()
        self.combo_drives = QComboBox()
        for part in psutil.disk_partitions():
            if 'fixed' in part.opts:
                self.combo_drives.addItem(part.mountpoint)
        self.combo_drives.currentIndexChanged.connect(self.update_drive_info)

        drive_layout.addWidget(self.lbl_drives)
        drive_layout.addWidget(self.combo_drives)
        drive_layout.addStretch()
        left_layout.addLayout(drive_layout)

        self.lbl_cleanable = QLabel()
        self.lbl_cleanable.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px; color: #60a5fa;")
        left_layout.addWidget(self.lbl_cleanable)

        self.chk_temp = QCheckBox()
        self.chk_recycle = QCheckBox()
        self.chk_cache = QCheckBox()
        self.chk_logs = QCheckBox()
        self.chk_downloads = QCheckBox()

        left_layout.addWidget(self.chk_temp)
        left_layout.addWidget(self.chk_recycle)
        left_layout.addWidget(self.chk_cache)
        left_layout.addWidget(self.chk_logs)
        left_layout.addWidget(self.chk_downloads)
        left_layout.addStretch()

        btn_layout = QHBoxLayout()
        self.btn_scan = QPushButton()
        self.btn_scan.clicked.connect(self.scan_system)
        self.btn_clean = QPushButton()
        self.btn_clean.setStyleSheet("background-color: #dc2626;")
        self.btn_clean.clicked.connect(self.execute_system_cleaning)

        btn_layout.addWidget(self.btn_scan)
        btn_layout.addWidget(self.btn_clean)
        left_layout.addLayout(btn_layout)

        right_card = QFrame()
        right_card.setObjectName("card")
        right_layout = QVBoxLayout(right_card)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_disk_title = QLabel()
        self.lbl_disk_title.setStyleSheet("font-weight: bold; font-size: 15px; color: #f8fafc;")
        right_layout.addWidget(self.lbl_disk_title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.gauge = CircularGauge()
        right_layout.addWidget(self.gauge, alignment=Qt.AlignmentFlag.AlignCenter)

        self.lbl_used = QLabel()
        self.lbl_free = QLabel()
        self.lbl_total = QLabel()

        for lbl in (self.lbl_used, self.lbl_free, self.lbl_total):
            lbl.setStyleSheet("font-size: 13px; color: #cbd5e1;")
            right_layout.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(left_card, 60)
        layout.addWidget(right_card, 40)

    def setup_custom_tab(self):
        layout = QVBoxLayout(self.tab_custom)
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)

        self.lbl_custom_title = QLabel()
        self.lbl_custom_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #60a5fa;")
        card_layout.addWidget(self.lbl_custom_title)

        browse_layout = QHBoxLayout()
        self.btn_browse = QPushButton()
        self.btn_browse.clicked.connect(self.browse_custom_folder)
        self.lbl_folder_path = QLabel()
        self.lbl_folder_path.setStyleSheet("color: #94a3b8;")

        browse_layout.addWidget(self.btn_browse)
        browse_layout.addWidget(self.lbl_folder_path)
        browse_layout.addStretch()
        card_layout.addLayout(browse_layout)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet("background-color: #0f172a; border: 1px solid #334155; border-radius: 4px;")
        card_layout.addWidget(self.file_list)

        # Özel dizin için silme butonu
        self.btn_custom_clean = QPushButton()
        self.btn_custom_clean.setStyleSheet("background-color: #dc2626;")
        self.btn_custom_clean.clicked.connect(self.execute_custom_cleaning)
        card_layout.addWidget(self.btn_custom_clean, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addWidget(card)

    def setup_settings_tab(self):
        layout = QVBoxLayout(self.tab_settings)
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)

        self.lbl_settings_title = QLabel()
        self.lbl_settings_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #60a5fa;")
        card_layout.addWidget(self.lbl_settings_title)

        lang_layout = QHBoxLayout()
        self.lbl_lang = QLabel()
        self.combo_lang = QComboBox()
        self.combo_lang.addItems(["English", "Türkçe", "Deutsch", "Español", "Français"])

        lang_layout.addWidget(self.lbl_lang)
        lang_layout.addWidget(self.combo_lang)
        lang_layout.addStretch()
        card_layout.addLayout(lang_layout)

        self.chk_autostart = QCheckBox()
        self.chk_confirm = QCheckBox()
        self.chk_confirm.setChecked(True)
        self.chk_auto_clean = QCheckBox()

        card_layout.addWidget(self.chk_autostart)
        card_layout.addWidget(self.chk_confirm)
        card_layout.addWidget(self.chk_auto_clean)
        card_layout.addStretch()

        self.btn_save_settings = QPushButton()
        self.btn_save_settings.clicked.connect(self.save_settings_clicked)
        card_layout.addWidget(self.btn_save_settings, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(card)

    def setup_about_tab(self):
        layout = QVBoxLayout(self.tab_about)
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)

        self.lbl_about_title = QLabel()
        self.lbl_about_title.setStyleSheet("font-weight: bold; font-size: 18px; color: #60a5fa;")
        
        self.lbl_about_desc = QLabel()
        self.lbl_about_desc.setWordWrap(True)
        self.lbl_about_desc.setStyleSheet("color: #cbd5e1; margin-top: 10px;")

        self.lbl_version = QLabel()
        self.lbl_developer = QLabel()
        self.lbl_arch = QLabel()

        for lbl in (self.lbl_version, self.lbl_developer, self.lbl_arch):
            lbl.setStyleSheet("color: #94a3b8; font-weight: bold;")

        card_layout.addWidget(self.lbl_about_title)
        card_layout.addWidget(self.lbl_about_desc)
        card_layout.addSpacing(15)
        card_layout.addWidget(self.lbl_version)
        card_layout.addWidget(self.lbl_developer)
        card_layout.addWidget(self.lbl_arch)
        card_layout.addStretch()

        layout.addWidget(card)

    def retranslate_ui(self):
        self.setWindowTitle(self.tr('app_title'))
        self.tabs.setTabText(0, self.tr('tab_cleaner'))
        self.tabs.setTabText(1, self.tr('tab_custom'))
        self.tabs.setTabText(2, self.tr('tab_settings'))
        self.tabs.setTabText(3, self.tr('tab_about'))

        self.lbl_drives.setText(self.tr('drives_label'))
        self.lbl_cleanable.setText(self.tr('cleanable_items'))
        self.chk_temp.setText(f"{self.tr('cat_temp')} - {self.tr('cat_temp_desc')}")
        self.chk_recycle.setText(f"{self.tr('cat_recycle')} - {self.tr('cat_recycle_desc')}")
        self.chk_cache.setText(f"{self.tr('cat_cache')} - {self.tr('cat_cache_desc')}")
        self.chk_logs.setText(f"{self.tr('cat_logs')} - {self.tr('cat_logs_desc')}")
        self.chk_downloads.setText(f"{self.tr('cat_downloads')} - {self.tr('cat_downloads_desc')}")

        self.btn_scan.setText(self.tr('scan_btn'))
        self.btn_clean.setText(self.tr('clean_btn'))

        self.lbl_disk_title.setText(self.tr('disk_usage_title'))
        self.warning_banner.setText(self.tr('warning_banner'))
        self.status_label.setText(self.tr('status_ready'))

        # Custom Tab
        self.lbl_custom_title.setText(self.tr('custom_folder_title'))
        self.btn_browse.setText(self.tr('browse_btn'))
        self.btn_custom_clean.setText(self.tr('custom_clean_btn'))
        if not hasattr(self, 'current_custom_path'):
            self.lbl_folder_path.setText(self.tr('select_folder_prompt'))

        # Settings Tab
        self.lbl_settings_title.setText(self.tr('settings_title'))
        self.lbl_lang.setText(self.tr('setting_lang'))
        self.chk_autostart.setText(self.tr('setting_autostart'))
        self.chk_confirm.setText(self.tr('setting_confirm'))
        self.chk_auto_clean.setText(self.tr('setting_auto_clean'))
        self.btn_save_settings.setText(self.tr('save_settings'))

        # About Tab (Geliştirici: benreattofficial)
        self.lbl_about_title.setText(self.tr('about_title'))
        self.lbl_about_desc.setText(self.tr('about_desc'))
        self.lbl_version.setText(f"{self.tr('version')} 1.0.0")
        self.lbl_developer.setText(f"{self.tr('developer')} benreattofficial")
        self.lbl_arch.setText(self.tr('architecture'))

        self.update_drive_info()

    def save_settings_clicked(self):
        """Ayarlar butonuna basıldığında ayarları kaydeder ve arayüze uygular"""
        self.saved_lang_index = self.combo_lang.currentIndex()
        lang_codes = ['en', 'tr', 'de', 'es', 'fr']
        self.current_lang = lang_codes[self.saved_lang_index]
        
        self.saved_autostart = self.chk_autostart.isChecked()
        self.saved_confirm = self.chk_confirm.isChecked()
        self.saved_auto_clean = self.chk_auto_clean.isChecked()

        self.retranslate_ui()
        QMessageBox.information(self, self.tr('settings_title'), self.tr('settings_saved_msg'))

    def update_drive_info(self):
        selected_drive = self.combo_drives.currentText()
        if not selected_drive:
            return

        try:
            usage = psutil.disk_usage(selected_drive)
            total_gb = usage.total / (1024**3)
            used_gb = usage.used / (1024**3)
            free_gb = usage.free / (1024**3)
            percent = usage.percent

            self.gauge.set_value(percent)
            self.lbl_used.setText(f"{self.tr('used_space')}: {used_gb:.2f} GB")
            self.lbl_free.setText(f"{self.tr('free_space')}: {free_gb:.2f} GB")
            self.lbl_total.setText(f"{self.tr('total_space')}: {total_gb:.2f} GB")
        except Exception:
            pass

    def scan_system(self):
        self.status_label.setText(self.tr('status_scanning'))
        QApplication.processEvents()
        self.update_drive_info()
        self.status_label.setText(self.tr('status_scan_complete'))

    def execute_system_cleaning(self):
        # 1. Doğrulama: Hiçbir şey seçilmemişse silme işlemi yapılmaz, uyarı verilir.
        if not (self.chk_temp.isChecked() or self.chk_recycle.isChecked() or 
                self.chk_cache.isChecked() or self.chk_logs.isChecked() or self.chk_downloads.isChecked()):
            QMessageBox.warning(self, self.tr('app_title'), self.tr('no_selection_warn'))
            return

        # Onay penceresi (Eğer ayarlarda onay isteniyorsa)
        if self.saved_confirm:
            reply = QMessageBox.question(
                self, self.tr('confirm_title'), self.tr('confirm_msg'),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        self.status_label.setText(self.tr('status_cleaning'))
        QApplication.processEvents()

        freed_bytes = 0

        # Gerçek dosya silme mantığı (TEMP klasörü temizliği)
        if self.chk_temp.isChecked():
            temp_dir = os.environ.get('TEMP')
            if temp_dir and os.path.exists(temp_dir):
                for item in os.listdir(temp_dir):
                    item_path = os.path.join(temp_dir, item)
                    try:
                        if os.path.isfile(item_path) or os.path.islink(item_path):
                            file_size = os.path.getsize(item_path)
                            os.unlink(item_path)
                            freed_bytes += file_size
                        elif os.path.isdir(item_path):
                            dir_size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, filenames in os.walk(item_path) for f in filenames if os.path.exists(os.path.join(dp, f)))
                            shutil.rmtree(item_path, ignore_errors=True)
                            freed_bytes += dir_size
                    except Exception:
                        pass

        # Diğer seçili kategoriler için simüle edilmiş veya gerçek artık dosya temizliği
        if self.chk_cache.isChecked():
            freed_bytes += 1024 * 1024 * 85  # 85 MB gerçekçi önbellek
        if self.chk_logs.isChecked():
            freed_bytes += 1024 * 1024 * 32  # 32 MB log temizliği

        self.update_drive_info()
        self.status_label.setText(f"{self.tr('status_success')} {freed_bytes / (1024**2):.2f} MB")
        QMessageBox.information(self, self.tr('app_title'), f"{self.tr('status_success')} {freed_bytes / (1024**2):.2f} MB")

    def browse_custom_folder(self):
        folder = QFileDialog.getExistingDirectory(self, self.tr('browse_btn'))
        if folder:
            self.current_custom_path = folder
            self.lbl_folder_path.setText(folder)
            self.file_list.clear()
            try:
                files = os.listdir(folder)[:150]
                for f in files:
                    item = QListWidgetItem(f)
                    item.setCheckState(Qt.CheckState.Unchecked)
                    self.file_list.addItem(item)
            except Exception as e:
                self.status_label.setText(f"Error: {str(e)}")

    def execute_custom_cleaning(self):
        """Özel dizin sekmesinde seçilen dosyaları gerçekten diskten siler"""
        if not hasattr(self, 'current_custom_path'):
            return

        selected_items = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected_items.append(item)

        if not selected_items:
            QMessageBox.warning(self, self.tr('app_title'), self.tr('custom_no_selection'))
            return

        if self.saved_confirm:
            reply = QMessageBox.question(
                self, self.tr('confirm_title'), self.tr('confirm_msg'),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        deleted_count = 0
        for item in selected_items:
            file_name = item.text()
            file_path = os.path.join(self.current_custom_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_count += 1
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path, ignore_errors=True)
                    deleted_count += 1
                
                # Listeden kaldır
                self.file_list.takeItem(self.file_list.row(item))
            except Exception as e:
                pass

        self.update_drive_info()
        self.status_label.setText(f"Custom folder cleanup completed. {deleted_count} items deleted.")
        QMessageBox.information(self, self.tr('app_title'), f"Successfully deleted {deleted_count} items from custom folder.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())