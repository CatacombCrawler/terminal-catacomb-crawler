import json
from datetime import datetime
from pathlib import Path
from constants import Constants as GAME_CONSTANTS

class ProgressSaveManager:
    """
    Manager class for saving progress to file
    """
    def __init__(self):
        """
        Core method for initializing progress data
        """
        self.data = dict()
        self.folder_path = Path(GAME_CONSTANTS.GAME_FOLDER)/GAME_CONSTANTS.PROGRESS_FOLDER

    def collate(self, new_data):
        """
        Core method for collecting progress data
        :param new_data:
        """
        for key, value in new_data.items():
            if key not in self.data:
                self.data[key] = value
            else:
                print(f"Overriding {key} with {value}")
                self.data[key] = value

    def retrieve(self, filename):
        """
        Core method for retrieving progress data from file
        :param filename: string filename
        :return:
        """
        file_path = self.folder_path/filename

        with open(file_path, "r") as f:
            data = json.load(f)
            return data

    def save(self):
        """
        Core method for saving progress to file
        """
        timestamp = datetime.now().strftime(GAME_CONSTANTS.TS_FORMAT)
        filename = f"{GAME_CONSTANTS.CKPT_FILE_PREFIX}{timestamp}{GAME_CONSTANTS.FILE_EXTENSION}"
        file_path = self.folder_path/filename

        with open(file_path, "w") as file:
            json.dump(self.data, file, indent=4)

        print("Progress saved successfully!")
        # print(f"Refer to file {GAME_CONSTANTS.CKPT_FILE_PREFIX}{timestamp}{GAME_CONSTANTS.FILE_EXTENSION}")
        ## TODO: add feature to lock these files so that players cannot modify this file without a decrypt code
