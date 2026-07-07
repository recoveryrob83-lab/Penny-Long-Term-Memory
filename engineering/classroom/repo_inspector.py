from pathlib import Path

# Core Life OS directories that must exist for the repo to be considered structurally healthy.
# These encode our current structural expectations for a healthy repo
EXPECTED_CORE_DIRECTORIES = [
    "archive",
    "coordination",
    "memory",
    "projects",
]

def find_unexpected_directories(directories):
    expected_names = set(EXPECTED_CORE_DIRECTORIES)
    actual_names = set(directory.name for directory in directories)

    unexpected_names = actual_names - expected_names

    return sorted(unexpected_names)

def check_expected_directories(repo_root):
    results = []

    for directory_name in EXPECTED_CORE_DIRECTORIES:
        directory_path = repo_root / directory_name

        if directory_path.exists() and directory_path.is_dir():
            results.append((directory_name, True))
        else:
            results.append((directory_name, False))

    return results

def check_expected_directories(repo_root):
    results = []

    for directory_name in EXPECTED_CORE_DIRECTORIES:
        directory_path = repo_root / directory_name

        if directory_path.exists() and directory_path.is_dir():
            results.append((directory_name, True))
        else:
            results.append((directory_name, False))

    return results

def get_top_level_items(repo_root):
    # Ignore .git because it is repository metadata, not Life OS content.
    # Sorting makes the report deterministic: same repo state, same output order.
    return sorted(
        [item for item in repo_root.iterdir() if item.name != ".git"],
        key=lambda item: item.name.lower()
    )

def classify_items(items):
    # Split filesystem entries into directories and files so reporting can present them separately.
    directories = []
    files = []

    for item in items:
        if item.is_dir():
            directories.append(item)
        else:
            files.append(item)

    return directories, files

def print_report(repo_root, directories, files, expected_directory_results, unexpected_directories):
    total_items = len(directories) + len(files)

    print("Repository Inspector v0.4")
    print("-------------------------")
    print(f"Repository root: {repo_root}")
    print()

    print("Top-level directories:")
    print()

    for directory in directories:
        print(f"[DIR]  {directory.name}")

    print()
    print("Top-level files:")
    print()

    for file in files:
        print(f"[FILE] {file.name}")

    print()
    print("Expected core directories:")
    print()

    for directory_name, exists in expected_directory_results:
        if exists:
            print(f"[OK]      {directory_name}")
        else:
            print(f"[MISSING] {directory_name}")

    print()
    print("Summary:")
    print()

    print(f"Total directories: {len(directories)}")
    print(f"Total files: {len(files)}")
    print(f"Total top-level items: {total_items}")
    print()
    # Snarky classroom signal: unexpected directories exist. Replace with formal wording for CI/use by others.
    print("OMG, MORE")
    print("OMG, MORE")
    print()

    if unexpected_directories:
        for directory_name in unexpected_directories:
            print(f"[EXTRA]   {directory_name}")
    else:
        print("[OK]      None")

def main():
    print("Hello")
    print()
    repo_root = Path(__file__).resolve().parents[2]

    items = get_top_level_items(repo_root)
    directories, files = classify_items(items)

    expected_directory_results = check_expected_directories(repo_root)
    unexpected_directories = find_unexpected_directories(directories)

    print_report(
        repo_root,
        directories,
        files,
        expected_directory_results,
        unexpected_directories
    )
if __name__ == "__main__":
    main()