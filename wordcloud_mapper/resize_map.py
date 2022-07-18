def resize_map(fig, scale):
    """
    Resize the matplotlib figure by a given scaling factor.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        A matplotlib Figure object.
    scale : float
        The rescaling factor as a multiplier of the figure's current size.
        If ``scale > 1.0``, image gets bigger by a factor of scale (e.g. 1.5 means 50% bigger).
        If ``scale < 1.0``, image gets smaller by a factor of scale (e.g. 0.5 means 50% smaller).
        If ``scale = 1.0``, no change is made.

    """
    # get current size and multiply that by the given scale
    width, height = fig.get_size_inches()*scale
    fig.set_size_inches(width, height)
    dpi = fig.dpi
    print(f"Figure resized to width {int(width*dpi)}px and height {int(height*dpi)}px.")
