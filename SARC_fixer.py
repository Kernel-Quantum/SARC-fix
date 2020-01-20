import zipfile
import json
import os

zipFileName = input('Enter the name of your zip file (inlcuding .zip): ')

with zipfile.ZipFile(zipFileName, 'r') as zipFileContents:
    replayFileNames = zipFileContents.namelist()
    zipFileContents.extractall()

for replayFileName in replayFileNames:
    print('Extracting: ' + replayFileName)
    with zipfile.ZipFile(replayFileName, 'r') as replayFileContents:
        replayComponents = replayFileContents.namelist()
        replayFileContents.extractall()
        print(' Reading metaData.json')
        with open('metaData.json', 'r') as replayJson:
            for data in replayJson:
                print('  Setting fileFormatVersion to 9')
                jsonData = json.loads(data)
                jsonData['fileFormatVersion'] = 9

        print(' Writing new json to metaData.json')
        with open('metaData.json', 'w') as replayJson:
            json.dump(jsonData, replayJson)


    os.remove(replayFileName)
    print(' Deleted old ' + replayFileName)

    with zipfile.ZipFile(replayFileName, 'w', compression=zipfile.ZIP_DEFLATED) as replayFile:
        replayFile.write(replayComponents[0])
        replayFile.write(replayComponents[1])
    print(' Created new ' + replayFileName)

    os.remove(replayComponents[0])
    os.remove(replayComponents[1])
print('Fix completed')
