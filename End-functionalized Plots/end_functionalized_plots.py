"""Calculate and plot homopolymer and end-functionalized partition coefficients."""

import math

import matplotlib.pyplot as plt


def bisect(function, lower: float, upper: float, tolerance: float = 1e-12) -> float:
    """Find a root of a continuous function by interval halving."""
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
    """Return alpha_m squared, including the imaginary-root limit for negative lambda."""
    if lambda_value == 0:
        base = (odd_m - 1) * math.pi / 2
        return base * base

    if odd_m == 1 and lambda_value < 0:
        beta = bisect(
            lambda beta: beta * math.tanh(beta) + lambda_value,
            1e-12,
            math.sqrt(-lambda_value) + 2,
        )
        return -(beta * beta)

    base = (odd_m - 1) * math.pi / 2
    angle = math.pi / 2
    if lambda_value > 0:
        lower = base + 1e-10
        upper = base + angle - 1e-10
    else:
        lower = base - angle + 1e-10
        upper = base - 1e-10

    def characteristic_root(alpha):
        return alpha - base - math.atan(lambda_value / alpha)

    alpha = bisect(characteristic_root, lower, upper)
    return alpha * alpha


def K_homopolymer(g: float, lambda_value: float, terms: int = 101) -> float:
    """Equation for the ordinary homopolymer partition coefficient."""
    if lambda_value == 0:
        return 1.0

    total = 0.0
    for odd_m in range(1, terms + 1, 2):
        alpha_squared = root_squared(lambda_value, odd_m)
        denominator = alpha_squared * (
            lambda_value * lambda_value + alpha_squared + lambda_value
        )
        term = 2 * lambda_value * lambda_value / denominator
        total += term * math.exp(-alpha_squared * g * g)
    return total


def U1(lambda_value: float, g: float, terms: int = 101) -> float:
    """One-end contact probability from Eq. 9."""
    if lambda_value == 0:
        return 0.0

    total = 0.0
    for odd_m in range(1, terms + 1, 2):
        alpha_squared = root_squared(lambda_value, odd_m)
        denominator = lambda_value + lambda_value * lambda_value + alpha_squared
        term = 2 * lambda_value / denominator
        total += term * math.exp(-alpha_squared * g * g)
    return total


def U2(lambda_value: float, g: float, terms: int = 101) -> float:
    """Two-end contact probability from Eq. 10."""
    if lambda_value == 0:
        # At lambda=0, the first root has alpha_1^2=0 and Ak has limit 2.
        total = 2.0
        odd_modes = range(3, terms + 1, 2)
    else:
        total = 0.0
        odd_modes = range(1, terms + 1, 2)

    for odd_m in odd_modes:
        alpha_squared = root_squared(lambda_value, odd_m)
        denominator = lambda_value + lambda_value * lambda_value + alpha_squared
        term = 2 * alpha_squared / denominator
        total += term * math.exp(-alpha_squared * g * g)
    return total


def K_singly_functionalized(g: float, lambda_value: float, q_a: float, terms: int = 101) -> float:
    """Eq. 3: K(1) = K(0) + q_a p_a."""
    return K_homopolymer(g, lambda_value, terms) + q_a * U1(lambda_value, g, terms)


def K_doubly_functionalized(
    g: float, lambda_value: float, q_a: float, q_b: float, terms: int = 101
) -> float:
    """Eq. 4: K(2) = K(0) + q_a p_a + q_b p_b + q_a q_b p_ab."""
    p_a = U1(lambda_value, g, terms)
    p_b = p_a
    return (
        K_homopolymer(g, lambda_value, terms)
        + q_a * p_a
        + q_b * p_b
        + q_a * q_b * U2(lambda_value, g, terms)
    )


def chain_length_to_g(chain_length: int, b_over_d: float = 1.0) -> float:
    """Convert chain length N to g=R/d using R=b sqrt(N/6)."""
    return math.sqrt(chain_length / 6.0) * b_over_d


def main() -> None:
    g_values = [index * 2.2 / 500 for index in range(501)]
    lambda_value = 0.1
    # Demonstration values; change them to model the strength of each functional end.
    q_a = 0.5
    q_b = 0.5

    fig, ax = plt.subplots(figsize=(8, 6))
    homopolymer = [K_homopolymer(g, lambda_value) for g in g_values]
    single = [K_singly_functionalized(g, lambda_value, q_a) for g in g_values]
    double = [K_doubly_functionalized(g, lambda_value, q_a, q_b) for g in g_values]
    ax.plot(g_values, homopolymer, label="Homopolymer", linewidth=2)
    ax.plot(g_values, single, label="One end functionalized", linewidth=2)
    ax.plot(g_values, double, label="Both ends functionalized", linewidth=2)
    ax.set_xlabel("g = Rg / Rp", fontsize=12)
    ax.set_ylabel("K", fontsize=12, rotation=0, labelpad=12)
    ax.set_title(r"$K$ versus $g$ at $\lambda = 0.1$; $q_a=q_b=0.5$")
    ax.set_xlim(0, 2.2)
    ax.set_ylim(bottom=0)
    ax.legend()
    fig.tight_layout()
    fig.savefig("singly_doubly_functionalized_K_vs_g.png", dpi=200, bbox_inches="tight")

    chain_lengths = list(range(1, 501))
    b_over_d = 1.0
    g_chain = [chain_length_to_g(n, b_over_d) for n in chain_lengths]

    lambda_value = 0.1
    fig, ax = plt.subplots(figsize=(8, 6))
    homopolymer = [K_homopolymer(g, lambda_value) for g in g_chain]
    single = [K_singly_functionalized(g, lambda_value, q_a) for g in g_chain]
    double = [K_doubly_functionalized(g, lambda_value, q_a, q_b) for g in g_chain]
    ax.plot(chain_lengths, homopolymer, label="Homopolymer", linewidth=2)
    ax.plot(chain_lengths, single, label="One end functionalized", linewidth=2)
    ax.plot(chain_lengths, double, label="Both ends functionalized", linewidth=2)
    ax.set_xlabel("Chain length N", fontsize=12)
    ax.set_ylabel("K", fontsize=12, rotation=0, labelpad=12)
    ax.set_title(r"$K$ versus chain length; $\lambda=0.1$; $q_a=q_b=0.5$")
    ax.legend()
    fig.tight_layout()
    fig.savefig("singly_doubly_functionalized_K_vs_N.png", dpi=200, bbox_inches="tight")


if __name__ == "__main__":
    main()
