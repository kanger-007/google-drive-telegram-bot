import os
import wget
import glob
import youtube_dl
from pySmartDL import SmartDL
from urllib.error import HTTPError
from youtube_dl import DownloadError
from bot import DOWNLOAD_DIRECTORY, LOGGER

import os
import json
import subprocess
import argparse
import sys
import pyfiglet
from rich import print
from typing import DefaultDict


currentFile = __filen__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)

youtubedlexe = dirPath + '/binaries/yt-dlp.exe'
aria2cexe = dirPath + '/binaries/aria2c.exe'
mp4decryptexe = dirPath + '/binaries/mp4decrypt_new.exe'
mkvmergeexe = dirPath + '/binaries/mkvmerge.exe'
SubtitleEditexe = dirPath + '/binaries/SubtitleEdit.exe'

mpdurl = str(args.mpd)
output = str(args.output)
subtitle = str(args.subtitle)

def download_file(url, dl_path):
  try:
    dl = SmartDL(url, dl_path, progress_bar=False)
    LOGGER.info(f'Downloading: {url} in {dl_path}')
    dl.start()
    return True, dl.get_dest()
  except HTTPError as error:
    return False, error
  except Exception as error:
    try:
      filename = wget.download(url, dl_path)
      return True, os.path.join(f"{DOWNLOAD_DIRECTORY}/{filename}")
    except HTTPError:
      return False, error

if args.id:

    subprocess.run([youtubedlexe, '-k', '--allow-unplayable-formats', '--no-check-certificate', '-F', mpdurl])

    vid_id = input("\nEnter Video ID : ")
    audio_id = input("Enter Audio ID : ")
    subprocess.run([youtubedlexe, '-k', '--allow-unplayable-formats', '--no-check-certificate', '-f', audio_id, '--fixup', 'never', mpdurl, '-o', 'encrypted.m4a', '--external-downloader', aria2cexe, '--external-downloader-args', '-x 16 -s 16 -k 1M'])
    subprocess.run([youtubedlexe, '-k', '--allow-unplayable-formats', '--no-check-certificate', '-f', vid_id, '--fixup', 'never', mpdurl, '-o', 'encrypted.mp4', '--external-downloader', aria2cexe, '--external-downloader-args', '-x 16 -s 16 -k 1M'])

else:
    subprocess.run([youtubedlexe, '-k', '--allow-unplayable-formats', '--no-check-certificate', '-f', 'ba', '--fixup', 'never', mpdurl, '-o', 'encrypted.m4a', '--external-downloader', aria2cexe, '--external-downloader-args', '-x 16 -s 16 -k 1M'])
    subprocess.run([youtubedlexe, '-k', '--allow-unplayable-formats', '--no-check-certificate', '-f', 'bv', '--fixup', 'never', mpdurl, '-o', 'encrypted.mp4', '--external-downloader', aria2cexe, '--external-downloader-args', '-x 16 -s 16 -k 1M'])    

def getkeys():
    with open("keys.txt", 'r') as f:
        file = f.readlines()

    length = len(file)

    keys = ""
    for i in range(0, length):
        key = file[i][33 : 65]
        kid = file[i][0 : 32]

        keys += f'--key {kid}:{key} '
        return keys


def getkeys1():
    with open("keys (1).txt", 'r') as f:
        file = f.readlines()

    length = len(file)

    keys = ""
    for i in range(0, length):
        key = file[i][33 : 65]
        kid = file[i][0 : 32]

        keys += f'--key {kid}:{key} '
        return keys

print("\nDecrypting .....")
try:
    subprocess.run(f'{mp4decryptexe} --show-progress {getkeys()} encrypted.m4a decrypted.m4a', shell=True)
    subprocess.run(f'{mp4decryptexe} --show-progress {getkeys()} encrypted.mp4 decrypted.mp4', shell=True)
except:
    subprocess.run(f'{mp4decryptexe} --show-progress {getkeys1()} encrypted.m4a decrypted.m4a', shell=True)
    subprocess.run(f'{mp4decryptexe} --show-progress {getkeys1()} encrypted.mp4 decrypted.mp4', shell=True)    

if args.subtitle:
    subprocess.run(f'{aria2cexe} {subtitle}', shell=True)
    os.system('ren *.xml en.xml') # Change this to your subtitle extension
    subprocess.run(f'{SubtitleEditexe} /convert en.xml srt', shell=True) # Change .xml to your extension    
    print("Merging .....")
    subprocess.run([mkvmergeexe, '--ui-language' ,'en', '--output', output +'.mkv', '--language', '0:eng', '--default-track', '0:yes', '--compression', '0:none', 'decrypted.mp4', '--language', '0:eng', '--default-track', '0:yes', '--compression' ,'0:none', 'decrypted.m4a','--language', '0:eng','--track-order', '0:0,1:0,2:0,3:0,4:0', 'en.srt'])
    print("\nAll Done .....")
else:
    print("Merging .....")
    subprocess.run([mkvmergeexe, '--ui-language' ,'en', '--output', output +'.mkv', '--language', '0:eng', '--default-track', '0:yes', '--compression', '0:none', 'decrypted.mp4', '--language', '0:eng', '--default-track', '0:yes', '--compression' ,'0:none', 'decrypted.m4a','--language', '0:eng','--track-order', '0:0,1:0,2:0,3:0,4:0'])
    print("\nAll Done .....")

