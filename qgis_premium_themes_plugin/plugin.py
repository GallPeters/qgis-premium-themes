from qgis.core import (
    Qgis,
    QgsApplication,
    QgsApplicationThemeRegistry,
)

import os

class QgisPremiumThemesPlugin:
    """
    QGIS theme plugin sample
    """

    THEME_NAME = "Premium"
    THEME_FOLDER = "premium" 
    
    def __init__(self, iface):
        """init"""

    def initGui(self):
        """startup"""
        QgsApplication.applicationThemeRegistry().addTheme(
                self.THEME_NAME, 
                os.path.join(os.path.dirname(__file__), self.THEME_FOLDER)
        )

    def unload(self):
        """teardown"""
        QgsApplication.applicationThemeRegistry().removeTheme(self.THEME_NAME)
