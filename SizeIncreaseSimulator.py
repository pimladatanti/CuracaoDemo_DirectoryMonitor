from time import sleep


def increaseFileSize():
    x = 0
    while x < 1000:
        with open('rawDirectory/testFile.txt', 'a') as myFile:
            myfile = open('rawDirectory/testFile.txt', 'a')
            myfile.write(str(x) + "increasing file size!\n")
            sleep(1)
        x += 1


if __name__ == '__main__':
    increaseFileSize()
