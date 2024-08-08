import subprocess
from typing import Optional

import matplotlib.pyplot as plt

from tfds.log import create_logger

plt.rcParams["font.size"] = 12
plt.rcParams["mathtext.fontset"] = "cm"  # Use CM for math font.
plt.rcParams["figure.autolayout"] = True  # Use tight layouts.

logger = create_logger(__name__)


def use_tex() -> None:
    if subprocess.call("which latex", shell=True) == 0:
        plt.rcParams["text.usetex"] = True
    else:
        logger.info(
            "No LaTeX installation found, so LaTeX will not be used to render `matplotlib` figures."
        )


def prettify(
    legend: Optional[bool] = None,
    legend_loc: Optional[str] = None,
    spines: Optional[bool] = True,
    ticks: Optional[bool] = True,
    ax: Optional[bool] = None,
) -> None:
    """Tweak a plot.

    Args:
        legend (bool, optional): Show a legend if any labels are set.
        legend_loc (str, optional): Position of the legend. Defaults to "upper right".
        spines (bool, optional): Hide top and right spine. Defaults to `True`.
        ticks (bool, optional): Hide top and right ticks. Defaults to `True`.
        ax (axis, optional): Axis to tune. Defaults to `plt.gca()`.
    """

    if legend_loc is None:
        legend_loc = "upper right"

    if ax is None:
        ax = plt.gca()

    if legend is None:
        legend = len(ax.get_legend_handles_labels()[0]) > 0

    if legend:
        leg = ax.legend(
            facecolor="#eeeeee",
            edgecolor="#ffffff",
            framealpha=0.85,
            loc=legend_loc,
            labelspacing=0.25,
        )
        leg.get_frame().set_linewidth(0)

    if spines:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_lw(1)
        ax.spines["left"].set_lw(1)

    if ticks:
        ax.xaxis.set_ticks_position("bottom")
        ax.xaxis.set_tick_params(width=1)
        ax.yaxis.set_ticks_position("left")
        ax.yaxis.set_tick_params(width=1)
