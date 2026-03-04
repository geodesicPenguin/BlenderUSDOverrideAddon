import bpy
import bpy.types as bt

from . import properties as prop


class USD_UL_SublayerList(bt.UIList):
    """List of root-layer sublayer filepaths for a USDA file."""

    bl_idname = "USD_UL_sublayer_list"

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
        sub: prop.USDSublayerItem = item
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            layout.label(text=sub.filepath or "<empty>")
        elif self.layout_type == "GRID":
            layout.alignment = "CENTER"
            layout.label(text=str(index))


class USD_PT_UsdaSublayers(bt.Panel):
    """Panel in the 3D Viewport sidebar to show and edit USDA root-layer sublayers."""

    bl_label = "USD Sublayers"
    bl_idname = "USD_PT_usd_sublayers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "USD Sublayers"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings: prop.USDSublayerSettings = scene.usd_sublayer_settings

        layout.prop(settings, "usda_path")

        row = layout.row(align=True)
        row.operator("usd_sublayers.scan", icon="FILE_REFRESH")

        if not settings.sublayers:
            layout.separator()
            layout.label(text="No sublayers found.")
            return

        layout.separator()

        layout.template_list(
            "USD_UL_sublayer_list",
            "sublayers",
            settings,
            "sublayers",
            settings,
            "active_sublayer_index",
            rows=6,
        )

        controls_row = layout.row(align=True)
        move_up = controls_row.operator(
            "usd_sublayers.move_item",
            text="",
            icon="TRIA_UP",
        )
        move_up.direction = "UP"

        move_down = controls_row.operator(
            "usd_sublayers.move_item",
            text="",
            icon="TRIA_DOWN",
        )
        move_down.direction = "DOWN"

        controls_row.separator()

        controls_row.operator(
            "usd_sublayers.save",
            text="Save Sublayer Order",
            icon="FILE_TICK",
        )


CLASSES = (
    USD_UL_SublayerList,
    USD_PT_UsdaSublayers,
)


def register() -> None:
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


