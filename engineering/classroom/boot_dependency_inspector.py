from pathlib import Path


# A list of boot-related files we want to inspect.
# Each item is a path relative to the repository root.
BOOT_FILES: list[str] = [
    "memory/STARTUP_BOOT.md",
    "memory/00_START_HERE.md",
]


# A dependency graph is:
#   key   = a boot file path
#   value = a list of boot file paths referenced by that file
#
# Example:
# {
#     "memory/STARTUP_BOOT.md": ["memory/00_START_HERE.md"],
#     "memory/00_START_HERE.md": ["memory/STARTUP_BOOT.md"],
# }
DependencyGraph = dict[str, list[str]]


def get_repo_root() -> Path:
    # Anchor from this script's location:
    # engineering/classroom/boot_dependency_inspector.py
    #
    # parents[0] = engineering/classroom
    # parents[1] = engineering
    # parents[2] = repository root
    repo_root: Path = Path(__file__).resolve().parents[2]

    return repo_root


def read_boot_file(repo_root: Path, relative_path: str) -> str:
    # Convert a repo-relative path into a full filesystem path.
    file_path: Path = repo_root / relative_path

    # Read the file contents as text.
    file_text: str = file_path.read_text(encoding="utf-8")

    return file_text


def find_references(
    text: str,
    possible_targets: list[str],
    current_file: str,
) -> list[str]:
    # This list will hold every known boot file that appears inside the current file's text.
    references: list[str] = []

    for target in possible_targets:
        # Ignore references to the file itself.
        # We are looking for cross-file dependencies.
        if target == current_file:
            continue

        # If this target path appears anywhere in the file text,
        # treat it as a dependency.
        if target in text:
            references.append(target)

    return references


def build_dependency_graph(repo_root: Path) -> DependencyGraph:
    # Dictionary where:
    #   key   = boot file path
    #   value = list of boot files referenced by that file
    graph: DependencyGraph = {}

    for relative_path in BOOT_FILES:
        # Read the contents of this boot file.
        text: str = read_boot_file(repo_root, relative_path)

        # Find which known boot files are mentioned inside this file.
        references: list[str] = find_references(
            text,
            BOOT_FILES,
            relative_path,
        )

        # Store the relationship:
        #   this file -> files it references
        graph[relative_path] = references

    return graph


def find_cycle(graph: DependencyGraph) -> list[str] | None:
    # Files that have been completely checked.
    fully_checked: set[str] = set()

    # Files in the current traversal path.
    # If we encounter a file already in this path, we found a cycle.
    current_path: list[str] = []

    def walk(file_name: str) -> list[str] | None:
        # If this file is already in the current path,
        # then we looped back to something we are currently walking.
        if file_name in current_path:
            cycle_start_index: int = current_path.index(file_name)
            cycle: list[str] = current_path[cycle_start_index:] + [file_name]

            return cycle

        # If this file was already fully checked in a previous walk,
        # we do not need to check it again.
        if file_name in fully_checked:
            return None

        # Add this file to the current path before walking its references.
        current_path.append(file_name)

        # Follow every outgoing dependency from this file.
        for reference in graph[file_name]:
            cycle: list[str] | None = walk(reference)

            if cycle:
                return cycle

        # We are done exploring this file's dependencies.
        # Remove it from the current path.
        current_path.pop()

        # Mark it as fully checked.
        fully_checked.add(file_name)

        return None

    # Try starting a graph walk from every file.
    for file_name in graph:
        cycle: list[str] | None = walk(file_name)

        if cycle:
            return cycle

    return None


def print_dependency_graph(graph: DependencyGraph) -> None:
    print("Dependency Graph")
    print("----------------")
    print()

    for file_name, references in graph.items():
        print(file_name)

        if references:
            for reference in references:
                print(f"    -> {reference}")
        else:
            print("    -> None")

        print()


def print_cycle_report(cycle: list[str] | None) -> None:
    print("Cycle Check")
    print("-----------")
    print()

    if cycle:
        edge_count: int = len(cycle) - 1

        print("[CYCLE DETECTED]")
        print(f"Cycle length: {edge_count} edges")
        print()

        print(cycle[0])

        for file_name in cycle[1:]:
            print(f"  -> {file_name}")
    else:
        print("[OK] No cycles detected")


def main() -> None:
    repo_root: Path = get_repo_root()
    graph: DependencyGraph = build_dependency_graph(repo_root)

    print_dependency_graph(graph)

    cycle: list[str] | None = find_cycle(graph)
    print_cycle_report(cycle)


if __name__ == "__main__":
    main()
