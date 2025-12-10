"""Scientific figure styling and management for matplotlib."""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
from .config import get_base_path


CMAP = 'PiYG'


def setup_figure_style():
    """Configure matplotlib for consistent, publication-ready figures."""
    # Set default font to be a sans-serif font
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['font.sans-serif'] = [
        'DejaVu Sans',
        'Arial',
        'Liberation Sans',
        'Bitstream Vera Sans',
        'sans-serif'
    ]

    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 11

    # Line and marker settings
    plt.rcParams['lines.linewidth'] = 1.5
    plt.rcParams['lines.markersize'] = 6
    plt.rcParams['patch.linewidth'] = 1.0

    # Axes and grid
    plt.rcParams['axes.linewidth'] = 1.5
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['xtick.major.width'] = 1.0
    plt.rcParams['ytick.major.width'] = 1.0
    plt.rcParams['grid.linewidth'] = 0.5

    plt.rcParams['axes.prop_cycle'] = mpl.cycler(
        color=['k', 'b', 'c', 'r', 'm', 'g', 'y']
    )

    # Figure settings
    plt.rcParams['figure.dpi'] = 150
    plt.rcParams['savefig.dpi'] = 150
    plt.rcParams['savefig.bbox'] = 'tight'
    plt.rcParams['savefig.pad_inches'] = 0.1

    # SVG-specific settings for Inkscape compatibility
    plt.rcParams['svg.fonttype'] = 'none'  # Keep text as text (not paths)


class Fycus:
    """Utility class for managing scientific figures with matplotlib.

    Provides convenient sizing presets and automated figure exporting
    with format-specific optimizations.

    Parameters
    ----------
    name : str
        Directory name within base_path where figures will be saved.
    base_path : str or Path, optional
        Base directory for figure storage. Defaults to current working directory.
    extension : str, optional
        Output format ('svg' or 'png'). Defaults to 'svg'.
    width : float, optional
        Base figure width in inches. Defaults to 7.0.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from fycus import Fycus
    >>> F = Fycus('my_figures')
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [1, 2, 3])
    >>> F.QQ()  # Set to quarter-page size
    >>> F.save('my_plot')
    """

    def __init__(
        self,
        name,
        base_path=None,
        extension='svg',
        width=7.0
    ):
        self.extension = extension
        self._QQ = (width / 4, width / 4)
        self._QT = (width / 3, width / 4)
        self._QH = (width / 2, width / 4)
        self._FQ = (width / 4, width / 5)

        self.page_width = width
        self._size_set = False

        # Priority: constructor param > config file > os.getcwd()
        if base_path is None:
            config_base = get_base_path()  # Try loading from config
            base_path = config_base if config_base else os.getcwd()
        base_path = Path(base_path)

        self.save_dir = base_path / name
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def FQ(self):
        """Set figure to fifth-quarter size (1/5 height, 1/4 width)."""
        plt.gcf().set_size_inches(self._FQ)
        self._size_set = True

    def QQ(self):
        """Set figure to quarter-quarter size (1/4 height and width)."""
        plt.gcf().set_size_inches(self._QQ)
        self._size_set = True

    def QT(self):
        """Set figure to quarter-third size (1/4 height, 1/3 width)."""
        plt.gcf().set_size_inches(self._QT)
        self._size_set = True

    def QH(self):
        """Set figure to quarter-half size (1/4 height, 1/2 width)."""
        plt.gcf().set_size_inches(self._QH)
        self._size_set = True

    def XX(self, height, width):
        """Set figure to custom size.

        Parameters
        ----------
        height : float
            Height as a fraction of page_width.
        width : float
            Width as a fraction of page_width.
        """
        width_inches = width * self.page_width
        height_inches = height * self.page_width
        plt.gcf().set_size_inches((width_inches, height_inches))
        self._size_set = True

    def save(self, filename, dpi=None, **kwargs):
        """Save the current figure to file.

        Automatically adds the configured extension if not present.
        Applies format-specific optimizations (SVG for Inkscape, PNG with
        white background).

        Parameters
        ----------
        filename : str
            Base filename without extension (extension will be added automatically).
        dpi : int, optional
            Dots per inch for output. Defaults to 100 for SVG, 300 for PNG.
        **kwargs
            Additional keyword arguments passed to matplotlib's savefig().

        Returns
        -------
        Path
            The full path where the figure was saved.
        """
        fig = plt.gcf()

        # Add extension if not present
        if '.' not in filename:
            filename = f"{filename}.{self.extension}"
            extension = self.extension
        else:
            extension = filename.split('.')[-1]

        output_path = self.save_dir / filename

        # Set default DPI based on format
        if dpi is None:
            dpi = 100 if extension == 'svg' else 300

        # Format-specific save parameters
        if extension == 'svg':
            save_params = {
                'format': extension,
                'bbox_inches': 'tight',
                'pad_inches': 0.1,
                'edgecolor': 'none'
            }
        elif extension == 'png':
            save_params = {
                'format': extension,
                'bbox_inches': 'tight',
                'facecolor': 'white',
                'edgecolor': 'none',
            }
        else:
            save_params = {'format': extension}

        # Apply default size if no preset was called
        if not self._size_set:
            self.QQ()

        # Merge with user-provided parameters
        save_params.update(kwargs)

        fig.savefig(str(output_path), dpi=dpi, **save_params)
        plt.close(fig)

        print(f'Saved to {output_path} (dpi={dpi})')

        return output_path


# Color palette for consistent styling
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'neutral': '#C73E1D',
    'gray': '#6B7280',
    'light_gray': '#D1D5DB',
    'black': '#1F2937'
}


# Apply default styling on module import
setup_figure_style()
