bl_info = {
    "name": "USD Sublayer Editor",
    "author": "lsantos",
    "version": (0, 1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar (N) > USD Refs",
    "description": "Edit USDA file's root layer's subLayerPaths (sublayers).",
    "category": "Import-Export",
}

from . import properties as prop
from . import operators as ops
from . import ui as ui_mod


def register() -> None:
    prop.register()
    ops.register()
    ui_mod.register()


def unregister() -> None:
    ui_mod.unregister()
    ops.unregister()
    prop.unregister()


