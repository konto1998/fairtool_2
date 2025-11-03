from pathlib import Path
from fairtool.visualize import serve_docs
import sys

if __name__ == '__main__':
    docs_src = Path('tests/VASP')
    # Build into a repository-root 'site' folder so CI can deploy it directly
    build_dir = Path('site')
    # Ensure output dir exists
    build_dir.mkdir(parents=True, exist_ok=True)

    # Run serve_docs which will copy packaged assets and run mkdocs build to `build_dir`
    serve_docs(docs_src, port=8000, dry_run=False, build=True, build_dir=build_dir)

    # Diagnostic: list resulting files so CI logs show what was generated.
    print(f"Built site directory: {build_dir}")
    entries = list(build_dir.rglob("**/*"))
    if not entries:
        print("ERROR: build directory appears empty. Contents:" )
        for p in build_dir.iterdir():
            print(p)
        # Fail so CI will surface this in logs and not silently publish an empty site
        sys.exit(2)

    print("Site contents (first 200 entries):")
    for i, p in enumerate(sorted([str(p.relative_to(build_dir)) for p in entries])):
        if i >= 200:
            break
        print(p)

    print(str(build_dir))
    sys.exit(0)
