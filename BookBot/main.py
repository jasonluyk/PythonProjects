import sys
from stats import count_words, char_count, book_report


def get_book_text(path_to_file):
  with open(path_to_file) as f:
    file_contents = f.read()
  


def main():
  if len(sys.argv) != 2:
    print("Usage: python3 main.py <path_to_book>")
    sys.exit(1)
  else:  
    book_report(sys.argv[1])

main()
