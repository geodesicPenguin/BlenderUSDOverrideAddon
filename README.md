# BlenderUSDOverrideAddon: Edit the Sublayer of a USDA file.
A tool simply for proof of concept. 


### What it does:
USD files have a hierarchy of "opinions" that tells the DCC how the output should display. 
This is a really simple editor for Blender to modify filepaths within a USDA sublayer to change which opinion gets output.
IE: I have 2 separate animation caches referenced in the sublayers of my USDA
```
subLayer = [ run_animation.usdc, jump_animation.usdc]
```
I can change which animation the USD data will play by affecting the order of this list.


# UI
Once installed the addon appears in the N panel.

# Why USD is Better than Alembic for Animation Caching
Let's say we have a shot set up in Maya that has some characters and a few props, all animated. We want to bring those into Blender as caches so that we can light and render. We could use Alembic or USD to export all these assets in one file or in a file for each asset and the result would be identical. But the differences appear once you must *edit* the assets later on. What if we must change UVs later? What if we want to iterate thru different animation cache data per asset? What if an asset has updated geometry (new vertex IDs)? There are new objects in some of the assets -- how do we bring those into Blender without re-importing what we already have?

The "live link" USD feature I mentioned really shines here. Instead of re-exporting our alembic(s) with new changes and having to carefully redo old organizational tasks on re-import, we write an organized .USDA file. It'd have prim definitions clearly laid out for each asset. Then in those definitions we write our prepended references. And in those prepended references we reference the USD files for the models and animation. So if we want to update some UVs, swap out old geo, try out new animation sequences, etc. we can do that. We'd be taking advantage of USD's hierarchy system. 

Again though, Blender doesn't truly take advantage of USD. So we can't expect updating the stage of our USDA file in something like Houdini to then perfectly propagate in Blender. The most annoying case being when adding in new objects somewhere in our USD hierarchy and not having them automatically appear in Blender's outliner. The temporary fix for this would be to write a tool to query lists of objects found in the USD stage and currently in Blender, then subtract the lists and use the resulting list as an argument in the Blender USD importer to bring in only the missing objects.
