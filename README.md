# RASPA2 FastAPI Client

This Python client provides an easy interface for interacting with the **RASPA2 FastAPI** service. It allows users to:

1. **Upload simulation input files and start a job**.
2. **Check the status of a running simulation**.
3. **Download the results once the simulation completes**.
4. **Run and wait for a simulation to finish automatically**.

## Installation

Ensure you have `requests` installed:
```sh
pip install requests
```

## Usage

### 1. Import and Initialize the Client
```python
from raspa_client import RaspaClient

client = RaspaClient(base_url="http://127.0.0.1:8000")
```

### 2. Start a Simulation
```python
task_id = client.run_simulation(
    "force_field_mixing_rules.def",
    "pseudo_atoms.def",
    "example_mof.cif",
    "adsorbate.def",
    "simulation.input",
    nproc=4
)
```

### 3. Check Simulation Status
```python
client.get_status(task_id)
```

### 4. Download Results
```python
client.download_results(task_id, "output.zip")
```

### 5. Run and Wait for Completion
```python
client.run_and_wait(
    "force_field_mixing_rules.def",
    "pseudo_atoms.def",
    "example_mof.cif",
    "adsorbate.def",
    "simulation.input",
    nproc=4
)
```

## License
This client follows the same licensing terms as the **RASPA2 FastAPI service**.

****