# Output files

The files in this folder are provisional outputs generated while validating the model's logic using a temporary test-only Mesa API compatibility shim. They are included to show the expected file structure and output format, but they are **not yet verified Mesa 3.5.2 outputs**.

After installing the dependencies from the repository root, run:

```bash
python src/project_model/run_experiments.py
```

This overwrites the provisional CSV and PNG files with outputs from the actual Mesa-based project model. Use only those regenerated files in the final DEL02.1 comparison.
