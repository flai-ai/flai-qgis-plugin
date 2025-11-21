# compat_qt.py
from qgis.PyQt.QtWidgets import QMessageBox as _MB

try:
    # Qt6 style (nested enums)?
    _MB.Icon    # will fail on Qt5
    ICON_INFORMATION = _MB.Icon.Information
    ICON_WARNING     = _MB.Icon.Warning
    ICON_CRITICAL    = _MB.Icon.Critical
    
    ROLE_ACCEPT      = _MB.ButtonRole.AcceptRole
    ROLE_REJECT      = _MB.ButtonRole.RejectRole

    BTN_OK           = _MB.StandardButton.Ok
    BTN_CANCEL       = _MB.StandardButton.Cancel
    BTN_NONE         = _MB.StandardButton.NoButton

except AttributeError:
    # Qt5 style (flat enums)
    ICON_INFORMATION = _MB.Information
    ICON_WARNING     = _MB.Warning
    ICON_CRITICAL    = _MB.Critical

    ROLE_ACCEPT      = _MB.AcceptRole
    ROLE_REJECT      = _MB.RejectRole

    BTN_OK           = _MB.Ok
    BTN_CANCEL       = _MB.Cancel
    BTN_NONE         = _MB.NoButton