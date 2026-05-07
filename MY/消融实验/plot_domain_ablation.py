import os
from matplotlib import pyplot as plt
from matplotlib.patches import Patch

if __name__ == '__main__':
    # 1) 图片中的原始数据
    methods = [
        'single_time', 'single_freq', 'single_sax',
        'time+freq', 'time+sax', 'freq+sax',
        'fusion'
    ]

    metrics = ['Test Accuracy', 'Test Balanced Accuracy', 'Test MCC', 'Test Macro-F1']

    # 每个指标对应 7 个配置（单域3个、双域3个、三域1个）
    # acc = [0.9790, 0.9595, 0.9756, 0.9813, 0.9821, 0.9728, 0.9853]
    # bal_acc = [0.9684, 0.9391, 0.9634, 0.9719, 0.9732, 0.9591, 0.9778]
    # mcc = [0.9762, 0.9531, 0.9718, 0.9783, 0.9793, 0.9685, 0.9829]
    # f1 = [0.9677, 0.9389, 0.9646, 0.9715, 0.9738, 0.9595, 0.9775]
    # data_all = [acc, bal_acc, mcc, f1]
    acc = [0.9716, 0.9786, 0.9643, 0.9643, 0.9429, 0.9786, 0.9929]
    bal_acc = [0.9590, 0.9812, 0.9596, 0.9701, 0.9318, 0.9812, 0.9923]
    mcc = [0.9684, 0.9764, 0.9604, 0.9609, 0.9366, 0.9764, 0.9921]
    f1 = [0.9621, 0.9820, 0.9644, 0.9643, 0.9379, 0.9820, 0.9933]
    data_all = [acc, bal_acc, mcc, f1]
    # 2) 每个柱子独立颜色（与你给的参考图风格一致）
    bar_colors = [
        '#D0D0D0',  # single_time
        '#E4DF9D',  # single_freq
        '#EAD3D3',  # single_sax
        '#C8B1C9',  # time+freq
        '#D0A47B',  # time+sax
        '#BBD1BC',  # freq+sax
        '#3F78B4',  # fusion
    ]

    # 3) 全局绘图样式
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.linewidth'] = 2.5

    # 4) 画布布局：4 个指标子图 + 1 个图例子图（右侧）
    fig = plt.figure(figsize=(22, 6))
    axes = [fig.add_subplot(1, 5, i + 1) for i in range(4)]
    ax_legend = fig.add_subplot(1, 5, 5)

    for i, ax in enumerate(axes):
        values = data_all[i]
        ax.bar(
            range(len(methods)),
            values,
            color=bar_colors,
            edgecolor='white',
            linewidth=0.6,
            width=0.82,
        )

        # 参考图风格：不显示 x 轴标签，用右侧图例解释每个柱子
        ax.set_xticks([])
        ax.set_ylabel(metrics[i], fontsize=28)

        ymin = max(0.0, min(values) - 0.03)
        ymax = min(1.0, max(values) + 0.01)
        ax.set_ylim([ymin, ymax])
        ax.tick_params(axis='y', labelsize=22, width=1.5)

    legend_elements = [
        Patch(facecolor=bar_colors[idx], edgecolor='white', label=methods[idx])
        for idx in range(len(methods))
    ]
    ax_legend.legend(handles=legend_elements, loc='center', fontsize=22, frameon=True)
    ax_legend.set_axis_off()

    fig.tight_layout(pad=2.0)

    # 5) 保存
    os.makedirs('././figures/', exist_ok=True)
    save_path = './figures/domain_ablation_results.png'
    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"绘图完成！图片已保存至 {save_path}")
