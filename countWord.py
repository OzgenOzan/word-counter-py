import textract, re
import os
import pandas as pd

d = {}

def getFileNames(path):
    result = set()
    i = 0
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            result.add(os.path.join(root, name))
    return result

def wordCount(fileName):
    textAsBytes = textract.process(fileName)

    text = textAsBytes.decode("utf-8")

    pattern = r"[^$α-ωΑ-Ωa-zA-Z0-9/`'’-]+"
    text = re.sub(pattern, ' ', text)
    text = text.lower()

    word_list = text.split()

    for word in word_list:
        d[word] = d.get(word,0) + 1

def main():
    files = getFileNames(r"C:\Users\oozgen\Desktop\Udemy\Sites\word-counter-py\Articles")
    for file in files:
        wordCount(file)

    df = pd.DataFrame(list(d.items()),columns = ['Word','Count'])
    df.to_excel("output.xlsx")

if __name__ == "__main__":
    main()


