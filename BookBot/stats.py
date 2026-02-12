def count_words(path_to_file):
  with open(path_to_file) as f:
    file_contents = f.read()
  words = file_contents.split()
  count =  0
  for word in words:
    count += 1
  print(f"Found {count} total words")


def char_count(path_to_file):
  with open(path_to_file) as f:
    file_contents = f.read()
  char_dict = {}
  for letter in file_contents.lower():
    if letter not in char_dict:
      char_dict[letter] = 1
    else:
      char_dict[letter] += 1
  print(char_dict)




def book_report(path_to_file):
  with open(path_to_file) as f:
    file_contents = f.read()
  char_dict = {}
  for letter in file_contents.lower():
    if letter not in char_dict:
      char_dict[letter] = 1
    else:
      char_dict[letter] += 1
  new_dict = []
  for k,v in char_dict.items():
    if k.isalpha():
      new_dict.append({"char": k, "num": v})
  def sort_on(items):
    return items["num"]
  
  new_dict.sort(reverse=True, key=sort_on)
  print("============ BOOKBOT ============")
  print("Analyzing book found at books/frankenstein.txt...")
  print("---------- Word Count ----------")
  count_words("books/frankenstein.txt")
  print("-------- Character Count -------")
  for item in new_dict:
    print(item["char"] + ': ' + str(item["num"]))
  print("============= END ===============")



