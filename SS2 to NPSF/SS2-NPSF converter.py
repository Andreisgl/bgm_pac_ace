##ACZ SS2 to NPSF converter by death_the_d0g (death_the_d0g @ Twitter)
##====================================================================
##This script generates a NPSF file from a SS2 file. Place your SS2 files in the same folder as this script and execute it.
##v1.0, still needs a lot of code cleaning
##TODO: check if the SS2 files contains their total sample value stored somewhere in their data, or find a way to calculate it.
##TODO: figure what these unkval values are.

import os
import shutil
import textwrap
basedir = os.getcwd()

def ssdos():
    while True:
        try:
            print(textwrap.fill("///INPUT///: Type the name (plus extension) of the SS2 file to convert:", width = 72))
            ssdos_file = open(input(">>> "), "rb+")
        except FileNotFoundError as e:
            print()
            print(textwrap.fill("///ERROR///: File does not exist.", width = 72))
            print()
        else:
            sshb_header = b'\x53\x53\x68\x64'
            sshd_header = b'\x53\x53\x62\x64'
            sshb_header_check = ssdos_file.read(4)
            ssdos_file.seek(32, 0)
            sshd_header_check = ssdos_file.read(4)
            ssdos_file.seek(0, 0)
            if (sshb_header_check != sshb_header) or (sshd_header_check != sshd_header):
                print()
                print("///ERROR///: Not a valid SS2 file.")
                print()
            else:
                return ssdos_file

def file_conv(ssdos_file):
    val = 0
    header = [78, 80, 83, 70]
    unkval1 = [0, 16, 0, 0]
    channel = [2, 0, 0, 0] ##TODO: add an option to create mono audio files (for speeches/voices)
    audio_stream_offset = [0, 8, 0, 0]
    audio_freq = [68, 172, 0, 0]
    unkval3 = [20, 0, 0, 0]
    unkval4 = [1, 0, 0, 0]
    unkval5 = [64, 0, 0, 0]
    while True:
        try:
            print(textwrap.fill("///INPUT///: Type the total duration of your custom music track in sample values: ", width = 72))
            total_sample_value = int(input(">>> "))
        except ValueError as e:
            print()
            print (textwrap.fill("///ERROR///: Integer values only.", width = 72))
            print()
        else:
            break
    ssdos_file.seek(0, os.SEEK_END)
    ssdos_stream = ssdos_file.tell()
    ssdos_stream_size = ssdos_stream - 40
    ssdos_file.seek(40, 0)
    ssdos_stream_data = ssdos_file.read(ssdos_stream_size)
    npsf_f_name = str(os.path.splitext(ssdos_file.name)[0]) + ".npsf"
    npsf_f = open(npsf_f_name, "wb")
    npsf_f.write(bytearray(header))
    npsf_f.write(bytearray(unkval1))
    while True:
        print()
        print(textwrap.fill("///INPUT///: Does your custom music have loop points? (y/n):", width = 72))
        does_it_loop = str(input(">>> "))
        if does_it_loop == "y":
            while True:
                try:
                    print()
                    print(textwrap.fill("///INPUT///: Type the start loop point value of your song in samples:", width = 72))
                    loop_start_point = int(input(">>> "))
                    print()
                    print(textwrap.fill("///INPUT///: Type the end loop point value of your song in samples:", width = 72))
                    loop_end_point = int(input(">>> "))
                    print()
                except ValueError as e:
                    print()
                    print (textwrap.fill("///ERROR///: Integer values only.", width = 72))
                    print()
                else:
                    break
            ls = loop_start_point
            le = round((loop_end_point * 16) / 28)
            unkval2 = [153, 3, 0, 0]
            break
        elif does_it_loop == "n":
            ls = 4294967295
            le = round((total_sample_value * 28) / 16)
            unkval2 = [232, 3, 0, 0]
            break
        else:
            print()
            print("///ERROR///: Not a valid option.")
            print("///INFO///: Only y or n are allowed.")
            print()
    npsf_f.write(le.to_bytes(4,"little"))
    npsf_f.write(bytearray(channel))
    npsf_f.write(bytearray(audio_stream_offset))
    npsf_f.write(ls.to_bytes(4,"little"))
    npsf_f.write(bytearray(audio_freq))
    npsf_f.write(bytearray(unkval2))
    npsf_f.write(bytearray(unkval3))
    npsf_f.write(bytearray(unkval4))
    npsf_f.write(bytearray(8))
    npsf_f.write(bytearray(unkval5))
    strng = str((os.path.splitext(ssdos_file.name)[0]) + ".wav")
    ##strng_spliced = strng[5:]
    padx = 60 - len(strng)
    encoded_strng = strng.encode()
    npsf_f.write(bytearray(encoded_strng))
    npsf_f.write(bytearray(padx))
    npsf_f.write(bytearray(2048-112))
    npsf_f.write(ssdos_stream_data)
    npsf_f.close()
    ssdos_file.close()
    print(textwrap.fill("///INFO///: File successfully converted!.", width = 72))
    
def continue_op(ssdos_file):
    while True:
        print(textwrap.fill("///INPUT///: Would you like to convert more files? (y/n): ", width = 72))
        continue_prompt = str(input(">>> "))
        if continue_prompt == "y":
            print()
            ssdos_file = ssdos()
            print()
            file_conv(ssdos_file)
            print()
            continue_op(ssdos_file)
        elif continue_prompt == "n":
            print()
            print(textwrap.fill("///INFO///: Rename and drop the newly created NSPF file(s) in the BGM folder.", width = 72))
            print()
            a = input("///INPUT///: Press any key to exit...")
            if a:
                exit(0)
            else:
                exit(0)
        else:
            print()
            print("///ERROR///: Only y or n are allowed.")
            print()

print(textwrap.fill("AC ZERO SS2 to NSPF converter by death_the_d0g (death_the_d0g @ Twitter)", width = 80))
print(textwrap.fill("========================================================================", width = 80))
print()
print(textwrap.fill("This script generates a NPSF file from a SS2 file.", width = 80))
print()

ssdos_file = ssdos()
print()
file_conv(ssdos_file)
print()
continue_op(ssdos_file)
