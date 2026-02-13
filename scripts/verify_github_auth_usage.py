import ast
import os

def check_github_auth_usage(directory):
    usage_found = False
    for root, _dirs, files in os.walk(directory):
        if "99_unsortiert" in root: # Skip the unsorted/backup directory
            continue
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                if filepath.endswith("auth/github_oauth.py") or filepath.endswith("tests/test_github_oauth_security.py"):
                    continue

                try:
                    with open(filepath, encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=filepath)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.Name) and node.id == "GitHubAuth":
                            print(f"Found usage in {filepath} line {node.lineno}")
                            usage_found = True
                        elif isinstance(node, ast.Attribute) and node.attr == "GitHubAuth":
                             print(f"Found usage in {filepath} line {node.lineno}")
                             usage_found = True
                except Exception as e:
                    print(f"Could not parse {filepath}: {e}")

    if not usage_found:
        print("No usage of GitHubAuth found in the codebase (excluding definition and test).")
    else:
        print("WARNING: GitHubAuth usage detected!")

if __name__ == "__main__":
    check_github_auth_usage(".")
