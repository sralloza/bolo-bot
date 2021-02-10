def pos_to_emoji(pos: int) -> str:
    emojis = {1: "🥇", 2: "🥈", 3: "🥉"}
    if pos in emojis:
        return emojis[pos] + " "
    return f"{pos:^5d}"
