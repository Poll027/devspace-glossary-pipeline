"""Validate an artifact against a pack schema, resolving cross-file $refs.

Usage as a CLI (any agent can run it): python3 schema_check.py <schema file name> <artifact.json>
"""
import json
import sys
from pathlib import Path

SCHEMAS = Path(__file__).resolve().parent.parent / "schemas"


def validate(obj, schema_name):
    import jsonschema
    from referencing import Registry, Resource
    reg = Registry().with_resources(
        (f.name, Resource.from_contents(json.loads(f.read_text()))) for f in SCHEMAS.glob("*.schema.json"))
    schema = json.loads((SCHEMAS / schema_name).read_text())
    jsonschema.Draft202012Validator(schema, registry=reg).validate(obj)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    validate(json.loads(Path(sys.argv[2]).read_text()), sys.argv[1])
    print(f"VALID: {sys.argv[2]} against {sys.argv[1]}")
