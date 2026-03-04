import bpy
import bpy.types as bt

from . import properties as prop


class USD_UL_PrimRefList(bt.UIList):
    """List of filepaths for a single prim's prepended references."""

    bl_idname = "USD_UL_prim_ref_list"

    def draw_item(
        self,
        context,
        layout,
        data,
        item,
        icon,
        active_data,
        active_propname,
        index,
    ):
        ref: prop.USDRefItem = item
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            layout.label(text=ref.filepath or "<empty>")
        elif self.layout_type == "GRID":
            layout.alignment = "CENTER"
            layout.label(text=str(index))


class USD_PT_PrimPrependedRefs(bt.Panel):
    """Panel in the 3D Viewport side bar to show USDA prim prepended refs."""

    bl_label = "USD Prim Prepended Refs"
    bl_idname = "USD_PT_prim_prepended_refs"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "USD Refs"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings: prop.USDPrimRefSettings = scene.usd_primref_settings

        layout.prop(settings, "usda_path")

        row = layout.row(align=True)
        row.operator("usd_primrefs.scan", icon="FILE_REFRESH")

        if not settings.prims:
            layout.separator()
            layout.label(text="No prims with prepended refs found.")
            return

        layout.separator()

        for prim in settings.prims:
            box = layout.box()
            header_row = box.row()
            header_row.label(text=prim.prim_path)

            box.template_list(
                "USD_UL_prim_ref_list",
                prim.prim_path,
                prim,
                "refs",
                prim,
                "active_ref_index",
                rows=3,
            )


CLASSES = (
    USD_UL_PrimRefList,
    USD_PT_PrimPrependedRefs,
)


def register() -> None:
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


