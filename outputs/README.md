# Output files

The checked-in CSV and SVG files are **provisional logic-check outputs** generated using a temporary test-only Mesa API compatibility shim. They are not verified Mesa 3.5.2 outputs. The raw CSVs include a `validation_status` field to make this status explicit.

After installing the dependencies from the repository root, run:

```bash
python src/project_model/run_experiments.py
```

This overwrites the provisional output files and generates the detailed exposure traces, per-video recommendation traces, summary CSV, and PNG/SVG graphs from the installed Mesa-based project model. Inspect the regenerated results before writing the DEL02.1 comparison or creating a submission release.
