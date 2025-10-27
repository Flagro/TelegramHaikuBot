def format_haiku(lines: list[str]) -> str:
    """
    Format haiku lines in italic (cursive) for Telegram.
    
    Args:
        lines: List of three haiku lines
        
    Returns:
        Formatted haiku string with each line in italic
    """
    return "\n".join(f"_{line}_" for line in lines)

