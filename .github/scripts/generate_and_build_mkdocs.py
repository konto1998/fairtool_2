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

    print(str(build_dir))
    sys.exit(0)
