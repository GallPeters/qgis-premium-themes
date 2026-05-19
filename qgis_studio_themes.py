from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QDir
from pathlib import Path
import os


def init_theme_paths():
    themes_dir = Path(__file__).parent / "themes"

    # THIS is the key change
    QDir.addSearchPath("theme", str(themes_dir))

class QgisStudioThemesPlugin:
    """
    QGIS theme plugin sample
    """

    THEMES = ["Premium", "Web", "Pro", "Dark"]

    def __init__(self, iface):
        """init"""

    def initGui(self):
        """startup"""
        for theme in self.THEMES:
            QgsApplication.applicationThemeRegistry().addTheme(
                   f'Studio {theme}', 
                    os.path.join(os.path.dirname(__file__), 'themes', theme.lower())
            )

    def unload(self):
        """teardown"""
        for theme in self.THEMES:
            QgsApplication.applicationThemeRegistry().removeTheme(f'Studio {theme}')
