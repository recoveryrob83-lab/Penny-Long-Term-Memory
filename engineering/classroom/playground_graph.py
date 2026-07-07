graph = {
    "A": ["B"],
    "B": ["A"],
}

for file_name, references in graph.items():
    print(file_name)
    
    for reference in references:
        print("  ->", reference)