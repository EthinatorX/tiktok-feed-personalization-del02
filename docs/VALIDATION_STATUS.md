# Validation status — read before creating the submission release

The code was syntax-checked and the project tests passed in the authoring environment. Both experiment conditions and the example script were exercised with a **temporary test-only Mesa API compatibility shim** because Mesa 3.5.2 could not be installed in that environment (the package index was unreachable). The shim is not included in this repository.

The model uses the Mesa APIs shown in the official Mesa stable tutorial (`mesa.Model`, `mesa.Agent`, `Agent.create_agents`, `AgentSet.shuffle_do`, and `Model.run_for`). However, **the current CSV and PNG files have not yet been regenerated under an installed Mesa 3.5.2 environment**. Treat the included outputs as provisional logic-check outputs, not as verified Mesa execution evidence.

Before submitting DEL02.2:

1. Create a Python 3.12+ virtual environment.
2. Install `requirements.txt`.
3. Run the preserved source example with `python src/boltzmann_wealth_model/run_model.py`.
4. Run `python -m unittest discover -s tests -v`.
5. Run `python src/project_model/run_experiments.py` to regenerate every output using Mesa itself.
6. Inspect the regenerated CSV/PNG files and update the DEL02.1 report so its comparison describes those actual outputs.
7. Only then commit, tag `DEL02`, and create the `DEL02 Release` GitHub release.

Do not describe the existing provisional outputs as having been produced by Mesa until step 5 has been completed successfully.
