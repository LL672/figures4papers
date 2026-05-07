import csv
import math
import os
from statistics import mean

from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.patches import Patch
from matplotlib.colors import to_rgb


def load_weights(csv_path):
    labels = []
    time_vals = []
    freq_vals = []
    sax_vals = []

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            norm = {(k.strip().lower() if isinstance(k, str) else k): v for k, v in row.items()}
            labels.append(norm["label"])
            time_vals.append(float(norm["time"]))
            freq_vals.append(float(norm["freq"]))
            sax_vals.append(float(norm["sax"]))

    return labels, time_vals, freq_vals, sax_vals


def normalized_entropy(t, f, s):
    vals = [max(1e-12, t), max(1e-12, f), max(1e-12, s)]
    h = -sum(v * math.log(v) for v in vals)
    return h / math.log(3.0)


def barycentric_to_cartesian(t, f, s):
    # Triangle vertices: time=(0,0), freq=(1,0), sax=(0.5,sqrt(3)/2)
    x = f + 0.5 * s
    y = (math.sqrt(3.0) / 2.0) * s
    return x, y


def lighten(color_hex, amount):
    """Blend a color with white. amount in [0,1], larger -> closer to original color."""
    r, g, b = to_rgb(color_hex)
    return (
        1.0 - (1.0 - r) * amount,
        1.0 - (1.0 - g) * amount,
        1.0 - (1.0 - b) * amount,
    )

def draw_gradient_bar(ax, x, bottom, height, base_color, width=0.75):
    """Draw a single bar segment with a vertical gradient."""
    if height <= 0:
        return
    steps = 50
    dh = height / steps
    for i in range(steps):
        # dist_from_center is 0 at the middle, 1 at the edges
        dist_from_center = abs(i - (steps - 1) / 2.0) / ((steps - 1) / 2.0)
        # Center is dark (amount=1.0), edges are lighter (amount=0.3)
        amount = 1.0 - 0.7 * dist_from_center
        color = lighten(base_color, amount)
        ax.bar(x, dh, bottom=bottom + i * dh, color=color, width=width, edgecolor="none", linewidth=0)


def plot_evidence(labels, time_vals, freq_vals, sax_vals, save_path):
    colors = {
        # Match the reference style: time=blue, freq=green, sax=purple.
        "time": "#7FA4C8",
        "freq": "#8DBA9B",
        "sax": "#A695BF",
    }

    entropies = [normalized_entropy(t, f, s) for t, f, s in zip(time_vals, freq_vals, sax_vals)]

    fig = plt.figure(figsize=(10, 6), facecolor="white")

    # Panel A: class-wise stacked bars
    ax1 = fig.add_subplot(1, 1, 1)
    x = list(range(len(labels)))

    n = len(labels)
    bottoms = [0.0] * n
    for idx in range(n):
        # time
        h_t = time_vals[idx]
        draw_gradient_bar(ax1, idx, bottoms[idx], h_t, colors["time"])
        bottoms[idx] += h_t

        # freq
        h_f = freq_vals[idx]
        draw_gradient_bar(ax1, idx, bottoms[idx], h_f, colors["freq"])
        bottoms[idx] += h_f

        # sax
        h_s = sax_vals[idx]
        draw_gradient_bar(ax1, idx, bottoms[idx], h_s, colors["sax"])

    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=11)
    ax1.set_ylim(0.0, 1.02)
    ax1.set_ylabel("Weight", fontsize=14)
    # ax1.set_title("Class-wise Stacked Domain Weights", fontsize=16, pad=10)
    ax1.grid(axis="y", linestyle="--", alpha=0.35)
    ax1.legend(
        handles=[
            Patch(facecolor=colors["time"], label="time"),
            Patch(facecolor=colors["freq"], label="freq"),
            Patch(facecolor=colors["sax"], label="sax"),
        ],
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        ncol=1,
        frameon=False,
        fontsize=12,
    )

    fig.tight_layout()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.savefig(save_path, dpi=320, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False

    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "class_domain_weights_seed42.csv")
    out_path = os.path.join(base_dir, "figures", "domain_weight_evidence_panels.png")

    labels_, time_, freq_, sax_ = load_weights(csv_path)
    plot_evidence(labels_, time_, freq_, sax_, out_path)
    print(f"Figure saved to: {out_path}")
