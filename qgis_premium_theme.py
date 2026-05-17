import os
import tempfile
from qgis.PyQt.QtCore import QObject, QEvent, Qt, QPoint, QTimer, QSize
from qgis.PyQt.QtGui import QPalette, QColor, QPainter, QPen, QBrush, QPolygon, QIcon, QImage
from qgis.PyQt.QtWidgets import (
    QApplication, QWidget, QListWidget, QListView, QAbstractItemView,
    QProxyStyle, QStyle, QSplitter, QTreeWidget, QTreeView, QSizePolicy,
    QStackedWidget
)
try:
    from qgis.utils import iface
except Exception:
    iface = None

# =========================
# COLOR PALETTE
# =========================
# Accent (brand green)
ACCENT                 = "#6b8c42"
ACCENT_HOVER           = "#7a9e4c"
ACCENT_PRESSED         = "#5c7a38"
ACCENT_CHECKED_BORDER  = "#5a7a3a"
ACCENT_DISABLED        = "#4a5a3a"
ACCENT_INDETERMINATE   = "#4a6635"
ACCENT_TRANSLUCENT     = "rgba(107, 140, 66, 0.15)"

# Backgrounds
BG_WINDOW              = "#2b2b2b"
BG_BASE                = "#232323"
BG_ALT                 = "#262626"
BG_DOCK                = "#282828"
BG_STATUSBAR           = "#242424"
BG_MENU                = "#2d2d2d"
BG_DISABLED            = "#2e2e2e"
BG_BTN_STATUS_HOVER    = "#2f2f2f"
BG_PRESSED             = "#2c2c2c"
BG_HOVER               = "#303030"
BG_HOVER_RAISED        = "#383838"
BG_INDICATOR           = "#252525"
BG_BTN_HOVER           = "#404040"
BG_SELECTED            = "#3a4a30"
BG_SELECTED_ACTIVE     = "#44582f"
BG_SELECTED_INACTIVE   = "#353535"
BG_PLUGIN_INACTIVE     = "#3f4a35"
BG_PLUGIN_SEL_HOVER    = "#4f6638"

# Borders / separators
BORDER                 = "#3a3a3a"
BORDER_SUBTLE          = "#1f1f1f"
BORDER_DARKER          = "#1c1c1c"
BORDER_DIM             = "#333333"
BORDER_BTN             = "#3f3f3f"
BORDER_HOVER           = "#484848"
BORDER_INDICATOR       = "#4a4a4a"
BORDER_LIST_ITEM       = "#2a2a2a"
SEPARATOR_BG           = "#222222"

# Text
TEXT                   = "#e8e8e8"
TEXT_BRIGHT            = "#ffffff"
TEXT_DIM               = "#b0b0b0"
TEXT_DISABLED          = "#6a6a6a"
TEXT_LIGHT             = "#d8d8d8"
TEXT_HEADER            = "#d0d0d0"
TEXT_PLACEHOLDER       = "#787878"
TEXT_DARK              = "#1a1a1a"
CHECKMARK              = "#ffffff"

# Arrow icons
ARROW_NORMAL           = "#c8c8c8"
ARROW_DISABLED         = "#5a5a5a"

# Scrollbar
SCROLLBAR_HANDLE_HOVER = "#525252"

# Named colour keyword
TRANSPARENT            = "transparent"

QSS = rf"""
* {{ outline: 0; color: {TEXT}; selection-background-color: {ACCENT}; selection-color: {TEXT_DARK}; }}
QWidget {{ background-color: {BG_WINDOW}; color: {TEXT}; font-family: "Segoe UI", "Inter", "Noto Sans", sans-serif; font-size: 9pt; border: none; }}
QWidget:disabled {{ color: {TEXT_DISABLED}; background-color: {BG_WINDOW}; }}
QToolTip {{ background-color: {BORDER_SUBTLE}; color: {TEXT}; border: 1px solid {BORDER}; padding: 4px 7px; border-radius: 3px; }}
QMainWindow {{ background-color: {BG_WINDOW}; color: {TEXT}; }}
QMainWindow::separator {{ background-color: {SEPARATOR_BG}; width: 1px; height: 1px; }}
QMainWindow::separator:hover {{ background-color: {ACCENT}; }}
QDialog {{ background-color: {BG_WINDOW}; color: {TEXT}; }}
QStatusBar {{ background-color: {BG_STATUSBAR}; color: {TEXT_DIM}; border-top: 1px solid {BORDER_DARKER}; min-height: 32px; padding: 6px 6px 2px 6px; }}
QStatusBar::item {{ border: 0; padding: 0; }}
QStatusBar QLabel {{ background: {TRANSPARENT}; color: {TEXT_DIM}; padding: 0 4px; min-height: 22px; }}
QStatusBar QToolButton, QStatusBar QPushButton {{ padding: 3px 10px; margin: 1px; min-height: 22px; min-width: 0; border-radius: 3px; }}
QStatusBar QToolButton:hover, QStatusBar QPushButton:hover {{ background-color: {BG_BTN_STATUS_HOVER}; border-color: {BORDER}; }}
QStatusBar QLineEdit, QStatusBar QComboBox {{ padding: 2px 6px; margin: 1px; min-height: 20px; }}
QSizeGrip {{ background: {TRANSPARENT}; width: 14px; height: 14px; }}
QDockWidget {{ background-color: {BG_DOCK}; color: {TEXT}; titlebar-close-icon: none; titlebar-normal-icon: none; border: 1px solid {BORDER_SUBTLE}; }}
QDockWidget::title {{ background-color: {BG_STATUSBAR}; color: {TEXT_LIGHT}; padding: 5px 8px; border-bottom: 1px solid {BORDER_DARKER}; text-align: left; font-weight: 600; }}
QDockWidget::close-button, QDockWidget::float-button {{ background: {TRANSPARENT}; border: 0; padding: 2px; border-radius: 3px; }}
QDockWidget::close-button:hover, QDockWidget::float-button:hover {{ background-color: {BG_HOVER_RAISED}; }}
QToolBar {{ background-color: {BG_WINDOW}; border: none; border-bottom: 1px solid {BORDER_SUBTLE}; spacing: 2px; padding: 3px 4px; }}
QToolBar::separator {{ background-color: {BORDER}; width: 1px; margin: 4px 4px; }}
QMenuBar {{ background-color: {BG_WINDOW}; color: {TEXT}; border-bottom: 1px solid {BORDER_SUBTLE}; padding: 3px 6px; font-size: 10pt; }}
QMenuBar::item {{ background: {TRANSPARENT}; padding: 7px 14px; margin: 0 1px; border-radius: 4px; }}
QMenuBar::item:selected {{ background-color: {BG_HOVER_RAISED}; color: {TEXT_BRIGHT}; }}
QMenuBar::item:pressed  {{ background-color: {BG_SELECTED_ACTIVE}; color: {TEXT_BRIGHT}; }}
QMenu {{ background-color: {BG_MENU}; color: {TEXT}; border: 1px solid {BORDER}; border-radius: 5px; padding: 4px 3px; }}
QMenu::item {{ background: {TRANSPARENT}; padding: 5px 26px 5px 22px; border-radius: 3px; margin: 1px 2px; }}
QMenu::item:selected {{ background-color: {BG_HOVER_RAISED}; color: {TEXT_BRIGHT}; }}
QMenu::separator {{ height: 1px; background-color: {BORDER}; margin: 4px 8px; }}
QPushButton {{ background-color: {BG_SELECTED_INACTIVE}; color: {TEXT}; border: 1px solid {BORDER_BTN}; border-radius: 4px; padding: 5px 14px; min-height: 18px; min-width: 64px; }}
QPushButton:hover {{ background-color: {BG_BTN_HOVER}; border-color: {BORDER_INDICATOR}; }}
QPushButton:pressed {{ background-color: {BG_PRESSED}; border-color: {BORDER}; }}
QPushButton:checked {{ background-color: {BORDER_INDICATOR}; border-color: {ACCENT}; color: {TEXT_BRIGHT}; }}
QPushButton:focus {{ border-color: {ACCENT}; }}
QPushButton:default {{ background-color: {ACCENT}; color: {TEXT_DARK}; border: 1px solid {ACCENT_PRESSED}; font-weight: 600; }}
QPushButton:default:hover {{ background-color: {ACCENT_HOVER}; border-color: {ACCENT}; }}
QPushButton:disabled {{ background-color: {BG_DISABLED}; color: {TEXT_DISABLED}; border-color: {BG_SELECTED_INACTIVE}; }}
QToolButton {{ background: {TRANSPARENT}; color: {TEXT}; border: 1px solid {TRANSPARENT}; border-radius: 4px; padding: 3px; margin: 1px; }}
QToolButton[popupMode="1"], QToolButton[popupMode="2"] {{ padding-right: 14px; }}
QToolButton[popupMode="1"] {{ padding-right: 18px; }}
QToolButton::menu-indicator {{ subcontrol-origin: padding; subcontrol-position: bottom right; right: 2px; bottom: 2px; }}
QToolButton::menu-button {{ border-left: 1px solid {BORDER}; border-top-right-radius: 4px; border-bottom-right-radius: 4px; width: 14px; }}
QToolButton:hover {{ background-color: {BG_HOVER_RAISED}; border-color: {BORDER_BTN}; }}
QToolButton:pressed {{ background-color: {BG_PRESSED}; }}
QToolButton:checked {{ background-color: {BG_SELECTED}; border-color: {ACCENT_CHECKED_BORDER}; }}
QToolButton:checked:hover {{ background-color: {BG_SELECTED_ACTIVE}; border-color: {ACCENT_PRESSED}; }}
QLineEdit, QTextEdit, QPlainTextEdit {{ background-color: {BG_BASE}; color: {TEXT}; border: 1px solid {BORDER}; border-radius: 4px; padding: 4px 7px; selection-background-color: {ACCENT}; selection-color: {TEXT_DARK}; }}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{ border-color: {ACCENT}; background-color: {BG_ALT}; }}
QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {{ background-color: {BG_ALT}; color: {TEXT_DISABLED}; border-color: {BORDER_DIM}; }}
QSpinBox, QDoubleSpinBox, QDateEdit, QDateTimeEdit, QTimeEdit, QgsSpinBox, QgsDoubleSpinBox {{ background-color: {BG_BASE}; color: {TEXT}; border: 1px solid {BORDER}; border-radius: 4px; padding: 3px 6px; padding-right: 22px; min-height: 20px; min-width: 60px; selection-background-color: {ACCENT}; selection-color: {TEXT_DARK}; }}
QSpinBox:focus, QDoubleSpinBox:focus, QgsSpinBox:focus, QgsDoubleSpinBox:focus {{ border-color: {ACCENT}; background-color: {BG_ALT}; }}
QSpinBox::up-button, QDoubleSpinBox::up-button, QDateEdit::up-button, QDateTimeEdit::up-button, QTimeEdit::up-button, QgsSpinBox::up-button, QgsDoubleSpinBox::up-button {{ subcontrol-origin: border; subcontrol-position: top right; width: 18px; background-color: {BG_MENU}; border: none; border-left: 1px solid {BORDER}; border-top-right-radius: 3px; }}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover, QgsSpinBox::up-button:hover, QgsDoubleSpinBox::up-button:hover {{ background-color: {BG_SELECTED_ACTIVE}; }}
QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed, QgsSpinBox::up-button:pressed, QgsDoubleSpinBox::up-button:pressed {{ background-color: {ACCENT_PRESSED}; }}
QSpinBox::down-button, QDoubleSpinBox::down-button, QDateEdit::down-button, QDateTimeEdit::down-button, QTimeEdit::down-button, QgsSpinBox::down-button, QgsDoubleSpinBox::down-button {{ subcontrol-origin: border; subcontrol-position: bottom right; width: 18px; background-color: {BG_MENU}; border: none; border-left: 1px solid {BORDER}; border-bottom-right-radius: 3px; }}
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover, QgsSpinBox::down-button:hover, QgsDoubleSpinBox::down-button:hover {{ background-color: {BG_SELECTED_ACTIVE}; }}
QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed, QgsSpinBox::down-button:pressed, QgsDoubleSpinBox::down-button:pressed {{ background-color: {ACCENT_PRESSED}; }}
QComboBox {{ background-color: {BG_BASE}; color: {TEXT}; border: 1px solid {BORDER}; border-radius: 4px; padding: 3px 8px; min-height: 18px; min-width: 60px; selection-background-color: {ACCENT}; selection-color: {TEXT_DARK}; }}
QComboBox:hover {{ border-color: {BORDER_HOVER}; background-color: {BG_ALT}; }}
QComboBox:focus, QComboBox:on {{ border-color: {ACCENT}; background-color: {BG_ALT}; }}
QComboBox:disabled {{ background-color: {BG_ALT}; color: {TEXT_DISABLED}; border-color: {BORDER_DIM}; }}
QComboBox QAbstractItemView {{ background-color: {BG_MENU}; color: {TEXT}; border: 1px solid {BORDER}; border-radius: 4px; padding: 3px; selection-background-color: {BG_SELECTED}; selection-color: {TEXT_BRIGHT}; outline: 0; }}
QComboBox QAbstractItemView::item {{ padding: 5px 8px; border-radius: 3px; min-height: 18px; }}
QComboBox QAbstractItemView::item:hover {{ background-color: {BG_HOVER_RAISED}; color: {TEXT_BRIGHT}; }}
QComboBox QAbstractItemView::item:selected {{ background-color: {BG_SELECTED}; color: {TEXT_BRIGHT}; }}
QComboBox::drop-down {{ border: none; width: 20px; }}
QComboBox::drop-down:hover {{ background-color: {BG_HOVER_RAISED}; }}
QListView, QListWidget, QTreeView, QTreeWidget {{ background-color: {BG_BASE}; color: {TEXT}; border: 1px solid {BORDER_DIM}; border-radius: 4px; alternate-background-color: {BG_ALT}; selection-background-color: {BG_SELECTED}; selection-color: {TEXT_BRIGHT}; outline: none; show-decoration-selected: 1; }}
QListView::item, QListWidget::item, QTreeView::item, QTreeWidget::item {{ padding: 3px 6px; border: none; color: {TEXT}; }}
QListView::item:hover, QListWidget::item:hover, QTreeView::item:hover, QTreeWidget::item:hover {{ background-color: {BG_HOVER}; color: {TEXT_BRIGHT}; }}
QListView::item:selected, QListWidget::item:selected, QTreeView::item:selected, QTreeWidget::item:selected {{ background-color: {BG_SELECTED}; color: {TEXT_BRIGHT}; }}
QListView::item:selected:active, QListWidget::item:selected:active, QTreeView::item:selected:active, QTreeWidget::item:selected:active {{ background-color: {BG_SELECTED_ACTIVE}; color: {TEXT_BRIGHT}; }}
QListView::item:selected:!active, QListWidget::item:selected:!active, QTreeView::item:selected:!active, QTreeWidget::item:selected:!active {{ background-color: {BG_SELECTED_INACTIVE}; color: {TEXT}; }}
QListView#vwPlugins, QListWidget#vwPlugins, QListView#mListPlugins, QListWidget#mListPlugins {{ background-color: {ACCENT_HOVER}; color: {TEXT}; border: 1px solid {BORDER_SUBTLE}; border-radius: 4px; alternate-background-color: {ACCENT_HOVER}; selection-background-color: {ACCENT_HOVER}; selection-color: {TEXT_BRIGHT}; outline: 0; show-decoration-selected: 1; padding: 2px; }}
QListView#vwPlugins::item, QListWidget#vwPlugins::item, QListView#mListPlugins::item, QListWidget#mListPlugins::item {{ background-color: {ACCENT_HOVER}; color: {TEXT}; padding: 8px 10px; border: none; border-bottom: 1px solid {BORDER_LIST_ITEM}; min-height: 32px; margin: 0; }}
QListView#vwPlugins::item:hover, QListWidget#vwPlugins::item:hover, QListView#mListPlugins::item:hover, QListWidget#mListPlugins::item:hover {{ background-color: {ACCENT_HOVER}; color: {TEXT_BRIGHT}; }}
QListView#vwPlugins::item:selected, QListWidget#vwPlugins::item:selected, QListView#mListPlugins::item:selected, QListWidget#mListPlugins::item:selected, QListView#vwPlugins::item:selected:active, QListWidget#vwPlugins::item:selected:active, QListView#mListPlugins::item:selected:active, QListWidget#mListPlugins::item:selected:active {{ background-color: {ACCENT_HOVER}; color: {TEXT_BRIGHT}; }}
QListView#vwPlugins::item:selected:hover, QListWidget#vwPlugins::item:selected:hover, QListView#mListPlugins::item:selected:hover, QListWidget#mListPlugins::item:selected:hover {{ background-color: {ACCENT_HOVER}; color: {TEXT_BRIGHT}; }}
QListView#vwPlugins::item:selected:!active, QListWidget#vwPlugins::item:selected:!active, QListView#mListPlugins::item:selected:!active, QListWidget#mListPlugins::item:selected:!active {{ background-color: {ACCENT_HOVER}; color: {TEXT}; }}
QListView#vwPlugins::item:focus, QListWidget#vwPlugins::item:focus, QListView#mListPlugins::item:focus, QListWidget#mListPlugins::item:focus {{ background-color: {ACCENT_HOVER}; color: {TEXT_BRIGHT}; }}
QTableView, QTableWidget {{ background-color: {BG_BASE}; color: {TEXT}; border: 1px solid {BORDER_DIM}; border-radius: 4px; alternate-background-color:{ACCENT_HOVER}; gridline-color: {BG_BTN_STATUS_HOVER}; selection-background-color: {ACCENT_HOVER}; selection-color: {ACCENT_HOVER}; outline: none; }}
QTableView::item, QTableWidget::item {{ padding: 3px 6px; border: none; color: {TEXT}; }}
QTableView::item:hover, QTableWidget::item:hover {{ background-color: {BG_PRESSED}; }}
QTableView::item:selected, QTableWidget::item:selected {{ background-color: {BG_SELECTED}; color: {TEXT_BRIGHT}; }}
QHeaderView {{ background-color: {BORDER_LIST_ITEM}; color: {TEXT_HEADER}; border: none; font-weight: 600; }}
QHeaderView::section {{ background-color: {BORDER_LIST_ITEM}; color: {TEXT_HEADER}; padding: 5px 8px; border: none; border-right: 1px solid {BORDER_SUBTLE}; border-bottom: 1px solid {BORDER_SUBTLE}; font-weight: 600; }}
QHeaderView::section:hover {{ background-color: {BORDER_DIM}; color: {TEXT_BRIGHT}; }}
QHeaderView::section:checked {{ background-color: {BG_SELECTED_INACTIVE}; color: {TEXT_BRIGHT}; }}
QTabWidget::pane {{ background-color: {BG_WINDOW}; border: 1px solid {BORDER_SUBTLE}; border-radius: 4px; top: -1px; }}
QTabWidget::tab-bar {{ alignment: left; left: 4px; }}
QTabBar {{ background: {TRANSPARENT}; qproperty-drawBase: 0; }}
QTabBar::tab {{ background-color: {BG_ALT}; color: {TEXT_DIM}; border: 1px solid {BORDER_SUBTLE}; padding: 6px 12px; margin-right: 1px; }}
QTabBar::tab:top {{ border-bottom: none; border-top-left-radius: 4px; border-top-right-radius: 4px; }}
QTabBar::tab:bottom {{ border-top: none; border-bottom-left-radius: 4px; border-bottom-right-radius: 4px; }}
QTabBar::tab:left {{ border-right: none; border-top-left-radius: 4px; border-bottom-left-radius: 4px; padding: 8px 8px; min-width: 28px; }}
QTabBar::tab:right {{ border-left: none; border-top-right-radius: 4px; border-bottom-right-radius: 4px; padding: 8px 8px; min-width: 28px; }}
QTabBar::tab:hover {{ background-color: {BG_HOVER}; color: {TEXT}; }}
QTabBar::tab:selected {{ background-color: {BG_WINDOW}; color: {TEXT_BRIGHT}; border-color: {BORDER_DIM}; }}
QTabBar::tab:selected:top    {{ border-bottom: 2px solid {ACCENT}; padding-bottom: 4px; }}
QTabBar::tab:selected:bottom {{ border-top: 2px solid {ACCENT}; padding-top: 4px; }}
QTabBar::tab:selected:left   {{ border-right: 2px solid {ACCENT}; padding-right: 6px; }}
QTabBar::tab:selected:right  {{ border-left: 2px solid {ACCENT}; padding-left: 6px; }}
QTabBar::tab:!selected {{ margin-top: 2px; }}
QScrollBar:vertical {{ background-color: {BG_BASE}; width: 12px; margin: 0; border: none; }}
QScrollBar::handle:vertical {{ background-color: {BORDER_BTN}; min-height: 28px; border-radius: 6px; margin: 2px 2px; }}
QScrollBar::handle:vertical:hover {{ background-color: {SCROLLBAR_HANDLE_HOVER}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ background: {TRANSPARENT}; height: 0; border: none; }}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: {TRANSPARENT}; }}
QScrollBar:horizontal {{ background-color: {BG_BASE}; height: 12px; margin: 0; border: none; }}
QScrollBar::handle:horizontal {{ background-color: {BORDER_BTN}; min-width: 28px; border-radius: 6px; margin: 2px 2px; }}
QScrollBar::handle:horizontal:hover {{ background-color: {SCROLLBAR_HANDLE_HOVER}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ background: {TRANSPARENT}; width: 0; border: none; }}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{ background: {TRANSPARENT}; }}
QScrollBar::corner {{ background-color: {BG_BASE}; }}
QCheckBox {{ background: {TRANSPARENT}; color: {TEXT}; spacing: 7px; padding: 2px 0; }}
QCheckBox:disabled {{ color: {TEXT_DISABLED}; }}
QCheckBox::indicator {{ width: 15px; height: 15px; border: 1px solid {BORDER_INDICATOR}; background-color: {BG_INDICATOR}; border-radius: 3px; }}
QCheckBox::indicator:hover {{ border-color: {ACCENT}; background-color: {BORDER_LIST_ITEM}; }}
QCheckBox::indicator:checked {{ background-color: {ACCENT}; border-color: {ACCENT}; }}
QCheckBox::indicator:indeterminate {{ background-color: {ACCENT_INDETERMINATE}; border-color: {ACCENT_PRESSED}; }}
QRadioButton {{ background: {TRANSPARENT}; color: {TEXT}; spacing: 7px; padding: 2px 0; }}
QRadioButton::indicator {{ width: 15px; height: 15px; border: 1px solid {BORDER_INDICATOR}; background-color: {BG_INDICATOR}; border-radius: 8px; }}
QRadioButton::indicator:hover {{ border-color: {ACCENT}; background-color: {BORDER_LIST_ITEM}; }}
QRadioButton::indicator:checked {{ background-color: {ACCENT}; border: 1px solid {ACCENT}; border-radius: 8px; }}
QGroupBox {{ background-color: {TRANSPARENT}; color: {TEXT_LIGHT}; border: 1px solid {BORDER_DIM}; border-radius: 5px; margin-top: 14px; padding: 10px 8px 6px 8px; font-weight: 600; }}
QGroupBox::title {{ subcontrol-origin: margin; subcontrol-position: top left; left: 10px; padding: 0 6px; background-color: {BG_WINDOW}; color: {TEXT_HEADER}; }}
QSplitter {{ background-color: {BG_WINDOW}; }}
QSplitter::handle {{ background-color: {BORDER_SUBTLE}; }}
QSplitter::handle:horizontal {{ width: 2px; }}
QSplitter::handle:vertical   {{ height: 2px; }}
QSplitter::handle:hover      {{ background-color: {ACCENT}; }}
QSplitter::handle:pressed    {{ background-color: {ACCENT_PRESSED}; }}
QFrame {{ background-color: {TRANSPARENT}; border: none; }}
QFrame[frameShape="2"], QFrame[frameShape="3"], QFrame[frameShape="6"] {{ border: 1px solid {BORDER_DIM}; border-radius: 3px; }}
QFrame[frameShape="4"] {{ background-color: {BORDER_SUBTLE}; border: none; max-height: 1px; min-height: 1px; }}
QFrame[frameShape="5"] {{ background-color: {BORDER_SUBTLE}; border: none; max-width: 1px; min-width: 1px; }}
QProgressBar {{ background-color: {BG_BASE}; color: {TEXT}; border: 1px solid {BORDER_DIM}; border-radius: 4px; text-align: center; min-height: 16px; font-weight: 600; }}
QProgressBar::chunk {{ background-color: {ACCENT}; border-radius: 3px; margin: 1px; }}
QSlider {{ background: {TRANSPARENT}; }}
QSlider::groove:horizontal {{ background-color: {BG_PRESSED}; height: 4px; border-radius: 2px; border: none; }}
QSlider::sub-page:horizontal {{ background-color: {ACCENT}; border-radius: 2px; height: 4px; }}
QSlider::handle:horizontal {{ background-color: {TEXT_LIGHT}; border: 1px solid {BORDER_BTN}; width: 14px; height: 14px; margin: -6px 0; border-radius: 8px; }}
QSlider::handle:horizontal:hover {{ background-color: {TEXT_BRIGHT}; border-color: {ACCENT}; }}
QAbstractItemView {{ background-color: {BG_BASE}; color: {TEXT}; border: 1px solid {BORDER_DIM}; selection-background-color: {BG_SELECTED}; selection-color: {TEXT_BRIGHT}; alternate-background-color: {BG_ALT}; outline: none; show-decoration-selected: 1; }}
QAbstractItemView::item {{ border: none; color: {TEXT}; }}
QAbstractItemView::item:hover {{ background-color: {BG_HOVER}; color: {TEXT_BRIGHT}; }}
QAbstractItemView::item:selected {{ background-color: {BG_SELECTED}; color: {TEXT_BRIGHT}; }}
QStackedWidget {{ background-color: {BG_WINDOW}; border: none; }}
QRubberBand {{ background-color: {ACCENT_TRANSLUCENT}; border: 2px solid {ACCENT}; border-radius: 2px; }}
QgsCollapsibleGroupBox, QgsCollapsibleGroupBoxBasic {{ background-color: {TRANSPARENT}; color: {TEXT_LIGHT}; border: 1px solid {BORDER_DIM}; border-radius: 5px; margin-top: 14px; padding: 10px 8px 6px 8px; font-weight: 600; }}
QgsFilterLineEdit {{ background-color: {BG_BASE}; color: {TEXT}; border: 1px solid {BORDER}; border-radius: 4px; padding: 4px 7px; }}
QgsFilterLineEdit:focus {{ border-color: {ACCENT}; background-color: {BG_ALT}; }}
QgsMapLayerComboBox, QgsFieldComboBox, QgsProjectionSelectionWidget, QgsScaleComboBox, QgsCheckableComboBox, QgsFeatureListComboBox, QgsRasterBandComboBox, QgsFontComboBox {{ background-color: {BG_BASE}; color: {TEXT}; border: 1px solid {BORDER}; border-radius: 4px; padding: 3px 8px; min-height: 18px; min-width: 60px; }}
QgsColorButton, QgsColorRampButton {{ border: 1px solid {BORDER}; border-radius: 4px; padding: 2px; background-color: {BG_BASE}; min-height: 18px; }}
QgsColorButton:hover, QgsColorRampButton:hover {{ border-color: {ACCENT}; }}
QgsLayerTreeView, QgsBrowserDockWidget QTreeView, QgsBrowserTreeView, QgsProcessingToolboxTreeView, QgsLocatorWidget, QgsAttributeTableView {{ background-color: {BG_BASE}; color: {TEXT}; border: 1px solid {BORDER_SUBTLE}; alternate-background-color: {BG_ALT}; selection-background-color: {BG_SELECTED}; selection-color: {TEXT_BRIGHT}; outline: none; show-decoration-selected: 1; }}
QgsLayerTreeView::item, QgsBrowserDockWidget QTreeView::item, QgsBrowserTreeView::item, QgsProcessingToolboxTreeView::item {{ padding: 3px 4px; border: none; color: {TEXT}; }}
QgsLayerTreeView::item:hover, QgsBrowserDockWidget QTreeView::item:hover, QgsBrowserTreeView::item:hover, QgsProcessingToolboxTreeView::item:hover {{ background-color: {BG_HOVER}; color: {TEXT_BRIGHT}; }}
QgsLayerTreeView::item:selected, QgsBrowserDockWidget QTreeView::item:selected, QgsBrowserTreeView::item:selected, QgsProcessingToolboxTreeView::item:selected {{ background-color: {BG_SELECTED}; color: {TEXT_BRIGHT}; }}
QgsLayerTreeView::item:selected:active, QgsBrowserDockWidget QTreeView::item:selected:active, QgsBrowserTreeView::item:selected:active, QgsProcessingToolboxTreeView::item:selected:active {{ background-color: {BG_SELECTED_ACTIVE}; color: {TEXT_BRIGHT}; }}
QgsCodeEditor, QgsCodeEditorPython, QgsCodeEditorSQL, QgsCodeEditorExpression, QgsCodeEditorHTML, QgsCodeEditorJavascript, QgsCodeEditorCSS {{ background-color: {BORDER_SUBTLE}; color: {TEXT}; border: 1px solid {BORDER_DIM}; border-radius: 4px; selection-background-color: {BG_SELECTED}; selection-color: {TEXT_BRIGHT}; }}
QgsMessageBar {{ background-color: {BG_PRESSED}; color: {TEXT}; border: 1px solid {BORDER}; border-radius: 4px; padding: 4px 8px; }}
QgsLayerStylingWidget QSplitter::handle {{ background-color: {BORDER_SUBTLE}; }}
QgsLayerStylingWidget QListWidget, QgsLayerStylingDock QListWidget {{ background-color: {BG_STATUSBAR}; border: none; border-right: 1px solid {BORDER_SUBTLE}; border-radius: 0; alternate-background-color: {BG_STATUSBAR}; min-width: 50px; }}
QgsLayerStylingWidget QListWidget::item, QgsLayerStylingDock QListWidget::item {{ padding: 6px 4px; margin: 0; border-radius: 0; border: none; min-height: 36px; }}
QgsLayerStylingWidget QListWidget::item:hover, QgsLayerStylingDock QListWidget::item:hover {{ background-color: {BG_HOVER}; color: {TEXT_BRIGHT}; }}
QgsLayerStylingWidget QListWidget::item:selected, QgsLayerStylingDock QListWidget::item:selected {{ background-color: {BG_SELECTED_ACTIVE}; color: {TEXT_BRIGHT}; }}
"""

STATUSBAR_QSS = f"""
QStatusBar {{ background-color: {BG_STATUSBAR}; color: {TEXT_DIM}; border-top: 1px solid {BORDER_DARKER}; padding: 6px 6px 2px 6px; min-height: 32px; }}
QStatusBar::item {{ border: 0; padding: 0; }}
QStatusBar QLabel {{ background: {TRANSPARENT}; color: {TEXT_DIM}; padding: 0 4px; min-height: 22px; }}
QStatusBar QToolButton, QStatusBar QPushButton {{ padding: 3px 10px; margin: 1px; min-height: 22px; min-width: 0; border-radius: 3px; }}
QStatusBar QToolButton:hover, QStatusBar QPushButton:hover {{ background-color: {BG_BTN_STATUS_HOVER}; border: 1px solid {BORDER}; }}
QStatusBar QLineEdit, QStatusBar QComboBox {{ padding: 2px 6px; margin: 1px; min-height: 20px; }}
"""

_ARROW_ICON_DIR = os.path.join(tempfile.gettempdir(), "qgis_premium_dark_arrows")

def _make_arrow_icons():
    os.makedirs(_ARROW_ICON_DIR, exist_ok=True)
    icons = {}
    size = 10
    states = {"normal": ARROW_NORMAL, "hover": ACCENT, "disabled": ARROW_DISABLED}
    for direction in ("up", "down"):
        for state, color in states.items():
            img = QImage(size, size, QImage.Format.Format_ARGB32)
            img.fill(Qt.GlobalColor.transparent)
            p = QPainter(img)
            p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            c = QColor(color)
            p.setPen(QPen(c, 1))
            p.setBrush(QBrush(c))
            cx, cy = size // 2, size // 2
            s = 3
            if direction == "down":
                pts = QPolygon([QPoint(cx - s, cy - s // 2), QPoint(cx + s, cy - s // 2), QPoint(cx, cy + s)])
            else:
                pts = QPolygon([QPoint(cx - s, cy + s // 2), QPoint(cx + s, cy + s // 2), QPoint(cx, cy - s)])
            p.drawPolygon(pts)
            p.end()
            path = os.path.join(_ARROW_ICON_DIR, f"arrow_{direction}_{state}.png")
            img.save(path, "PNG")
            icons[(direction, state)] = path.replace("\\", "/")
    branch_size = 14
    branch_states = {"normal": TEXT_LIGHT, "hover": TEXT_BRIGHT}
    for direction in ("closed", "open"):
        for state, color in branch_states.items():
            img = QImage(branch_size, branch_size, QImage.Format.Format_ARGB32)
            img.fill(Qt.GlobalColor.transparent)
            p = QPainter(img)
            p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            c = QColor(color)
            p.setPen(QPen(c, 1.4))
            p.setBrush(QBrush(c))
            cx, cy = branch_size // 2, branch_size // 2
            s = 4
            if direction == "closed":
                pts = QPolygon([QPoint(cx - s // 2, cy - s), QPoint(cx - s // 2, cy + s), QPoint(cx + s // 2 + 2, cy)])
            else:
                pts = QPolygon([QPoint(cx - s, cy - s // 2), QPoint(cx + s, cy - s // 2), QPoint(cx, cy + s // 2 + 2)])
            p.drawPolygon(pts)
            p.end()
            path = os.path.join(_ARROW_ICON_DIR, f"branch_{direction}_{state}.png")
            img.save(path, "PNG")
            icons[("branch", direction, state)] = path.replace("\\", "/")
    return icons

def _arrows_qss(icons):
    dn, dh, dd = (icons[("down", k)] for k in ("normal", "hover", "disabled"))
    un, uh, ud = (icons[("up",   k)] for k in ("normal", "hover", "disabled"))
    return f"""
QComboBox::down-arrow {{ image: url("{dn}"); width: 10px; height: 10px; }}
QComboBox::down-arrow:hover, QComboBox::down-arrow:on {{ image: url("{dh}"); }}
QComboBox::down-arrow:disabled {{ image: url("{dd}"); }}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow, QDateEdit::up-arrow, QDateTimeEdit::up-arrow, QTimeEdit::up-arrow, QgsSpinBox::up-arrow, QgsDoubleSpinBox::up-arrow {{ image: url("{un}"); width: 10px; height: 10px; }}
QSpinBox::up-arrow:hover, QDoubleSpinBox::up-arrow:hover, QgsSpinBox::up-arrow:hover, QgsDoubleSpinBox::up-arrow:hover {{ image: url("{uh}"); }}
QSpinBox::up-arrow:disabled, QDoubleSpinBox::up-arrow:disabled, QgsSpinBox::up-arrow:disabled, QgsDoubleSpinBox::up-arrow:disabled {{ image: url("{ud}"); }}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow, QDateEdit::down-arrow, QDateTimeEdit::down-arrow, QTimeEdit::down-arrow, QgsSpinBox::down-arrow, QgsDoubleSpinBox::down-arrow {{ image: url("{dn}"); width: 10px; height: 10px; }}
QSpinBox::down-arrow:hover, QDoubleSpinBox::down-arrow:hover, QgsSpinBox::down-arrow:hover, QgsDoubleSpinBox::down-arrow:hover {{ image: url("{dh}"); }}
QSpinBox::down-arrow:disabled, QDoubleSpinBox::down-arrow:disabled, QgsSpinBox::down-arrow:disabled, QgsDoubleSpinBox::down-arrow:disabled {{ image: url("{dd}"); }}
"""

def build_palette():
    p = QPalette()
    PR = QPalette.ColorRole
    PG = QPalette.ColorGroup
    p.setColor(PR.Window,          QColor(BG_WINDOW))
    p.setColor(PR.WindowText,      QColor(TEXT))
    p.setColor(PR.Base,            QColor(BG_BASE))
    p.setColor(PR.AlternateBase,   QColor(BG_ALT))
    p.setColor(PR.Text,            QColor(TEXT))
    p.setColor(PR.BrightText,      QColor(TEXT_BRIGHT))
    p.setColor(PR.Button,          QColor(BG_SELECTED_INACTIVE))
    p.setColor(PR.ButtonText,      QColor(TEXT))
    p.setColor(PR.Highlight,       QColor(BG_SELECTED_ACTIVE))
    p.setColor(PR.HighlightedText, QColor(TEXT_BRIGHT))
    p.setColor(PR.ToolTipBase,     QColor(BORDER_SUBTLE))
    p.setColor(PR.ToolTipText,     QColor(TEXT))
    p.setColor(PR.Link,            QColor(ACCENT))
    p.setColor(PR.LinkVisited,     QColor(ACCENT_HOVER))
    p.setColor(PR.PlaceholderText, QColor(TEXT_PLACEHOLDER))
    try:
        p.setColor(PR.Accent, QColor(ACCENT))
    except Exception:
        pass
    p.setColor(PG.Disabled, PR.Text,       QColor(TEXT_DISABLED))
    p.setColor(PG.Disabled, PR.WindowText, QColor(TEXT_DISABLED))
    p.setColor(PG.Disabled, PR.ButtonText, QColor(TEXT_DISABLED))
    p.setColor(PG.Inactive, PR.Highlight,       QColor(BG_SELECTED_INACTIVE))
    p.setColor(PG.Inactive, PR.HighlightedText, QColor(TEXT))
    return p

class ThemedProxyStyle(QProxyStyle):
    def generatedIconPixmap(self, mode, pixmap, opt):
        if mode == QIcon.Mode.Selected:
            return pixmap
        return super().generatedIconPixmap(mode, pixmap, opt)
    def drawPrimitive(self, element, option, painter, widget=None):
        PE = QStyle.PrimitiveElement
        SF = QStyle.StateFlag
        if element == PE.PE_IndicatorCheckBox:
            self._draw_checkbox(option, painter); return
        if element == PE.PE_IndicatorRadioButton:
            self._draw_radio(option, painter); return
        if element == PE.PE_IndicatorBranch:
            if option.state & SF.State_Children:
                self._draw_branch_arrow(option, painter)
            return
        if element in (PE.PE_IndicatorSpinUp, PE.PE_IndicatorArrowUp):
            self._draw_spin_arrow(option, painter, "up"); return
        if element in (PE.PE_IndicatorSpinDown, PE.PE_IndicatorArrowDown):
            self._draw_spin_arrow(option, painter, "down"); return
        super().drawPrimitive(element, option, painter, widget)
    def _draw_checkbox(self, option, painter):
        SF = QStyle.StateFlag
        rect = option.rect.adjusted(1, 1, -1, -1)
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        checked = bool(option.state & SF.State_On)
        partial = bool(option.state & SF.State_NoChange)
        hover   = bool(option.state & SF.State_MouseOver)
        enabled = bool(option.state & SF.State_Enabled)
        if checked or partial:
            fill = QColor(ACCENT) if enabled else QColor(ACCENT_DISABLED)
            painter.setBrush(QBrush(fill)); painter.setPen(QPen(fill, 1))
        else:
            painter.setBrush(QBrush(QColor(BG_INDICATOR)))
            border = QColor(ACCENT) if hover else QColor(BORDER_INDICATOR)
            painter.setPen(QPen(border, 1))
        painter.drawRoundedRect(rect, 2, 2)
        if checked:
            pen = QPen(QColor(CHECKMARK), 1.8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen); painter.setBrush(Qt.BrushStyle.NoBrush)
            cx, cy = rect.center().x(), rect.center().y(); w = rect.width()
            painter.drawLine(cx - w//4, cy + 1, cx - w//10, cy + w//5)
            painter.drawLine(cx - w//10, cy + w//5, cx + w//3, cy - w//5)
        elif partial:
            painter.setPen(QPen(QColor(CHECKMARK), 2))
            painter.drawLine(rect.left() + 3, rect.center().y(), rect.right() - 3, rect.center().y())
        painter.restore()
    def _draw_radio(self, option, painter):
        SF = QStyle.StateFlag
        rect = option.rect.adjusted(1, 1, -1, -1)
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        checked = bool(option.state & SF.State_On)
        hover   = bool(option.state & SF.State_MouseOver)
        enabled = bool(option.state & SF.State_Enabled)
        if checked:
            fill = QColor(ACCENT) if enabled else QColor(ACCENT_DISABLED)
            painter.setBrush(QBrush(fill)); painter.setPen(QPen(fill, 1))
        else:
            painter.setBrush(QBrush(QColor(BG_INDICATOR)))
            border = QColor(ACCENT) if hover else QColor(BORDER_INDICATOR)
            painter.setPen(QPen(border, 1))
        painter.drawEllipse(rect)
        if checked:
            inner = rect.adjusted(rect.width()//4, rect.height()//4, -rect.width()//4, -rect.height()//4)
            painter.setBrush(QBrush(QColor(CHECKMARK)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(inner)
        painter.restore()
    def _draw_branch_arrow(self, option, painter):
        SF = QStyle.StateFlag
        rect = option.rect
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        is_open  = bool(option.state & SF.State_Open)
        hover    = bool(option.state & SF.State_MouseOver)
        selected = bool(option.state & SF.State_Selected)
        color = QColor(TEXT_BRIGHT) if (hover or selected) else QColor(TEXT_LIGHT)
        painter.setPen(QPen(color, 1.4)); painter.setBrush(QBrush(color))
        cx, cy = rect.center().x(), rect.center().y(); s = 4
        if is_open:
            pts = QPolygon([QPoint(cx - s, cy - s // 2), QPoint(cx + s, cy - s // 2), QPoint(cx, cy + s // 2 + 2)])
        else:
            pts = QPolygon([QPoint(cx - s // 2, cy - s), QPoint(cx - s // 2, cy + s), QPoint(cx + s // 2 + 2, cy)])
        painter.drawPolygon(pts)
        painter.restore()
    def _draw_spin_arrow(self, option, painter, direction):
        SF = QStyle.StateFlag
        rect = option.rect
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        enabled = bool(option.state & SF.State_Enabled)
        hover   = bool(option.state & SF.State_MouseOver)
        if not enabled: color = QColor(ARROW_DISABLED)
        elif hover:     color = QColor(TEXT_BRIGHT)
        else:           color = QColor(ARROW_NORMAL)
        painter.setPen(QPen(color, 1)); painter.setBrush(QBrush(color))
        cx, cy = rect.center().x(), rect.center().y(); s = 3
        if direction == "up":
            pts = QPolygon([QPoint(cx - s, cy + s // 2), QPoint(cx + s, cy + s // 2), QPoint(cx, cy - s)])
        else:
            pts = QPolygon([QPoint(cx - s, cy - s // 2), QPoint(cx + s, cy - s // 2), QPoint(cx, cy + s)])
        painter.drawPolygon(pts)
        painter.restore()

NAV_LIST_QSS = (
    "QListWidget, QListView {"
    f" background-color: {BG_BASE}; color: {TEXT};"
    f" border: 1px solid {BORDER_SUBTLE};"
    " border-radius: 4px; outline: none;"
    f" alternate-background-color: {BG_ALT};"
    " padding: 2px;"
    "}"
    "QListWidget::item, QListView::item {"
    f" background-color: transparent; color: {TEXT};"
    " padding: 7px 10px; border: none; border-radius: 3px;"
    " margin: 1px 2px; min-height: 22px;"
    "}"
    "QListWidget::item:hover, QListView::item:hover {"
    f" background-color: {BG_HOVER}; color: {TEXT_BRIGHT};"
    "}"
    "QListWidget::item:selected, QListView::item:selected {"
    f" background-color: {BG_SELECTED_ACTIVE}; color: {TEXT_BRIGHT};"
    "}"
    "QListWidget::item:selected:!active, QListView::item:selected:!active {"
    f" background-color: {BG_SELECTED_INACTIVE}; color: {TEXT};"
    "}"
)

PLUGIN_LIST_QSS = (
    "QListView, QListWidget {"
    f" background-color: {BG_BASE}; color: {TEXT};"
    f" border: 1px solid {BORDER_SUBTLE};"
    " border-radius: 4px; outline: 0;"
    f" alternate-background-color: {BG_ALT};"
    f" selection-background-color: {BG_SELECTED_ACTIVE};"
    f" selection-color: {TEXT_BRIGHT};"
    " show-decoration-selected: 1; padding: 2px;"
    "}"
    "QListView::item, QListWidget::item {"
    f" background-color: transparent; color: {TEXT};"
    " padding: 8px 10px; border: none;"
    f" border-bottom: 1px solid {BORDER_LIST_ITEM};"
    " min-height: 32px; margin: 0;"
    "}"
    "QListView::item:hover, QListWidget::item:hover {"
    f" background-color: {BG_HOVER}; color: {TEXT_BRIGHT};"
    "}"
    "QListView::item:selected, QListWidget::item:selected,"
    "QListView::item:selected:active, QListWidget::item:selected:active {"
    f" background-color: {BG_SELECTED_ACTIVE}; color: {TEXT_BRIGHT};"
    "}"
    "QListView::item:selected:hover, QListWidget::item:selected:hover {"
    f" background-color: {BG_PLUGIN_SEL_HOVER}; color: {TEXT_BRIGHT};"
    "}"
    "QListView::item:selected:!active, QListWidget::item:selected:!active {"
    f" background-color: {BG_PLUGIN_INACTIVE}; color: {TEXT};"
    "}"
    "QListView::item:focus, QListWidget::item:focus {"
    f" background-color: {BG_SELECTED_ACTIVE}; color: {TEXT_BRIGHT};"
    "}"
)

def _build_nav_tree_qss(icons):
    bcn = icons[("branch", "closed", "normal")]
    bch = icons[("branch", "closed", "hover")]
    bon = icons[("branch", "open",   "normal")]
    boh = icons[("branch", "open",   "hover")]
    return f"""
QTreeWidget, QTreeView {{ background-color: {BG_BASE}; color: {TEXT}; border: 1px solid {BORDER_SUBTLE}; border-radius: 4px; outline: none; alternate-background-color: {BG_ALT}; padding: 2px; show-decoration-selected: 1; selection-background-color: {BG_SELECTED_ACTIVE}; selection-color: {TEXT_BRIGHT}; }}
QTreeWidget::item, QTreeView::item {{ background-color: transparent; color: {TEXT}; padding: 5px 4px; border: none; min-height: 22px; }}
QTreeWidget::item:hover, QTreeView::item:hover {{ background-color: {BG_HOVER}; color: {TEXT_BRIGHT}; }}
QTreeWidget::item:selected, QTreeView::item:selected {{ background-color: {BG_SELECTED_ACTIVE}; color: {TEXT_BRIGHT}; }}
QTreeWidget::item:selected:!active, QTreeView::item:selected:!active {{ background-color: {BG_SELECTED_INACTIVE}; color: {TEXT}; }}
QTreeWidget::branch, QTreeView::branch {{ background: transparent; }}
QTreeWidget::branch:hover, QTreeView::branch:hover {{ background-color: {BG_HOVER}; }}
QTreeWidget::branch:selected, QTreeView::branch:selected {{ background-color: {BG_SELECTED_ACTIVE}; }}
QTreeWidget::branch:has-children:!has-siblings:closed, QTreeWidget::branch:closed:has-children:has-siblings, QTreeView::branch:has-children:!has-siblings:closed, QTreeView::branch:closed:has-children:has-siblings {{ image: url("{bcn}"); }}
QTreeWidget::branch:open:has-children:!has-siblings, QTreeWidget::branch:open:has-children:has-siblings, QTreeView::branch:open:has-children:!has-siblings, QTreeView::branch:open:has-children:has-siblings {{ image: url("{bon}"); }}
QTreeWidget::branch:has-children:!has-siblings:closed:hover, QTreeWidget::branch:closed:has-children:has-siblings:hover, QTreeView::branch:has-children:!has-siblings:closed:hover, QTreeView::branch:closed:has-children:has-siblings:hover {{ image: url("{bch}"); }}
QTreeWidget::branch:open:has-children:!has-siblings:hover, QTreeWidget::branch:open:has-children:has-siblings:hover, QTreeView::branch:open:has-children:!has-siblings:hover, QTreeView::branch:open:has-children:has-siblings:hover {{ image: url("{boh}"); }}
"""

NAV_TREE_QSS = ""

NAV_LIST_NAMES = (
    "mOptListWidget", "mOptionsListWidget", "mWidgetMenu",
    "mNavigationList", "mTabsList",
    "mOptionsTreeView", "mOptionsTreeWidget", "mOptionsTree", "mNavigationTree",
)

NAV_TREE_CLASSES = ("QgsOptionsTreeView", "QgsOptionsTreeWidget")

PLUGIN_LIST_NAMES = ("vwPlugins", "mListPlugins", "mPluginsList")

LAYER_STYLING_CLASSES = (
    "QgsLayerStylingWidget", "QgsLayerStylingDock", "QgsMapStylingDock",
)

PLUGIN_MANAGER_CLASSES = (
    "QgsPluginManager", "QgsPluginManagerDialog", "QgsPluginManagerInterface",
)

class PluginViewportHoverFilter(QObject):
    """Forces repaint when the mouse moves so State_MouseOver updates each row."""
    def eventFilter(self, obj, event):
        t = event.type()
        if t in (QEvent.Type.MouseMove, QEvent.Type.HoverMove,
                 QEvent.Type.HoverEnter, QEvent.Type.HoverLeave,
                 QEvent.Type.Leave):
            try:
                obj.update()
            except Exception:
                pass
        return False

_vp_hover_filter = PluginViewportHoverFilter()   # keep a reference alive

class PluginListDelegate(QStyledItemDelegate):
    """Wraps the plugin manager's own delegate, injects themed hover/selection
    backgrounds, AND clamps decoration size so plugin icons render uniformly.
    QSS is ignored by custom delegates, so the icon size must be enforced here."""

    ICON_SIZE = QSize(32, 32)   # single source of truth for plugin icon size

    def __init__(self, wrapped, parent=None):
        super().__init__(parent)
        self._wrapped = wrapped

    def _clamp(self, option):
        # Force a uniform decoration size regardless of the icon's native size.
        option.decorationSize = self.ICON_SIZE
        # Re-bake the icon at the target size, so any code path that draws
        # option.icon.pixmap() without an explicit size cannot pull a 128px pixmap.
        if not option.icon.isNull():
            option.icon = QIcon(option.icon.pixmap(self.ICON_SIZE))

    def paint(self, painter, option, index):
        from qgis.PyQt.QtWidgets import QStyleOptionViewItem

        selected = bool(option.state & QStyle.StateFlag.State_Selected)
        hovered  = bool(option.state & QStyle.StateFlag.State_MouseOver)

        if selected:
            bg_color = QColor(BG_SELECTED_ACTIVE)
        elif hovered:
            bg_color = QColor(BG_HOVER)
        else:
            bg_color = QColor(BG_BASE)

        painter.save()
        painter.fillRect(option.rect, bg_color)
        painter.setPen(QPen(QColor(BORDER_LIST_ITEM), 1))
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
        painter.restore()

        opt = QStyleOptionViewItem(option)
        opt.state &= ~(QStyle.StateFlag.State_Selected | QStyle.StateFlag.State_MouseOver)
        self._clamp(opt)                              # <-- enforce here too

        pal = opt.palette
        text_color = QColor(TEXT_BRIGHT) if (selected or hovered) else QColor(TEXT)
        pal.setColor(QPalette.ColorRole.Text,       text_color)
        pal.setColor(QPalette.ColorRole.WindowText, text_color)
        opt.palette = pal

        self._wrapped.paint(painter, opt, index)

    def sizeHint(self, option, index):
        from qgis.PyQt.QtWidgets import QStyleOptionViewItem
        opt = QStyleOptionViewItem(option)
        self._clamp(opt)                              # <-- so row height shrinks
        return self._wrapped.sizeHint(opt, index)

    def initStyleOption(self, option, index):
        try:
            self._wrapped.initStyleOption(option, index)
        except Exception:
            super().initStyleOption(option, index)
        self._clamp(option)                           # <-- clamp AFTER wrapped runs

class WidgetFixer(QObject):
    def eventFilter(self, obj, event):
        try:
            if event.type() == QEvent.Type.Show and isinstance(obj, QWidget):
                self._fix(obj)
                QTimer.singleShot(0,   lambda w=obj: self._fix_safe(w))
                QTimer.singleShot(150, lambda w=obj: self._fix_safe(w))
                QTimer.singleShot(500, lambda w=obj: self._fix_safe(w))
        except Exception:
            pass
        return False
    def _fix_safe(self, w):
        try:
            if w is None: return
            self._fix(w)
        except RuntimeError:
            return
        except Exception:
            return
    def _fix(self, w):
        for child in w.findChildren((QListWidget, QListView)):
            if child.objectName() in NAV_LIST_NAMES:
                child.setStyleSheet(NAV_LIST_QSS)
        for child in w.findChildren((QTreeWidget, QTreeView)):
            if (child.objectName() in NAV_LIST_NAMES
                    or type(child).__name__ in NAV_TREE_CLASSES):
                child.setStyleSheet(NAV_TREE_QSS)
        for child in w.findChildren(QSplitter):
            child.setHandleWidth(2)
        cls = type(w).__name__
        if cls in LAYER_STYLING_CLASSES or any(p for p in self._ancestors(w) if p in LAYER_STYLING_CLASSES):
            self._fix_layer_styling(w)
        for inner in w.findChildren(QWidget):
            try:
                if type(inner).__name__ in LAYER_STYLING_CLASSES:
                    self._fix_layer_styling(inner)
            except Exception:
                pass
        if cls in PLUGIN_MANAGER_CLASSES:
            self._fix_plugin_manager(w)
        for child in w.findChildren((QListView, QListWidget)):
            if child.objectName() in PLUGIN_LIST_NAMES:
                self._fix_plugin_list(child)
    def _ancestors(self, w):
        names = []
        try:
            p = w.parentWidget()
            depth = 0
            while p is not None and depth < 8:
                names.append(type(p).__name__)
                p = p.parentWidget()
                depth += 1
        except Exception:
            pass
        return names
    def _fix_layer_styling(self, w):
        try:
            for sp in w.findChildren(QSplitter):
                sp.setChildrenCollapsible(False)
                sp.setHandleWidth(2)
                if sp.orientation() == Qt.Orientation.Horizontal and sp.count() >= 2:
                    first = sp.widget(0)
                    if first is not None:
                        first.setMinimumWidth(52)
                        first.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                    sp.setStretchFactor(0, 0)
                    sp.setStretchFactor(1, 1)
                    total = sp.width() or 480
                    sp.setSizes([56, max(220, total - 56)])
            tab_lists = []
            for lw in w.findChildren(QListWidget):
                try:
                    is_iconmode = lw.viewMode() == QListView.ViewMode.IconMode
                    is_vert = lw.flow() == QListView.Flow.TopToBottom
                    if is_iconmode or is_vert or lw.objectName() in NAV_LIST_NAMES:
                        tab_lists.append(lw)
                except Exception:
                    continue
            for lw in tab_lists:
                lw.setMinimumWidth(52)
                lw.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                lw.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                lw.raise_()
                try:
                    lw.viewport().raise_()
                except Exception:
                    pass
            for stk in w.findChildren(QStackedWidget):
                stk.setContentsMargins(0, 0, 0, 0)
        except Exception:
            pass
    def _fix_plugin_manager(self, w):
        for plist in w.findChildren((QListView, QListWidget)):
            if plist.objectName() in PLUGIN_LIST_NAMES or "Plugin" in type(plist).__name__:
                self._fix_plugin_list(plist)

    def _fix_plugin_list(self, plist):
        try:
            # --- mouse tracking & hover events ---
            plist.setMouseTracking(True)
            plist.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
            plist.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
            vp = plist.viewport()
            if vp is not None:
                vp.setMouseTracking(True)
                vp.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
                vp.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
                # Force repaint on every mouse-move so hover rows update
                vp.installEventFilter(_vp_hover_filter)

            plist.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            plist.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

            # --- palette (fallback path and for the delegate's opt.palette) ---
            pal = plist.palette()
            pal.setColor(QPalette.ColorRole.Base,            QColor(BG_BASE))
            pal.setColor(QPalette.ColorRole.AlternateBase,   QColor(BG_ALT))
            pal.setColor(QPalette.ColorRole.Text,            QColor(TEXT))
            pal.setColor(QPalette.ColorRole.Highlight,       QColor(BG_SELECTED_ACTIVE))
            pal.setColor(QPalette.ColorRole.HighlightedText, QColor(TEXT_BRIGHT))
            pal.setColor(QPalette.ColorGroup.Inactive,
                        QPalette.ColorRole.Highlight,       QColor(BG_PLUGIN_INACTIVE))
            pal.setColor(QPalette.ColorGroup.Inactive,
                        QPalette.ColorRole.HighlightedText, QColor(TEXT))
            plist.setPalette(pal)
            if vp is not None:
                vp.setPalette(pal)

            plist.setIconSize(PluginListDelegate.ICON_SIZE)
            
            # --- QSS as an additional layer ---
            plist.setStyleSheet(PLUGIN_LIST_QSS)
            # plist.style().unpolish(plist)
            # plist.style().polish(plist)
            sz = plist.iconSize()
            if not sz.isValid() or sz.width() <= 0:
                from qgis.PyQt.QtCore import QSize
                sz = QSize(32, 32)
            plist.setIconSize(sz)
            try:
                plist.update()
                if vp is not None:
                    vp.update()
                    vp.repaint()
            except Exception:
                pass
        except Exception:
            pass


def apply_theme():
    app = QApplication.instance()
    if app is None:
        return
    app.setPalette(build_palette())
    arrow_icons = _make_arrow_icons()
    arrows_qss  = _arrows_qss(arrow_icons)
    global NAV_TREE_QSS
    NAV_TREE_QSS = _build_nav_tree_qss(arrow_icons)
    app.setStyleSheet(QSS + arrows_qss)
    app.setStyle(ThemedProxyStyle(app.style().name()))
    global theme_fixer
    theme_fixer = WidgetFixer()
    app.installEventFilter(theme_fixer)
    if iface is not None:
        iface.mainWindow().statusBar().setStyleSheet(STATUSBAR_QSS)
    print("Premium Dark Theme Applied Successfully!")

apply_theme()