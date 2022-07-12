import os
import shutil
from time import sleep
from WavManager import WavManager


class DirectoryMonitor:

    def __init__(self, input_directory):
        self.input_directory = input_directory
        self.allFiles = {}

    def walkThroughDirectory(self):
        while True:
            for dirpath, dnames, fnames in os.walk(self.input_directory):
                for f in fnames:
                    # if the extension is a wav file
                    if f.find(".wav") != -1:
                        input_file_path = os.path.join(
                            "rawDirectory", f)
                        # if the file is in the dictionary,
                        if f in self.allFiles:
                            # check file size for size increase
                            self.monitorFileSize(f, self.allFiles[f])
                        else:  # if not in dictionary,
                            # get current file size
                            current_size = os.stat(input_file_path)
                            current_file_size = current_size.st_size
                            # save file to dictionary as key and its size as the value
                            self.allFiles[f] = current_file_size
            sleep(10)

    def monitorFileSize(self, input_file, previous_file_size):
        # get current file size
        input_file_path = os.path.join("rawDirectory", input_file)
        current_size = os.stat(input_file_path)
        current_file_size = current_size.st_size

        # compare current to previous file size
        comp = current_file_size - previous_file_size

        # if file is changing in size, ADD NEW SIZE TO FILE DICTIONARY. MOVE ON TO NEXT FILE.
        if comp != 0:
            self.allFiles[input_file] = current_file_size
            print(str(input_file) + ": " + str(comp) + " bytes changed" + "\n")
        else:  # otherwise, if file size is constant
            # encrypt file
            WavManager.encrypt(input_file_path)
            # move file
            self.moveFile(input_file)
            # remove file entry from dictionary
            self.allFiles.pop(input_file)

    def moveFile(self, input_file):
        source = "rawDirectory/"
        destination = "encryptedDirectory/"

        shutil.move(source + input_file, destination + input_file)


if __name__ == '__main__':
    directoryMonitor = DirectoryMonitor("rawDirectory")
    directoryMonitor.walkThroughDirectory()
