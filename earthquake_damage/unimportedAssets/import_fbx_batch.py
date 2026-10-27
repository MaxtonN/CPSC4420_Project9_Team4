import os
import unreal

# Folder containing the downloaded asset-pack folders.
SOURCE_DIR = r"F:\Unreal Projects\earthquake_damage\unimportedAssets"

# Unreal virtual Content Browser path, NOT a Windows filesystem path.
DESTINATION_ROOT = "/Game/DisasterAssets"

if not os.path.isdir(SOURCE_DIR):
    raise RuntimeError(f"Source directory does not exist: {SOURCE_DIR}")

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
fbx_files = []

for root, dirs, files in os.walk(SOURCE_DIR):
    dirs.sort()
    for filename in sorted(files):
        if filename.lower().endswith(".fbx"):
            fbx_files.append(os.path.join(root, filename))

unreal.log(f"Found {len(fbx_files)} FBX files.")

success = 0
failed = []

for index, filename in enumerate(fbx_files, start=1):
    # Preserve the asset-pack folder, without copying the entire source path.
    relative = os.path.relpath(filename, SOURCE_DIR)
    pack_folder = relative.split(os.sep)[0]
    destination = f"{DESTINATION_ROOT}/{pack_folder}"

    unreal.EditorAssetLibrary.make_directory(destination)

    task = unreal.AssetImportTask()
    task.filename = filename
    task.destination_path = destination
    task.automated = True
    task.save = True
    task.replace_existing = False

    options = unreal.FbxImportUI()
    options.import_mesh = True
    options.import_as_skeletal = False
    options.import_materials = True
    options.import_textures = True
    task.options = options

    unreal.log(f"[{index}/{len(fbx_files)}] {filename}")

    asset_tools.import_asset_tasks([task])

    if task.imported_object_paths:
        success += 1
        unreal.log(f"Imported: {task.imported_object_paths}")
    else:
        failed.append(filename)
        unreal.log_warning(f"No assets imported: {filename}")

unreal.log(f"Finished. Successful FBX files: {success}")
unreal.log(f"Files with no reported import: {len(failed)}")

for filename in failed:
    unreal.log_warning(f"Review: {filename}")