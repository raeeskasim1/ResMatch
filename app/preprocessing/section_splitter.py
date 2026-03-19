def split_sections(text: str) -> dict:
    sections = {
        "summary": "",
        "skills": "",
        "experience": "",
        "education": "",
        "projects": "",
        "certifications": "",
        "full_text": text
    }

    lines = text.splitlines()
    current = "summary"

    headers = {
        "skills": [
            "skills",
            "technical skills",
            "technical expertise",
            "technical competencies"
        ],
        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment history"
        ],
        "education": [
            "education",
            "academic background",
            "academic qualification",
            "qualifications"
        ],
        "projects": [
            "projects",
            "relevant projects",
            "academic projects"
        ],
        "certifications": [
            "certifications",
            "certificates",
            "licenses & certifications"
        ]
    }

    for line in lines:
        line_clean = line.strip().lower()

        if not line_clean:
            continue

        switched = False
        for key, values in headers.items():
            if line_clean in values:
                current = key
                switched = True
                break

        if not switched:
            sections[current] += line + "\n"

    return sections