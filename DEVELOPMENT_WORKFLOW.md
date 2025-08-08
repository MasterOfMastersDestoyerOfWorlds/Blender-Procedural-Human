# Development Workflow

## 🚀 Quick Start

### Method 1: Simple Install (Recommended)
```bash
python install.py
```
- Copies files to Blender's addon directory
- No waiting for input
- Works from command line/terminal

### Method 2: Auto Install + Reload (In Blender)
1. Open Blender
2. Go to **Scripting** workspace
3. Open `auto_install_reload.py`
4. Press **Alt+P** or click **Run Script**
5. Addon is automatically installed AND reloaded!

### Method 3: Hot Reload Only (When addon already installed)
1. Open Blender  
2. Go to **Scripting** workspace
3. Open `quick_reload.py`
4. Press **Alt+P** or click **Run Script**

## 🛠️ Development Commands

```bash
# Format code
python dev.py format

# Check code quality  
python dev.py lint

# Create distribution zip
python dev.py package

# Install to Blender
python dev.py install

# Do everything
python dev.py all
```

## 📦 Packaging Options

### **Simple Packaging (Recommended)**
```bash
python package.py
```
Creates `procedural_human.zip` ready for Blender installation.

### **Via Development Tools**
```bash
python dev.py package
```
Same as above but integrated with other dev tools.

### **Via UV Build System**
```bash
uv build
```
Creates wheel and source distributions (advanced usage).

## 📋 Typical Workflow

1. **Make changes** to code in `procedural_human/`
2. **Install**: Run `python install.py`  
3. **Enable in Blender**: Go to Preferences > Add-ons > Search "Procedural Human" > Enable
4. **Test**: Use the addon in Blender
5. **For quick updates**: Use `auto_install_reload.py` in Blender's scripting workspace

## 🔧 Files Explained

- `install.py` - Simple, fast installer (no user interaction)
- `auto_install_reload.py` - Run inside Blender for install + reload
- `quick_reload.py` - Run inside Blender for reload only
- `dev.py` - Development tools (format, lint, install)
- `install_and_reload.py` - Old script (deprecated)

## ✅ Benefits

- **No more waiting** for user input
- **No need to restart Blender** (use auto_install_reload.py)
- **Fast development cycle** with hot reloading
- **Professional code formatting** and linting
