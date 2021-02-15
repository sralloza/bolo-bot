def pos_to_emoji(pos: int, emoji_enabled=True) -> str:
    emojis = {1: "🥇", 2: "🥈", 3: "🥉"}
    if pos in emojis and emoji_enabled:
        return emojis[pos] + " "
    return f"{pos:^5d}"
