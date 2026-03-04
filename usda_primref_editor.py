"""Edit USDA files that consist only of root-layer sublayers.

This module provides a small helper around ``Sdf.Layer`` that focuses
exclusively on reading and writing the root layer's ``subLayerPaths``
(sublayer file paths). It intentionally does **not** deal with prims,
references, or other composition arcs.
"""

from typing import List, Optional

from pxr import Sdf


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


def get_sublayer_paths(usda_path: str) -> List[str]:
    """Return the root layer's subLayerPaths (sublayer file paths) for the USDA file."""
    
    layer = Sdf.Layer.FindOrOpen(usda_path)
    if layer is None:
        raise RuntimeError(f"Could not open USD layer: {usda_path}")

    layer.Reload()
    return list(layer.subLayerPaths)