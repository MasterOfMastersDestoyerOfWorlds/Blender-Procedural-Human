"""
Package the Procedural Human Generator addon for distribution
Creates a clean zip file ready for Blender installation
"""

import os
import zipfile
from pathlib import Path


def create_addon_package():
    """Create a zip package of the addon"""
    project_root = Path(__file__).parent
    source_dir = project_root / "procedural_human"
    output_file = project_root / "procedural_human.zip"

    print("📦 Packaging Procedural Human Generator...")
    print(f"📁 Source: {source_dir}")
    print(f"📁 Output: {output_file}")

    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return False

    if output_file.exists():
        output_file.unlink()
        print("🗑️ Removed existing package")

    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:

        for file_path in source_dir.glob("*.py"):
            if file_path.is_file():

                arcname = f"procedural_human/{file_path.name}"
                zipf.write(file_path, arcname)
                print(f"✅ Added {file_path.name}")

    print(f"🎉 Package created successfully: {output_file}")
    print(f"📊 File size: {output_file.stat().st_size / 1024:.1f} KB")

    print("\n📋 Installation Instructions:")
    print("1. Open Blender")
    print("2. Go to Edit > Preferences > Add-ons")
    print("3. Click 'Install...'")
    print("4. Select the procedural_human.zip file")
    print("5. Enable the addon")

    return True


if __name__ == "__main__":
    success = create_addon_package()
    if not success:
        exit(1)
