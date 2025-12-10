# Fycus

Easy scientific figure generation with matplotlib.

## Why Fycus?

Fycus simplifies the process of creating publication-ready scientific figures by solving common pain points:

- **Standardized figure formatting**: Apply consistent, professional styling to all your matplotlib figures without repeating configuration code
- **Centralized figure storage**: Always save figures to the same location without thinking about it
- **No more complicated paths**: Skip dealing with long, nested file paths every time you save a figure

With Fycus, you can focus on your data and visualizations instead of wrestling with matplotlib configuration and file paths.
**Note: by default, fycus saves figures as .svg files which can be opened in [Inkscape](https://inkscape.org/release/inkscape-1.4.2/windows/64-bit/msi/dl/) and then powerfully refined and/or combined into larger scientific figures**

## Installation

Clone the repository and install with pip:

```bash
git clone https://github.com/jbmelander/fycus.git
cd fycus
pip install .
```

After installation, run the configuration wizard to set your default figure directory:

```bash
fycus init
```

This will prompt you to choose where figures should be saved by default. You can always override this on a per-project basis.

## Example Usage

```python
import matplotlib.pyplot as plt
from fycus import Fycus

# Create a figure manager for this project
# Now, all figures from this script will be saved to YOUR_DEFAULT_FYCUS_PATH / my_project / savename.svg
F = Fycus('my_project')

# Create your plot
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('My Plot')

# Set figure size using convenient presets
F.QQ()  # Quarter-quarter (1/4 width, 1/4 height)

# Save with automatic formatting
F.save('my_plot')  # Saves as SVG by default
```

### Size Presets

Fycus provides several convenient size presets based on page width fractions. The page width can be set when creating the Fycus option, but standardizes as a standard paper size with a one-inch margin:

```python
F.QQ()  # Quarter-quarter: 1/4 width, 1/4 height
F.QT()  # Quarter-third: 1/3 width, 1/4 height
F.QH()  # Quarter-half: 1/2 width, 1/4 height
F.FQ()  # Fifth-quarter: 1/4 width, 1/5 height
F.XX(height=0.3, width=0.5)  # Custom size as fractions
```

### Output Formats

Choose your preferred output format:

```python
# SVG (default) - great for Inkscape and vector graphics
F = Fycus('my_project', extension='svg')

# PNG - for raster graphics with white background
F = Fycus('my_project', extension='png')
```

### Custom Base Path

Override the default base path for specific projects:

```python
F = Fycus('my_project', base_path='/path/to/custom/directory')
```

### Style Customization

Fycus automatically applies professional styling when imported, but you can also use the style function directly:

```python
from fycus import setup_figure_style, COLORS

# Apply default styling
setup_figure_style()

# Use the color palette
plt.plot(x, y, color=COLORS['primary'])
plt.plot(x, z, color=COLORS['secondary'])
```
