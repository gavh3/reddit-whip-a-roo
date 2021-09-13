import matplotlib.pyplot as plt

def plot_barh(y=None, width=None, x_lab=None, y_lab=None, title=None, plot_width=3, plot_height=1):
    fig, ax = plt.subplots(figsize=(plot_width, plot_height))
    ax.barh(y, width)
    ax.set_title(title)
    ax.set_xlabel(x_lab)
    ax.set_ylabel(y_lab)
    ax.tick_params(axis="both", labelsize=4)

    return fig