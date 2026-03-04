"""Edit USDA files: prepended references per prim and root-layer sublayers."""

from typing import List, Optional

from pxr import Sdf


class UsdPrimRefEditor:
    """Edits prepended references on a single prim in a USDA layer."""

    def __init__(self, usda_path: str, prim_path: str):
        """Open the given USDA file and target the prim at prim_path (e.g. '/robotCharComp')."""
        
        self.usda_path: str = str(usda_path)
        self.prim_path: str = prim_path if prim_path.startswith("/") else f"/{prim_path}"
        self._layer: Optional[Sdf.Layer] = None


    def _get_layer(self) -> Sdf.Layer:
        """Return the Sdf layer for the USDA file, reloading from disk so data is current."""
        
        if self._layer is None:
            layer = Sdf.Layer.FindOrOpen(self.usda_path)
            if layer is None:
                raise RuntimeError(f"Could not open USD layer: {self.usda_path}")

            self._layer = layer

        self._layer.Reload()
        return self._layer


    def _get_prim_spec(self) -> Sdf.PrimSpec:
        """Return the Sdf.PrimSpec for this editor's prim path."""
        
        layer = self._get_layer()
        prim_spec = layer.GetPrimAtPath(Sdf.Path(self.prim_path))
        if prim_spec is None:
            raise RuntimeError(f"Could not find prim at path: {self.prim_path}")

        return prim_spec


    def load_primrefs(self) -> List[str]:
        """Return the ordered list of asset paths from this prim's prepended references."""
        
        
        prim_spec = self._get_prim_spec()
        ref_list_op = prim_spec.referenceList

        if ref_list_op is None:
            return []

        prepended_refs = list(ref_list_op.prependedItems)

        return [ref.assetPath for ref in prepended_refs]


    def save_primrefs(self, new_order: List[str]) -> None:
        """Set this prim's prepended reference order to new_order (list of asset paths) and save the layer."""
        
        prim_spec = self._get_prim_spec()
        ref_list_op = prim_spec.referenceList

        if ref_list_op is None:
            raise RuntimeError("Prim has no references to reorder.")

        original_refs = list(ref_list_op.prependedItems)

        if not original_refs and new_order:
            raise RuntimeError("No prepended references found on prim.")

        # Build a reordered list by walking the original references and matching
        # each path in new_order in sequence. This preserves duplicates and the
        # original Sdf.Reference objects.
        used_indices: set[int] = set()
        reordered_refs: list[Sdf.Reference] = []

        for path in new_order:
            found_index: int | None = None

            for idx, ref in enumerate(original_refs):
                if idx in used_indices:
                    continue
                if ref.assetPath == path:
                    found_index = idx
                    reordered_refs.append(ref)
                    used_indices.add(idx)
                    break

            if found_index is None:
                raise RuntimeError(f"Unknown reference path in new_order: {path}")

        # Assign a new ReferenceListOp back to the prim spec so the change is
        # actually written to the layer. Construct the op first, then set
        # prependedItems to avoid signature mismatches in some USD builds.
        new_list_op = Sdf.ReferenceListOp()
        new_list_op.prependedItems = reordered_refs
        prim_spec.referenceList = new_list_op

        layer = self._get_layer()
        layer.Save()


# ---------------------------------------------------------------------------
# Sublayers (root layer subLayerPaths) for files that use only sublayers
# ---------------------------------------------------------------------------


class UsdaSublayerEditor:
    """Edits the root layer's subLayerPaths (sublayers) in a USDA file."""

    def __init__(self, usda_path: str):
        """Open the given USDA file for sublayer read/write."""
        
        
        self.usda_path: str = str(usda_path)
        self._layer: Optional[Sdf.Layer] = None


    def _get_layer(self) -> Sdf.Layer:
        """Return the Sdf layer for the USDA file, reloading from disk so data is current."""
        
        
        if self._layer is None:
            layer = Sdf.Layer.FindOrOpen(self.usda_path)
            if layer is None:
                raise RuntimeError(f"Could not open USD layer: {self.usda_path}")

            self._layer = layer

        self._layer.Reload()
        return self._layer


    def load_sublayers(self) -> List[str]:
        """Return the current sublayer paths (subLayerPaths) of the root layer."""
        
        
        layer = self._get_layer()
        return list(layer.subLayerPaths)


    def save_sublayers(self, new_order: List[str]) -> None:
        """Set the root layer's subLayerPaths to new_order and save the USDA file."""
        
        
        layer = self._get_layer()
        layer.subLayerPaths = list(new_order)
        layer.Save()


def get_prim_paths_with_prepended_refs(usda_path: str) -> List[str]:
    """Return all prim paths in the layer that have at least one prepended reference."""
    
    
    layer = Sdf.Layer.FindOrOpen(usda_path)
    if layer is None:
        raise RuntimeError(f"Could not open USD layer: {usda_path}")

    layer.Reload()

    result: List[str] = []
    stack: List[Sdf.PrimSpec] = list(layer.rootPrims)

    while stack:
        spec = stack.pop()
        ref_list_op = spec.referenceList
        if ref_list_op is not None and list(ref_list_op.prependedItems):
            result.append(str(spec.path))

        for child in spec.nameChildren:
            stack.append(child)

    return result