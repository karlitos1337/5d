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
                        if isinstance(node, ast.Attribute) and node.attr == "GitHubAuth":
                             print(f"⚠️  Found direct usage of GitHubAuth in {filepath}:{node.lineno}")
                             usage_found = True
                        elif isinstance(node, ast.ImportFrom) and node.module == "auth.github_oauth":
                             print(f"⚠️  Found import from auth.github_oauth in {filepath}:{node.lineno}")
                             usage_found = True

                except Exception as e:
                    print(f"Error analyzing {filepath}: {e}")

    if not usage_found:
        print("✅ No direct usage of GitHubAuth found. All auth seems to go through caching layer.")
    else:
        print("❌ Found direct usages of GitHubAuth. Please verify they are necessary.")

if __name__ == "__main__":
    check_github_auth_usage(".")
