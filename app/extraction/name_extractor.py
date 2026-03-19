def extract_name(text: str) -> str:
    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if line:
            return line.title()  

    return "Unknown"