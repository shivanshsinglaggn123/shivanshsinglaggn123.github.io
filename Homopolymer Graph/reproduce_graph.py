"""Reproduce the slit-pore partition-coefficient graph.

The series used here is the slit-pore result from the supplied text:

    K(g, lambda) = sum[2 lambda**2 /
        (alpha_m**2 * (lambda**2 + alpha_m**2 + lambda))
        * exp(-alpha_m**2 * g**2)]

where the sum is over odd m and alpha_m satisfies

    alpha_m = arctan(lambda / alpha_m) + (m - 1) * pi / 2.

The first root is imaginary when lambda is negative.  The code evaluates
that root as alpha_1**2 = -beta**2, where beta*tanh(beta) = -lambda.
"""

import math

import matplotlib.pyplot as plt


def bisect(function, lower: float, upper: float, tolerance: float = 1e-12) -> float:
    """Find a zero of a continuous function between lower and upper."""
    lower_value = function(lower)
    upper_value = function(upper)
    if lower_value * upper_value > 0:
        raise ValueError("The root is not bracketed.")

    while upper - lower > tolerance:
        middle = (lower + upper) / 2
        middle_value = function(middle)
        if lower_value * middle_value <= 0:
            upper, upper_value = middle, middle_value
        else:
            lower, lower_value = middle, middle_value
    return (lower + upper) / 2


def root_squared(lambda_value: float, odd_m: int) -> float:
    """Return alpha_m**2 without needing a complex-number library."""
    if odd_m == 1 and lambda_value == 0:
        return 0.0

    if odd_m == 1 and lambda_value < 0:
        beta = bisect(
            lambda beta: beta * math.tanh(beta) + lambda_value,
            1e-12,
            math.sqrt(-lambda_value) + 2,
        )
        return -(beta**2)

    base = (odd_m - 1) * math.pi / 2
    angle = math.pi / 2
    if lambda_value > 0:
        lower = base + 1e-10
        upper = base + angle - 1e-10
    else:
        lower = base - angle + 1e-10
        upper = base - 1e-10

    def characteristic_root(alpha: float) -> float:
        return alpha - base - math.atan(lambda_value / alpha)

    alpha = bisect(characteristic_root, lower, upper)
    return alpha**2


def partition_coefficient(g: float, lambda_value: float, terms: int = 101) -> float:
    """Calculate K for pore-size parameter g and interaction lambda."""
    if lambda_value == 0:
        return 1.0

    total = 0.0
    for odd_m in range(1, terms + 1, 2):
        alpha_squared = root_squared(lambda_value, odd_m)
        denominator = alpha_squared * (
            lambda_value**2 + alpha_squared + lambda_value
        )
        term = 2 * lambda_value**2 / denominator
        total += term * math.exp(-alpha_squared * g**2)
    return total


def main() -> None:
    g_values = [index * 2.2 / 500 for index in range(501)]
    lambda_values = [50, 3, 0.1, 0, -0.1, -3]

    fig, ax = plt.subplots(figsize=(8, 6))
    label_positions = {50: 0.33, 3: 0.85, 0.1: 1.8, 0: 1.45, -0.1: 1.25, -3: 0.33}
    for lambda_value in lambda_values:
        k_values = [partition_coefficient(g, lambda_value) for g in g_values]
        ax.plot(g_values, k_values, color="black", linewidth=1.4)

        label_g = label_positions[lambda_value]
        label_k = partition_coefficient(label_g, lambda_value)
        if 0.05 < label_k < 3.05:
            ax.text(label_g, label_k, rf"$\lambda={lambda_value:g}$", fontsize=10)

    ax.set_xlim(0, 2.2)
    ax.set_ylim(0, 3.2)
    ax.set_xlabel("g = Rg / Rp", fontsize=12)
    ax.set_ylabel("K", fontsize=14, rotation=0, labelpad=12)
    ax.set_xticks([0, 1, 2])
    ax.set_yticks([0, 1, 2, 3])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_position(("data", 0))
    ax.spines["bottom"].set_position(("data", 0))
    ax.grid(False)
    fig.tight_layout()
    fig.savefig("reproduced_graph.png", dpi=200, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
