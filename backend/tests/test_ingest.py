from app.ingest import chunk_text
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / 'data' / 'manuals'
sample = DATA_DIR / 'sample_manual.txt'

def main():
    text = sample.read_text(encoding='utf-8')
    chunks = chunk_text(text, chunk_size=50, overlap=10)
    print('Original length:', len(text))
    print('Chunks count:', len(chunks))
    print('First chunk preview:\n', chunks[0][:200])

if __name__ == '__main__':
    main()
