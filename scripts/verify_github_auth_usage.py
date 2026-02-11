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
                        # Check for GitHubAuth instantiation or import
                        if isinstance(node, ast.Call):
                            if isinstance(node.func, ast.Name) and node.func.id == "GitHubAuth":
                                print(f"⚠️  Found direct GitHubAuth usage in: {filepath}:{node.lineno}")
                                usage_found = True
                            elif isinstance(node.func, ast.Attribute) and node.func.attr == "GitHubAuth":
                                print(f"⚠️  Found direct GitHubAuth usage in: {filepath}:{node.lineno}")
                                usage_found = True

                        # Check for imports
                        if isinstance(node, ast.ImportFrom):
                            if node.module and "auth.github_oauth" in node.module:
                                print(f"ℹ️  Found import of auth.github_oauth in: {filepath}:{node.lineno}")

                except Exception:
                    # Parse errors or encoding errors
                    pass

    if not usage_found:
        print("✅ No direct instantiation of GitHubAuth found (good).")
    else:
        print("⚠️  Review above usages. Ensure secrets are handled safely.")

if __name__ == "__main__":
    check_github_auth_usage(".")
