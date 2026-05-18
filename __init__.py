def classFactory(iface):
    """invoke plugin"""
    from qgis_studio_themes.plugin import QgisStudioThemesPlugin  # pylint: disable=import-outside-toplevel

    return QgisStudioThemesPlugin(iface)
    
