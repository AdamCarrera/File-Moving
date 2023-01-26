import pandas as pd
from pathlib import Path
import os
import logging
import shutil
from enum import Enum, auto

EXCEL_EXTENSIONS = (".xlsx", ".xls", ".xlsm", ".xlsb")


class Transfer(Enum):
    COPY = auto()
    CUT = auto()


def move_files(file_name: str, transfer_type: Transfer = Transfer.COPY) -> None:
    """
    Transfers files to their respective destinations based on excel config file.


    The config file consists of 3 columns:
        name: name of file to be transferred
        from: parent directory of above file
        to:   destination file directory

    :param file_name: excel config file name
    :param transfer_type: choose between cut/paste or copy/paste, defualt functionality is to copy and paste files
    """

    # write steps taken to transfer.log
    logging.basicConfig(
        level=logging.INFO,
        filename="transfer.log",
        filemode="w",
        # format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
        # datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not isinstance(transfer_type, Transfer):
        raise TypeError("incorret type for transfer_type argument")

    # Open excel file with file name, location, and destination
    file_path = Path(file_name)
    file_extension = file_path.suffix.lower()

    # handle different input file types
    if file_extension in EXCEL_EXTENSIONS:
        df = pd.read_excel(file_name, engine="openpyxl")
    else:
        df = pd.read_csv(file_name)

    # for each row in the column, move the file from the source to the
    #   destination
    for _, row in df.iterrows():
        logging.info(f"Copying: {row['file name']}")
        logging.info(f"From:  {row['from']}")
        logging.info(f"To:  {row['to']} \n")

        source = os.path.join(row["from"], row["file name"])
        dest = os.path.join(row["to"], row["file name"])

        try:
            if transfer_type == Transfer.COPY:
                shutil.copy(source, dest)
            if transfer_type == Transfer.CUT:
                os.replace(source, dest)
        except FileNotFoundError as e:
            logging.error(f"{e}\n")
            continue

    logging.shutdown()


if __name__ == "__main__":

    move_files("test.xlsx", "asdf")
