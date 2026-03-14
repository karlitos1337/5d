import ast
import os


def check_github_auth_usage(directory):
    usage_found = False
    for root, _dirs, files in os.walk(directory):
        if "99_unsortiert" in root:  # Skip the unsorted/backup directory
        if "99_unsortiert" in root: # Skip the unsorted/backup directory
            continue
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                if filepath.endswith("auth/github_oauth.py") or filepath.endswith(
                    "tests/test_github_oauth_security.py"
                ):
                    continue

                try:
                    with open(filepath, encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=filepath)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Attribute) and node.attr == "auth":
                            # Check if it's related to Github
                            # This is a heuristic, might need refinement
                            usage_found = True
                            print(f"Potential Github Auth usage found in: {filepath}")
                        elif isinstance(node, ast.Attribute) and node.attr == "GitHubAuth":
                            print(f"Found usage in {filepath} line {node.lineno}")
                            usage_found = True
                except Exception as e:
                    print(f"Could not parse {filepath}: {e}")
    return usage_found





if __name__ == "__main__":
    if check_github_auth_usage("."):
        print("Github Auth usage detected.")
    else:
        print("No obvious Github Auth usage found.")
