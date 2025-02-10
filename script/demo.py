# Step by Step call API
from raspa_client import RaspaClient
client = RaspaClient()

# You need to focus here: double check the path of all def, cif, and input files
# Start simulation
task_id = client.run_simulation(
    "force_field_mixing_rules.def",
    "pseudo_atoms.def",
    "example_mof.cif",
    "adsorbate.def",
    "simulation.input",
    nproc=4
)

# Check status
client.get_status(task_id)

# Download results
client.download_results(task_id, "output.zip")

# Serial call API
# You need to focus here: double check the path of all def, cif, and input files
client = RaspaClient()
client.run_and_wait(
    "force_field_mixing_rules.def",
    "pseudo_atoms.def",
    "example_mof.cif",
    "adsorbate.def",
    "simulation.input",
    nproc=4
)
