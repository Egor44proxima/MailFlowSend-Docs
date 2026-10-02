# MailFlowSend Documentation

Public technical and operator documentation for **MailFlowSend**.

Current accepted application baseline:

```text
Core       0.16.9
Schema     v53
ABI        1
Migration  NONE
```

This repository contains the source for the MailFlowSend GitHub Pages site, built with **MkDocs Material**.

## Local preview

```bash
python -m pip install -r requirements.txt
mkdocs serve
```

## Production build

```bash
mkdocs build --strict
```

## Public documentation boundary

This repository intentionally excludes credentials, private recipient evidence, raw Message-ID values, production databases, diagnostic bundles, local secrets, and other sensitive runtime artifacts.
