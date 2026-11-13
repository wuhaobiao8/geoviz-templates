"""geoviz_templates: publication-quality figure templates for geoscience papers."""

from .style import (
    PALETTE, GRADE_CMAP, DIVERGE_CMAP, CONT_CMAP,
    use_style, panel_label, event_line,
)

__version__ = "0.1.0"
__all__ = [
    "PALETTE", "GRADE_CMAP", "DIVERGE_CMAP", "CONT_CMAP",
    "use_style", "panel_label", "event_line",
]
