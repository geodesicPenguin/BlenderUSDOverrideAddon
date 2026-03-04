import bpy
import bpy.types as bt

from . import properties as prop
from . import usda_primref_editor as primref


class USD_OT_ScanPrimPrependedRefs(bt.Operator):
    """Scan a USDA file for prims that have prepended references."""

    bl_idname = "usd_primrefs.scan"
    bl_label = "Scan USDA Prims"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context) -> bool:
        return context.scene is not None

    def execute(self, context):
        scene = context.scene
        settings: prop.USDPrimRefSettings = scene.usd_primref_settings

        usda_path = settings.usda_path
        if not usda_path:
            self.report({"ERROR"}, "Please choose a USDA file first.")
            return {"CANCELLED"}

        try:
            prim_paths = primref.get_prim_paths_with_prepended_refs(usda_path)
        except Exception as exc:  
            self.report({"ERROR"}, f"Failed to read USDA file: {exc}")
            return {"CANCELLED"}

        settings.prims.clear()

        for prim_path in prim_paths:
            prim_item: prop.USDPrimItem = settings.prims.add()
            prim_item.prim_path = prim_path

            try:
                editor = primref.UsdPrimRefEditor(usda_path, prim_path)
                ref_paths = editor.load_primrefs()
            except Exception as exc:  
                self.report(
                    {"WARNING"},
                    f"Failed to read prepended refs for '{prim_path}': {exc}",
                )
                continue

            for ref_path in ref_paths:
                ref_item: prop.USDRefItem = prim_item.refs.add()
                ref_item.filepath = ref_path

        if not settings.prims:
            self.report(
                {"INFO"},
                "No prims with prepended references were found in this USDA file.",
            )
        else:
            self.report(
                {"INFO"},
                f"Found {len(settings.prims)} prim(s) with prepended references.",
            )

        return {"FINISHED"}


class USD_OT_MovePrimRefItem(bt.Operator):
    """Move the active prepended reference up or down within a prim's list."""

    bl_idname = "usd_primrefs.move_ref_item"
    bl_label = "Move Prim Reference"
    bl_options = {"REGISTER", "UNDO"}

    direction: bpy.props.EnumProperty(
        name="Direction",
        items=(
            ("UP", "Up", "Move the item up"),
            ("DOWN", "Down", "Move the item down"),
        ),
    )

    prim_path: bpy.props.StringProperty(
        name="Prim Path",
        description="USD prim path this reference list belongs to",
    )

    @classmethod
    def poll(cls, context) -> bool:
        return context.scene is not None

    def execute(self, context):
        scene = context.scene
        settings: prop.USDPrimRefSettings = scene.usd_primref_settings

        # Find the matching prim item by path
        prim_item = None
        for item in settings.prims:
            if item.prim_path == self.prim_path:
                prim_item = item
                break

        if prim_item is None:
            self.report({"ERROR"}, f"Prim '{self.prim_path}' not found in settings.")
            return {"CANCELLED"}

        refs = prim_item.refs
        idx = prim_item.active_ref_index

        if not refs or idx < 0 or idx >= len(refs):
            return {"CANCELLED"}

        if self.direction == "UP":
            new_index = idx - 1
        else:
            new_index = idx + 1

        if new_index < 0 or new_index >= len(refs):
            return {"CANCELLED"}

        refs.move(idx, new_index)
        prim_item.active_ref_index = new_index

        return {"FINISHED"}


class USD_OT_SavePrimRefOrder(bt.Operator):
    """Save the current order of prepended references for a prim back to the USDA file."""

    bl_idname = "usd_primrefs.save_prim_order"
    bl_label = "Save Prim Reference Order"
    bl_options = {"REGISTER", "UNDO"}

    prim_path: bpy.props.StringProperty(
        name="Prim Path",
        description="USD prim path whose references should be saved",
    )

    @classmethod
    def poll(cls, context) -> bool:
        return context.scene is not None

    def execute(self, context):
        scene = context.scene
        settings: prop.USDPrimRefSettings = scene.usd_primref_settings

        usda_path = settings.usda_path
        if not usda_path:
            self.report({"ERROR"}, "Please choose a USDA file first.")
            return {"CANCELLED"}

        # Find the matching prim item by path
        prim_item = None
        for item in settings.prims:
            if item.prim_path == self.prim_path:
                prim_item = item
                break

        if prim_item is None:
            self.report({"ERROR"}, f"Prim '{self.prim_path}' not found in settings.")
            return {"CANCELLED"}

        new_order = [ref.filepath for ref in prim_item.refs]

        try:
            editor = primref.UsdPrimRefEditor(usda_path, self.prim_path)
            editor.save_primrefs(new_order)
        except Exception as exc:
            self.report(
                {"ERROR"},
                f"Failed to save prepended refs for '{self.prim_path}': {exc}",
            )
            return {"CANCELLED"}

        self.report(
            {"INFO"},
            f"Saved {len(new_order)} prepended reference(s) for '{self.prim_path}'.",
        )

        return {"FINISHED"}


CLASSES = (
    USD_OT_ScanPrimPrependedRefs,
    USD_OT_MovePrimRefItem,
    USD_OT_SavePrimRefOrder,
)


def register() -> None:
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


