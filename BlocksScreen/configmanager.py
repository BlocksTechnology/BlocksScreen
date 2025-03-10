import configparser
import os
import pathlib

class ConfigManager(configparser.ConfigParser):
    baseFilename = "bo_config.cfg"
    dirpath_klipper_print_data = "\printer_data\config"

    def __init__(self, filename: str = baseFilename):
        self.filename = filename
        kpd_dirpath = os.getcwd() + self.dirpath_klipper_print_data

        super(ConfigManager, self).__init__()

        kpd

        ...


    def read_config(self, dir, filename): 
        if os.access(os.path.join(dir, filename), os.X_OK): 
            with _file_handler as  self.read(os.path.join(dir, filename))
                

    def __getitem__(self, key: str) -> configparser.SectionProxy:
        return super().__getitem__(key)

