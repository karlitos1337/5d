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
                try:
                    with open(filepath, encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=filepath)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.ImportFrom):
                            if node.module == "auth.github_oauth" and "GitHubAuth" in [n.name for n in node.names]:
                                print(f"✅ Found GitHubAuth usage in: {filepath}")
                                usage_found = True
                except Exception as e:
                    print(f"⚠️  Could not parse {filepath}: {e}")

    if not usage_found:
        print("❌ No usage of GitHubAuth found in the codebase (excluding 99_unsortiert).")
    else:
        print("\n✅ Verification Complete: GitHubAuth is integrated.")

if __name__ == "__main__":
    check_github_auth_usage(".")
