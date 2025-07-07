import re
from pathlib import Path

INPUT_DIR = Path('books_txt_output')
OUTPUT_DIR = Path('books_txt_clean')

URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')
EMAIL_PATTERN = re.compile(r'\S+@\S+')
FOOTNOTE_PATTERN = re.compile(r'\[\s*[\*\-\u2190]?\d+\s*\]')
PAGE_NUM_LINE_PATTERN = re.compile(r'^\s*[-\u2013\u2014]*\s*\d{1,4}\s*[-\u2013\u2014]*\s*$')
PAGE_NUM_START_PATTERN = re.compile(r'^\s*\d{1,4}\s+')
PAGE_NUM_END_PATTERN = re.compile(r'\s+\d{1,4}\s*$')

def preprocess_line(line: str) -> str:
    line = line.strip('\ufeff').strip()  # remove BOM and surrounding spaces
    line = URL_PATTERN.sub('', line)
    line = EMAIL_PATTERN.sub('', line)
    line = FOOTNOTE_PATTERN.sub('', line)
    if PAGE_NUM_LINE_PATTERN.fullmatch(line):
        return ''
    line = PAGE_NUM_START_PATTERN.sub('', line)
    line = PAGE_NUM_END_PATTERN.sub('', line)
    line = re.sub(r'\s+', ' ', line)  # collapse whitespace
    return line.strip()

def should_skip(line: str) -> bool:
    if not line:
        return True
    # skip lines that contain only digits or punctuation
    if re.fullmatch(r'[\d\W]+', line):
        return True
    return False

def preprocess_file(in_path: Path, out_path: Path):
    with in_path.open('r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        line = preprocess_line(line)
        if should_skip(line):
            continue
        cleaned.append(line)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open('w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned))


def preprocess_directory(input_dir: Path = INPUT_DIR, output_dir: Path = OUTPUT_DIR):
    for path in input_dir.glob('*.txt'):
        out_file = output_dir / path.name
        preprocess_file(path, out_file)

if __name__ == '__main__':
    preprocess_directory()
