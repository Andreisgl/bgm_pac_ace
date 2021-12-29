## AC Audio File Organizer - by Andreisgl @ Github
# Manipulates the folder with audio files in order to organize each file to aid editing.

# Dependencies:
    # MFAudio

import os
import shutil
import subprocess

basedir = 'BGM'
metadataFolder = 'orgMeta'
mainMetadataFile = 'mainMeta.txt' #Contains the names of all audio files to be worked with

saveFolder = 'save1'

manipulateMode = 0 # Mode for 'manipulateFile' function.
                        # 0: Convert audio
                        # 1: Reproduce audio
aczRADIOArguValues = [22050, 1, 320, 0, 'WAVU', 22050, 1, 320] # Temporary. Argument value set for ACZ RADIOUSA files.



def manipulateFile(inputFilename, outputFilename, arguValues, mode):
    # Parameter list for function:
        # inputFilename - Name of file to be read.
        # outputFilename - Name of resulting file. Mandatory, but only really used if convert mode is selected ('mode' == 0).
        # arguValues - List of the values for the MFAudio arguments, minus input and output filenames, described below. Contais 8 indexes
        # mode - Selects function mode.
            # mode == 0: Convert audio
            # mode == 1: Reproduce audio

    # Argument list for MFAudio, with indexes for the lists used in this code
        #0 -  /IFnnnnn	Input frequency
        #1 -  /ICn	Input channels
        #2 -  /IIxxxx	Input interleave (hex)
        #3 -  /IHxxxx	Input headerskip (hex)
        #4 -  /OTtttt	Output type (WAVU, VAGC,
        # 	            SS2U, SS2C, RAWU, RAWC)
        #5 -  /OFnnnnn	Output frequency
        #6 -  /OCn	Output channels
        #7 -  /OIxxxx	Output interleave (hex)
        #8 -  "InputFile"	Input file to play/convert
        #9 -  "OutputFile"	Output file to convert to

    exeFilename = 'MFAudio.exe'

    batFilename = 'temp.bat' # Temporary .bat file to execute MFAudio.exe (It only worked when I did this...)

    ARGU = ['/IF', '/IC', '/II', '/IH', '/OT', '/OF', '/OC', '/OI'] #Contains the core arguments.
    currentArguValue = [] #The current set of argument VALUES currently being used.
    concatArgu = [] #Concatenated Arguments and values
    argumentBuffer = ''
    currentArguValue = arguValues


    for i in range(len(ARGU)): # Concatenates each core parameter with it's value individually, by list index.
        concatArgu.append( ARGU[i] + str(currentArguValue[i]) )

    for i in range(len(ARGU)): # Creates string based on 'concatArgu' list contents.
        argumentBuffer = argumentBuffer + concatArgu[i] + ' '

    argumentBuffer = exeFilename + ' ' + argumentBuffer + '"' + inputFilename + '"' # Adsa input filename to 'argumentBuffer' string and...
    

    if mode == 0: # ... if the mode is "Convert (0)", add output filename as well.
        argumentBuffer = argumentBuffer + ' ' + '"' + outputFilename + '"'
    
    with open(batFilename, 'w') as batFile:
        batFile.write(argumentBuffer)
        
    subprocess.run(batFilename)
    os.remove(batFilename)

if os.path.exists(basedir) == False: # Check if the folder to be accessed exists. If not, the program quits.
    exit(0)

if os.path.exists(metadataFolder) == False: # Check if the folder to be accessed exists. If not, the creates one.
    os.mkdir(metadataFolder)





nof = len(os.listdir(basedir))

parameterList = ['CHARACTER', 'MISSION', 'ACESTYLE'] # This list stores all parameters that will be used to separate files. E.g: "CHARACTER", "MISSION"...



fileList = [] # List of all files on 'basedir'
for f in os.listdir(basedir):
    fileList.append(f)

with open(metadataFolder + '/' + mainMetadataFile, 'w') as metaFile: # Store al filenames in file
    for i in range(nof):
        metaFile.write(fileList[i])
        if i < nof - 1:
            metaFile.write('\n')


fileDataList = []
for i in range(nof):
    fileDataList.append('')
for i in range(nof):
    toExit = False
    print('File: ' + fileList[i] + '\n' )
    fileDataList[i] = fileList[i]
    for g in parameterList:
        print('Input parameter ' + g + ': ')
        x = input()
        if x == 'exit':
            toExit = True
            break
        fileDataList[i] = fileDataList[i] + ',' + g + '.' + x
    if toExit == True:
        print('Exiting...')
        break

saveFileList = 'FL.txt' # File that stores the list 'FileList' to resume work later
saveFileDataList = 'FDL.txt' # File that stores the list 'FileDataList' to resume work later

with open(saveFolder + '/' + saveFileList, 'w') as sFL:
    for i in range(len(fileList)):
        w = fileList[i] + '\n'
        sFL.write(w)
with open(saveFolder + '/' + saveFileDataList, 'w') as sFDL:
    for i in range(len(fileDataList)):
        w = fileDataList[i] + '\n'
        sFDL.write(w)




    





print('lol')
# manipulateFile('lol.npsf', 'lol.wav', aczRADIOArguValues, 0)