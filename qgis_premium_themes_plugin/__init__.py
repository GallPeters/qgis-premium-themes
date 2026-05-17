def classFactory(iface):
    """invoke plugin"""
    from qgis_premium_themes_plugin.plugin import QgisPremiumThemesPlugin  # pylint: disable=import-outside-toplevel

    return QgisPremiumThemesPlugin(iface)
    
