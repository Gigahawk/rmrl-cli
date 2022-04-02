import os
from glob import glob
import json
from rmrl import render

INPUT = "/mnt/d/remarkable_sync"
OUTPUT = "./out"

paths = glob(os.path.join(INPUT, "*.metadata"))
paths = [os.path.splitext(p)[0] for p in paths]

for p in paths:
    print(f"Reading {p}")
    guid = os.path.basename(p)
    meta_path = f"{p}.metadata"
    with open(meta_path) as f:
        metadata = json.load(f)
    name = metadata.get("visibleName")
    f_type = metadata.get("type")

    if not name:
        name = guid
        print(f"Warning, name not found for {name}")

    if f_type == "CollectionType":
        print(f"{name} appears to be a folder, skipping")
        continue
    print(f"Converting {name}")
    try:
        stream = render(
            p,
            template_alpha=0.3,
            expand_pages=True,
            only_annotated=False)
    except Exception as e:
        print(f"error converting {name}")
        print(e)
        print(e.args)
        import pdb;pdb.set_trace()
        continue
    with open(os.path.join(OUTPUT, f"{name}.pdf"), "wb") as f:
        f.write(stream.read())

import pdb;pdb.set_trace()
