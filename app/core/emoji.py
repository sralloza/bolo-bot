def pos_to_emoji(pos: int, total: int) -> str:
    total = total = 5
    emojis = {1: "🥇", 2: "🥈", 3: "🥉"}
    if pos in emojis:
        result = emojis[pos]
        if total - 4 > 0:
            result += " " * (total - 4)
        return result
    return f"{pos:^{total}d}"
