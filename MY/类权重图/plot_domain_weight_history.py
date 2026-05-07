import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'domain_weight_history_seed42.csv')
    
    # Load data
    df = pd.read_csv(csv_path)
    
    # Plot configuration
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Colors suitable for scientific papers
    colors = {
        'time': '#3498db',  # Blue
        'freq': "#8BCF8B",  # Red
        'sax':  "#A695BF"   # Green
    }
    
    ax.plot(df['epoch'], df['time'], label='Time Domain', linewidth=2.5, color=colors['time'])
    ax.plot(df['epoch'], df['freq'], label='Frequency Domain', linewidth=2.5, color=colors['freq'])
    ax.plot(df['epoch'], df['sax'], label='SAX Domain', linewidth=2.5, color=colors['sax'])
    
    # Formatting
    ax.set_xlabel('Epoch', fontsize=14, fontweight='bold')
    ax.set_ylabel('Domain Weight', fontsize=14, fontweight='bold')
    ax.set_title('Domain Weight Evolution during Training', fontsize=16, fontweight='bold')
    
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(fontsize=12, loc='best', framealpha=0.9)
    
    # Axis limits
    ax.set_xlim(df['epoch'].min(), df['epoch'].max())
    
    # Save figure
    out_dir = os.path.join(script_dir, 'figures')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    out_path = os.path.join(out_dir, 'domain_weight_history.png')
    out_path_pdf = os.path.join(out_dir, 'domain_weight_history.pdf')
    
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.savefig(out_path_pdf, bbox_inches='tight')
    print(f"Visualization saved to:\n  - {out_path}\n  - {out_path_pdf}")

if __name__ == '__main__':
    main()
