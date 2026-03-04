import bpy
import bpy.types as bt

from . import properties as prop
from . import usda_primref_editor as subedit


class USD_OT_ScanSublayers(bt.Operator):
    """Scan a USDA file's root layer for sublayers."""

    bl_idname = "usd_sublayers.scan"
    bl_label = "Scan USDA Sublayers"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context) -> bool:
        return context.scene is not None

    def execute(self, context):
        scene = context.scene
        settings: prop.USDSublayerSettings = scene.usd_sublayer_settings

        usda_path = settings.usda_path
        if not usda_path:
            self.report({"ERROR"}, "Please choose a USDA file first.")
            return {"CANCELLED"}

        try:
            editor = subedit.UsdaSublayerEditor(usda_path)
            sublayer_paths = editor.load_sublayers()
        except Exception as exc:
            self.report({"ERROR"}, f"Failed to read USDA sublayers: {exc}")
            return {"CANCELLED"}

        settings.sublayers.clear()

        for path in sublayer_paths:
            item: prop.USDSublayerItem = settings.sublayers.add()
            item.filepath = path

        if not settings.sublayers:
            self.report({"INFO"}, "No sublayers found in this USDA file.")
        else:
            self.report(
                {"INFO"},
                f"Found {len(settings.sublayers)} sublayer(s) in this USDA file.",
            )

        return {"FINISHED"}


class USD_OT_MoveSublayerItem(bt.Operator):
    """Move the active sublayer up or down within the root layer's subLayerPaths."""

    bl_idname = "usd_sublayers.move_item"
    bl_label = "Move Sublayer"
    bl_options = {"REGISTER", "UNDO"}

    direction: bpy.props.EnumProperty(
        name="Direction",
        items=(
            ("UP", "Up", "Move the item up"),
            ("DOWN", "Down", "Move the item down"),
        ),
    )

    @classmethod
    def poll(cls, context) -> bool:
        return context.scene is not None

    def execute(self, context):
        scene = context.scene
        settings: prop.USDSublayerSettings = scene.usd_sublayer_settings

        sublayers = settings.sublayers
        idx = settings.active_sublayer_index

        if not sublayers or idx < 0 or idx >= len(sublayers):
            return {"CANCELLED"}

        if self.direction == "UP":
            new_index = idx - 1
        else:
            new_index = idx + 1

        if new_index < 0 or new_index >= len(sublayers):
            return {"CANCELLED"}

        sublayers.move(idx, new_index)
        settings.active_sublayer_index = new_index

        return {"FINISHED"}


class USD_OT_SaveSublayers(bt.Operator):
    """Save the current list and order of sublayers back to the USDA file."""

    bl_idname = "usd_sublayers.save"
    bl_label = "Save Sublayers"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context) -> bool:
        return context.scene is not None

    def execute(self, context):
        scene = context.scene
        settings: prop.USDSublayerSettings = scene.usd_sublayer_settings

        usda_path = settings.usda_path
        if not usda_path:
            self.report({"ERROR"}, "Please choose a USDA file first.")
            return {"CANCELLED"}

        new_order = [item.filepath for item in settings.sublayers]

        try:
            editor = subedit.UsdaSublayerEditor(usda_path)
            editor.save_sublayers(new_order)
        except Exception as exc:
            self.report(
                {"ERROR"},
                f"Failed to save sublayers for '{usda_path}': {exc}",
            )
            return {"CANCELLED"}

        self.report(
            {"INFO"},
            f"Saved {len(new_order)} sublayer(s) for '{usda_path}'.",
        )

        return {"FINISHED"}


CLASSES = (
    USD_OT_ScanSublayers,
    USD_OT_MoveSublayerItem,
    USD_OT_SaveSublayers,
)


def register() -> None:
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


