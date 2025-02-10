import requests
import time
import os

class RaspaClient:
    """
    A client for interacting with the RASPA2 + FastAPI service.
    
    Provides methods to:
    1. Upload simulation files and start a job.
    2. Check job status.
    3. Download the results after the simulation completes.
    """

    def __init__(self, base_url="YOU SERVER URL"):
        """
        Initialize the client with the base URL of the API.
        
        Args:
            base_url (str): The base URL of the FastAPI service.
        """
        self.base_url = base_url

    def run_simulation(self, force_field_mixing_rules, pseudo_atoms, mof_cif, adsorbate_def, simulation_input, nproc=2):
        """
        Upload input files and start a RASPA2 simulation.

        Args:
            force_field_mixing_rules (str): Path to `force_field_mixing_rules.def`.
            pseudo_atoms (str): Path to `pseudo_atoms.def`.
            mof_cif (str): Path to MOF `.cif` file.
            adsorbate_def (str): Path to adsorbate `.def` file.
            simulation_input (str): Path to `simulation.input`.
            nproc (int, optional): Number of MPI processes (default is 2).

        Returns:
            str: The task ID assigned to this simulation.
        """
        url = f"{self.base_url}/run_simulation"
        files = {
            "force_field_mixing_rules": open(force_field_mixing_rules, "rb"),
            "pseudo_atoms": open(pseudo_atoms, "rb"),
            "mof_cif": open(mof_cif, "rb"),
            "adsorbate_def": open(adsorbate_def, "rb"),
            "simulation_input": open(simulation_input, "rb"),
        }
        data = {"nproc": nproc}

        response = requests.post(url, files=files, data=data)
        for file in files.values():
            file.close()  # Close files after upload

        if response.status_code == 202:
            task_id = response.json().get("task_id")
            print(f"Simulation started. Task ID: {task_id}")
            return task_id
        else:
            print(f"Error: {response.json()}")
            return None

    def get_status(self, task_id):
        """
        Check the status of a RASPA2 simulation.

        Args:
            task_id (str): The ID of the simulation task.

        Returns:
            dict: A dictionary containing the task status and log output.
        """
        url = f"{self.base_url}/task_status/{task_id}"
        response = requests.get(url)

        if response.status_code == 200:
            status_data = response.json()
            print(f"Task Status: {status_data['status']}")
            print("Recent Logs:")
            for log in status_data.get("log", []):
                print(log.strip())
            return status_data
        else:
            print(f"Error: {response.json()}")
            return None

    def download_results(self, task_id, output_path="results.zip"):
        """
        Download the simulation results if the task is completed.

        Args:
            task_id (str): The ID of the completed simulation task.
            output_path (str, optional): Path to save the results ZIP file.

        Returns:
            bool: True if download was successful, False otherwise.
        """
        url = f"{self.base_url}/download_results/{task_id}"
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Results downloaded: {output_path}")
            return True
        else:
            print(f"Error: {response.json()}")
            return False

    def run_and_wait(self, force_field_mixing_rules, pseudo_atoms, mof_cif, adsorbate_def, simulation_input, nproc=2, poll_interval=10):
        """
        Run a simulation and wait for it to complete, then download results.

        Args:
            force_field_mixing_rules (str): Path to `force_field_mixing_rules.def`.
            pseudo_atoms (str): Path to `pseudo_atoms.def`.
            mof_cif (str): Path to MOF `.cif` file.
            adsorbate_def (str): Path to adsorbate `.def` file.
            simulation_input (str): Path to `simulation.input`.
            nproc (int, optional): Number of MPI processes (default is 2).
            poll_interval (int, optional): Time interval (seconds) to check task status.

        Returns:
            str: Path to downloaded results ZIP file if successful, else None.
        """
        task_id = self.run_simulation(force_field_mixing_rules, pseudo_atoms, mof_cif, adsorbate_def, simulation_input, nproc)
        if not task_id:
            return None

        while True:
            status_data = self.get_status(task_id)
            if not status_data:
                return None

            status = status_data["status"]
            if status == "completed":
                return self.download_results(task_id)
            elif status == "failed":
                print("Simulation failed.")
                return None

            print(f"Waiting {poll_interval} seconds before checking again...")
            time.sleep(poll_interval)
