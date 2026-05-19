def classFactory(iface):
    """invoke plugin"""
    from qgis_studio_themes.qgis_studio_themes import QgisStudioThemesPlugin, init_theme_paths  # pylint: disable=import-outside-toplevel

    init_theme_paths()
    return QgisStudioThemesPlugin(iface)
    
