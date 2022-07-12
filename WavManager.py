import shutil
import wave
import sys


class WavManager:

    @staticmethod
    def encrypt(file_to_encrypt):
        # get bytes from wave
        wav_reader = wave.open(file_to_encrypt, mode='rb')
        channels = wav_reader.getnchannels()
        sample_width = wav_reader.getsampwidth()
        frame_rate = wav_reader.getframerate()
        total_frames = wav_reader.getnframes()
        wav_as_bytes = wav_reader.readframes(wav_reader.getnframes())
        wav_reader.close()
        num = len(wav_as_bytes)

        # convert wave bytes to int to binary
        wav_as_int = int.from_bytes(wav_as_bytes, byteorder=sys.byteorder)
        wav_as_binary_string = bin(wav_as_int)

        with open("wav_original.txt", 'w') as f:
            f.write(wav_as_binary_string)

        # reverse file
        header = wav_as_binary_string[0:2]
        wav_as_binary_string = wav_as_binary_string[2:]

        #swap0 = wav_as_binary_string.replace("0", "2")
        #swap1 = swap0.replace("1", "0")
        #swap2 = swap1.replace("2", "1")
        #wav_as_binary_string = swap2

        with open("wav_as_encrypted_bin_swap.txt", 'w') as f:
            f.write(wav_as_binary_string)

        wav_as_encrypted_string = header + wav_as_binary_string[::-1]

        with open("wav_as_encrypted_bin_final.txt", 'w') as f:
            f.write(wav_as_encrypted_string)

        wav_as_int = int(wav_as_encrypted_string, 2)
        wav_as_encrypted_bytes = wav_as_int.to_bytes(num, byteorder=sys.byteorder)

        print("before write")
        # write to wav file
        f = wave.open(file_to_encrypt, mode="wb")
        f.setnchannels(channels)
        f.setsampwidth(sample_width)
        f.setframerate(frame_rate)
        f.writeframes(wav_as_encrypted_bytes)
        f.close()

    @staticmethod
    def decrypt(file_to_decrypt):
        # get bytes from wave
        wav_reader = wave.open(file_to_decrypt, mode='rb')
        channels = wav_reader.getnchannels()
        sample_width = wav_reader.getsampwidth()
        frame_rate = wav_reader.getframerate()
        total_frames = wav_reader.getnframes()
        wav_as_bytes = wav_reader.readframes(wav_reader.getnframes())
        wav_reader.close()
        num = len(wav_as_bytes)

        # convert wave bytes to int to binary
        wav_as_int = int.from_bytes(wav_as_bytes, byteorder=sys.byteorder)
        wav_as_encrypted_string = bin(wav_as_int)

        # reverse file back to original
        header = wav_as_encrypted_string[0:2]
        wav_as_encrypted_string = wav_as_encrypted_string[2:]

        wav_as_decrypted_string = wav_as_encrypted_string[::-1]
        #swap0 = wav_as_decrypted_string.replace("0", "2")
        #swap1 = swap0.replace("1", "0")
        #swap2 = swap1.replace("2", "1")
        #wav_as_decrypted_string = swap2

        #with open("wav_as_decrypted_bin_swap.txt", 'w') as f:
            #f.write(wav_as_decrypted_string)
            # byte object became binary string
        wav_as_decrypted_string = header + wav_as_decrypted_string

        with open("wav_as_decrypted_bin_final.txt", 'w') as f:
            f.write(wav_as_decrypted_string)

        # convert int to bytes
        wav_as_int = int(wav_as_decrypted_string, 2)
        wav_as_decrypted_bytes = wav_as_int.to_bytes(num, byteorder=sys.byteorder)

        # write to wav file
        f = wave.open(file_to_decrypt, mode="wb")
        f.setnchannels(channels)
        f.setsampwidth(sample_width)
        f.setframerate(frame_rate)
        f.writeframes(wav_as_decrypted_bytes)
        f.close()

if __name__ == '__main__':
    WavManager.decrypt("encryptedDirectory/crickets.wav")
    WavManager.decrypt("encryptedDirectory/crickets1.wav")
    shutil.move("encryptedDirectory/crickets.wav", "rawDirectory/crickets.wav")
    shutil.move("encryptedDirectory/crickets1.wav", "rawDirectory/crickets1.wav")