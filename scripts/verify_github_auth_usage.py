import ast
import os


def check_github_auth_usage(directory):
    usage_found = False
    for root, _, files in os.walk(directory):
        if "99_unsortiert" in root: # Skip the unsorted/backup directory
            continue

        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=filepath)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.Attribute) and node.attr == "Github":
                             # Check if it's imported from github (PyGithub)
                            # This is a basic check; AST analysis for imports would be more robust
                            print(f"Potential PyGithub usage in: {filepath}:{node.lineno}")
                            usage_found = True
                        elif isinstance(node, ast.ImportFrom) and node.module == "github":
                             print(f"PyGithub import in: {filepath}:{node.lineno}")
                             usage_found = True

                except Exception as e:
                    print(f"Error parsing {filepath}: {e}")

    if not usage_found:
        print("✅ No direct PyGithub 'Github' class usage found (likely using custom auth wrapper).")
    else:
        print("⚠️  Potential direct PyGithub usage found. Verify if it uses the auth wrapper.")

if __name__ == "__main__":
    check_github_auth_usage(".")