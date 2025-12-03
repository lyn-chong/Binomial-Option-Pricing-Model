"""
Two-asset portfolio frontier calculator and visualizer.

This script provides utilities to compute the expected return and standard deviation
for all portfolio allocations between two assets, and to plot the resulting
risk-return frontier.
"""

from __future__ import annotations

import argparse
from typing import Iterable, Tuple

import matplotlib.pyplot as plt
import numpy as np


def compute_two_asset_frontier(
    expected_returns: Iterable[float],
    standard_deviations: Iterable[float],
    correlation: float,
    num_points: int = 101,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute weights, expected returns, and standard deviations for a two-asset portfolio.

    Args:
        expected_returns: Iterable containing expected returns for the two assets.
        standard_deviations: Iterable containing standard deviations for the two assets.
        correlation: Correlation coefficient between the two assets (-1 to 1).
        num_points: Number of weight points to evaluate between 0 and 1.

    Returns:
        Tuple of (weights, portfolio_returns, portfolio_std_devs), each as numpy arrays.
    """

    mu = np.asarray(list(expected_returns), dtype=float)
    sigma = np.asarray(list(standard_deviations), dtype=float)

    if mu.shape != (2,) or sigma.shape != (2,):
        raise ValueError("expected_returns and standard_deviations must each have exactly two values")

    if not -1.0 <= correlation <= 1.0:
        raise ValueError("correlation must be between -1 and 1")

    if num_points < 2:
        raise ValueError("num_points must be at least 2 to span the weight range")

    weights = np.linspace(0.0, 1.0, num_points)
    w1 = weights
    w2 = 1 - weights

    portfolio_returns = w1 * mu[0] + w2 * mu[1]

    variance = (
        (w1 ** 2) * (sigma[0] ** 2)
        + (w2 ** 2) * (sigma[1] ** 2)
        + 2 * w1 * w2 * sigma[0] * sigma[1] * correlation
    )
    portfolio_std_devs = np.sqrt(variance)

    return weights, portfolio_returns, portfolio_std_devs


def plot_two_asset_frontier(
    expected_returns: Iterable[float],
    standard_deviations: Iterable[float],
    correlation: float,
    num_points: int = 101,
    output_path: str | None = None,
    show: bool = False,
):
    """
    Plot the risk-return frontier for a two-asset portfolio.

    Args:
        expected_returns: Iterable containing expected returns for the two assets.
        standard_deviations: Iterable containing standard deviations for the two assets.
        correlation: Correlation coefficient between the two assets (-1 to 1).
        num_points: Number of weight points to evaluate between 0 and 1.
        output_path: Optional path to save the generated plot.
        show: When True, displays the plot window (may not be available in all environments).
    """

    weights, portfolio_returns, portfolio_std_devs = compute_two_asset_frontier(
        expected_returns, standard_deviations, correlation, num_points
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    scatter = ax.scatter(
        portfolio_std_devs,
        portfolio_returns,
        c=weights,
        cmap="viridis",
        label="Weight in Asset 1",
    )
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Weight in Asset 1")

    ax.set_title("Two-Asset Portfolio Frontier")
    ax.set_xlabel("Portfolio Standard Deviation")
    ax.set_ylabel("Expected Portfolio Return")
    ax.grid(True, linestyle="--", alpha=0.6)

    # Mark the individual assets for reference.
    mu = list(expected_returns)
    sigma = list(standard_deviations)
    ax.scatter([sigma[0], sigma[1]], [mu[0], mu[1]], color="red", marker="x", zorder=5, label="Assets")
    ax.legend()

    if output_path:
        fig.savefig(output_path, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return weights, portfolio_returns, portfolio_std_devs


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot the expected return vs. standard deviation frontier for two assets.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mu",
        nargs=2,
        type=float,
        required=True,
        metavar=("MU1", "MU2"),
        help="Expected returns of the two assets.",
    )
    parser.add_argument(
        "--sigma",
        nargs=2,
        type=float,
        required=True,
        metavar=("SIGMA1", "SIGMA2"),
        help="Standard deviations of the two assets.",
    )
    parser.add_argument(
        "--correlation",
        type=float,
        required=True,
        help="Correlation coefficient between the two assets (-1 to 1).",
    )
    parser.add_argument(
        "--points",
        type=int,
        default=101,
        help="Number of weight points to evaluate between 0 and 1.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="portfolio_frontier.png",
        help="Path to save the generated plot image.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display the plot window instead of closing it (may not work in headless environments).",
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    plot_two_asset_frontier(
        expected_returns=args.mu,
        standard_deviations=args.sigma,
        correlation=args.correlation,
        num_points=args.points,
        output_path=args.output,
        show=args.show,
    )


if __name__ == "__main__":
    main()
