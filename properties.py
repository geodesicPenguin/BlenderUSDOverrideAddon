import bpy
import bpy.types as bt
import bpy.props as bp


class USDSublayerItem(bt.PropertyGroup):
    filepath: bp.StringProperty(
        name="Sublayer Filepath",
        description="Filepath of a sublayer in the USDA file's root layer",
    )


class USDSublayerSettings(bt.PropertyGroup):
    usda_path: bp.StringProperty(
        name="USDA File",
        description="Path to a USDA file whose root-layer sublayers should be edited",
        subtype="FILE_PATH",
    )
    sublayers: bp.CollectionProperty(
        name="Sublayers",
        description="Sublayer filepaths from the USDA file's root layer",
        type=USDSublayerItem,
    )
    active_sublayer_index: bp.IntProperty(
        name="Active Sublayer Index",
        default=0,
    )


CLASSES = (
    USDSublayerItem,
    USDSublayerSettings,
)


def register() -> None:
    for cls in CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.Scene.usd_sublayer_settings = bp.PointerProperty(
        type=USDSublayerSettings
    )


def unregister() -> None:
    del bpy.types.Scene.usd_sublayer_settings

    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


