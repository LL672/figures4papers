import os
import numpy as np
from matplotlib import pyplot as plt

def plot_metrics_comparison(save_path):
    # Data from the table
    metrics = ['Test Accuracy', 'Test Balanced\nAccuracy', 'Test MCC', 'Test Macro-F1']
    methods = ['single_time', 'single_freq', 'single_sax', 'Fusion']
    
    data = {
        'single_time': [0.9716, 0.9590, 0.9684, 0.9621],
        'single_freq': [0.9786, 0.9812, 0.9764, 0.9820],
        'single_sax': [0.9643, 0.9596, 0.9604, 0.9644],
        'Fusion': [0.9929, 0.9923, 0.9921, 0.9933]
    }
    
    colors = {
        'single_time': '#D4D4D4',
        'single_freq': '#E6E1A8',
        'single_sax': '#E8D0D4',
        'Fusion': '#3D77B6'
    }

    fig, ax = plt.subplots(figsize=(10, 7), facecolor='white')
    
    x = np.arange(len(metrics))
    width = 0.10
    gap = 0.03
    step = width + gap
    
    offsets = [-1.5 * step, -0.5 * step, 0.5 * step, 1.5 * step]
    
    for i, method in enumerate(methods):
        ax.bar(
            x + offsets[i], 
            data[method], 
            width, 
            label=method, 
            color=colors[method],
            edgecolor='none'
        )

    ax.set_ylabel('Scores', fontsize=26)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=20)
    ax.tick_params(axis='y', labelsize=22)
    ax.tick_params(axis='x', length=0, pad=10)
    ax.set_ylim(0.82, 1.00)
    
    # Set thicker axes
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_linewidth(3.0)

    # Global legend
    ax.legend(
        loc='upper center', 
        bbox_to_anchor=(0.5, 1.15), 
        ncol=4, 
        fontsize=18, 
        frameon=False
    )

    fig.tight_layout()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.savefig(save_path, dpi=320, bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False

    base_dir = os.path.dirname(__file__)
    out_path = os.path.join(base_dir, 'figures', 'metrics_comparison_bar.png')
    
    plot_metrics_comparison(out_path)
    print(f"Figure saved to: {out_path}")
