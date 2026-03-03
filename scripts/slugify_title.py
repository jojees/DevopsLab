import re
from datetime import datetime

FILLER_WORDS = {
    'how', 'to', 'this', 'is', 'a', 'an', 'the', 'and', 'of', 'for', 'with',
    'by', 'from', 'on', 'in', 'that', 'when', 'you', 'run', 'your', 'guide',
    'using', 'use', 'into', 'step', 'steps', 'tutorial'
}

def slugify_title(title, max_words=5):
    title = title.lower()
    title = re.sub(r'[^a-z0-9]+', ' ', title)
    words = title.split()
    filtered = [word for word in words if word not in FILLER_WORDS]
    limited = filtered[:max_words]
    return '_'.join(limited)

def build_filename(project, title):
    today = datetime.today().strftime('%Y%m%d')  # Get current date
    slug = slugify_title(title)
    project_clean = project.lower().replace(' ', '')
    return f"{today}_{project_clean}_{slug}"

if __name__ == "__main__":
    project = input("Project or Series Name (e.g., interviewprep):\n> ").strip()
    title = input("Enter YouTube video title:\n> ")

    filename = build_filename(project, title)
    print(f"\nGenerated Filename:\n{filename}")
