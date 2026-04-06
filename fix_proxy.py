import os

files_to_fix = [
    "web/5d-map/owid_proxy.py",
    "docs/5d-map/owid_proxy.py"
]

for filepath in files_to_fix:
    with open(filepath, "r") as f:
        content = f.read()

    # 1. Remove duplicate MAX_RESPONSE_SIZE = 10 * 1024 * 1024  # 10MB
    content = content.replace("                MAX_RESPONSE_SIZE = 10 * 1024 * 1024  # 10MB\n", "")

    # 2. Fix the try/except block around Content-Length
    old_block = """                    if content_len:
                        try:
                            if int(content_len) > MAX_RESPONSE_SIZE:
                                raise ValueError("Response too large")
                        except (TypeError, ValueError):
                            # Invalid Content-Length from upstream; log and fall back to streamed size check
                            sys.stderr.write(
                                f"Invalid Content-Length header from upstream for {key}: {content_len}\\n"
                            )"""

    new_block = """                    if content_len:
                        try:
                            content_size = int(content_len)
                        except (TypeError, ValueError):
                            # Invalid Content-Length from upstream; log and fall back to streamed size check
                            sys.stderr.write(
                                f"Invalid Content-Length header from upstream for {key}: {content_len}\\n"
                            )
                            content_size = -1
                        if content_size > MAX_RESPONSE_SIZE:
                            raise ValueError("Response too large")"""

    content = content.replace(old_block, new_block)

    with open(filepath, "w") as f:
        f.write(content)
