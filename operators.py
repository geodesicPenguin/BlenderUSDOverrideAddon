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


CLASSES = (
    USD_OT_ScanPrimPrependedRefs,
)


def register() -> None:
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


