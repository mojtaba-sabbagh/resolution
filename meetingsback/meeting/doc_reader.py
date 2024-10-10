from docx import Document
from pathlib import Path
import os


class WordReader:
    def __init__(self, file_name):
        self.doc = None
        self.read_file(file_name)

    def read_file(self, file_name):
        base_dir = Path(__file__).resolve().parent
        path = os.path.join(base_dir, 'assets', 'test_word', file_name)
        self.doc = Document(path)

    def get_paragraphs(self):
        paragraphs = [para.text for para in self.doc.paragraphs if para.text.strip()]
        return paragraphs


def test():
    file_name = "test.docx"
    reader = WordReader(file_name)
    paragraphs = reader.get_paragraphs()

    for i, para in enumerate(paragraphs, 1):
        print(f"{i}: {para}")


if __name__ == '__main__':
    test()
