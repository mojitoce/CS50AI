from questions import load_files, tokenize, compute_idfs, top_files



dir = 'corpus'


files = load_files(dir)

file_words = {
    filename: tokenize(files[filename])
    for filename in files
}

file_idfs = compute_idfs(file_words)

# Prompt user for query
# query = set(tokenize(input("Query: ")))
query = set(tokenize("What are the types of supervised learning?"))
print(query)

filenames = top_files(query, file_words, file_idfs, n=1)

print(filenames)
