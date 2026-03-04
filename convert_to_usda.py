#convert_to_usda.py

"""Convenience script to convert a USD file to an explicit USDA file.
Just to use in the interim while working with many different files."""

from pxr import Usd

def convert_usd_to_usda(input_path: str, output_path: str = None) -> str:
    """
    Convert a USD file to an explicit USDA file.
    Args:
        input_path: The path to the USD file to convert.
        output_path: The path to the USDA file to create. If not provided, the output path will be the same as the input path with the .usdc extension replaced with .usda.
    Returns:
        The path to the USDA file that was created.
    Example:
    convert_usd_to_usda("my_asset.usdc") # outputs: my_asset.usda
    convert_usd_to_usda("my_asset.usdc", "output/my_asset_ascii.usda") # outputs: output/my_asset_ascii.usda
    """

    if output_path is None:
        output_path = input_path.rsplit(".", 1)[0] + ".usda"
    
    stage = Usd.Stage.Open(input_path)
    stage.Export(output_path)
    return output_path