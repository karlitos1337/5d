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
                        if isinstance(node, ast.Attribute):
                            if node.attr == "Github":
                                print(f"Found Github usage in {filepath}")
                                usage_found = True
                        elif isinstance(node, ast.ImportFrom):
                            if node.module == "github":
                                print(f"Found github import in {filepath}")
                                usage_found = True
                except Exception as e:
                    print(f"Error parsing {filepath}: {e}")

    return usage_found

if __name__ == "__main__":
    if check_github_auth_usage("."):
        print("⚠️  Potential direct GitHub API usage found. Verify it uses auth/github_oauth.py")
    else:
        print("✅ No direct GitHub API usage found (naive check).")
