import bpy
import bpy.types as bt
import bpy.props as bp


class USDRefItem(bt.PropertyGroup):
    filepath: bp.StringProperty(
        name="Filepath",
        description="Filepath from a prepended USD reference",
    )


class USDPrimItem(bt.PropertyGroup):
    prim_path: bp.StringProperty(
        name="Prim Path",
        description="USD prim path that has prepended references",
    )
    refs: bp.CollectionProperty(
        name="Prepended References",
        description="Filepaths found in this prim's prepended references",
        type=USDRefItem,
    )
    active_ref_index: bp.IntProperty(
        name="Active Reference Index",
        default=0,
    )


class USDPrimRefSettings(bt.PropertyGroup):
    usda_path: bp.StringProperty(
        name="USDA File",
        description="Path to a USDA file to inspect for prim prepended references",
        subtype="FILE_PATH",
    )
    prims: bp.CollectionProperty(
        name="Prims With Prepended Refs",
        description="Prims in the USDA file that have prepended references",
        type=USDPrimItem,
    )


CLASSES = (
    USDRefItem,
    USDPrimItem,
    USDPrimRefSettings,
)


def register() -> None:
    for cls in CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.Scene.usd_primref_settings = bp.PointerProperty(type=USDPrimRefSettings)


def unregister() -> None:
    del bpy.types.Scene.usd_primref_settings

    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


