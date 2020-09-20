def progress(current: int, total: int) -> str:
    i = current * 100 / total
    p_bar = "["
    p_bar += str(round(i, 2))
    p_bar += "%]"
    return p_bar
