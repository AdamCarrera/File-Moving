from pathlib import Path
from tempfile import TemporaryDirectory
from movefiles import move_files
import pandas as pd
import pytest
import os


def test_config() -> None:
    # read the config file in the project directory to make sure that it's ready
    # this tests the config file as well as the setup function
    pass


def test_transfer() -> None:
    # create temporary source and destination folders in project directory and test that the program can transfer them properly
    with TemporaryDirectory() as source_folder, TemporaryDirectory() as dest_folder:
        source_path = Path(source_folder)
        dest_path = Path(dest_folder)

        records = {"file name": [], "from": [], "to": []}
        for i in range(5):
            current_file = source_path / f"file_{i}.txt"
            current_file.write_text(f"Hello I am file {i}")
            records["file name"].append(current_file.name)
            records["from"].append(source_folder)
            records["to"].append(dest_folder)

            config_file = source_path / "config.csv"
            pd.DataFrame(records).to_csv(config_file)

            # assert that the example files were created properly
            assert os.path.exists(current_file)

        # transfer files from source to destination
        move_files(config_file)

        # assert that files were transferred properly
        for i in range(5):
            assert os.path.exists(dest_path / f"file_{i}.txt")

        # maybe have one file that in config.csv that doesn't exist in source? allows us to test exception handling behavior


def test_transfer_missing_file() -> None:
    # test that the program does not crash upon transfer of a non-existent file
    pass
