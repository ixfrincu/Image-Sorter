import os
import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from re import search

date_time_tag = 36867

imgFormats = ['png', 'jpg', 'jpeg']
videoFormats = ['m4v', 'mov', 'mp4']

months = {
    "1": "01.Ianuarie",
    "2": "02.Februarie",
    "3": "03.Martie",
    "4": "04.Aprilie",
    "5": "05.Mai",
    "6": "06.Iunie",
    "7": "07.Iulie",
    "8": "08.August",
    "9": "09.Septembrie",
    "10": "10.Octombrie",
    "11": "11.Noiembrie",
    "12": "12.Decembrie"
}

# to be replaced
os.chdir('C:\\Users\\Ionut\\Desktop\\imgsort\\files')

for xfile in os.listdir():
    filename = os.fsdecode(xfile)
    print(f'Processing {filename}...')
    name = filename.split('.')[0]
    if os.path.isdir(filename):
        continue
    elif filename.endswith('.py'):
        continue
    elif filename.split('.')[1].lower() in imgFormats:
        try:
            imx = Image.open(xfile)
            exif = imx._getexif()
            imx.close()
            if date_time_tag in exif:
                datestr = exif[date_time_tag].split()
                dateobj = datetime.datetime.strptime(datestr[0], "%Y:%m:%d")
                month = months.get(f'{dateobj.month}')
                dirpath = f'{dateobj.year}/{month}/{dateobj.day}.{dateobj.month}.{dateobj.year}/'
                os.makedirs(dirpath, exist_ok=True)
                os.rename(filename, dirpath + filename)
            continue
        except Exception as err:
            print(err)
            continue
    elif filename.split('.')[1].lower() in videoFormats:
        parser = createParser(filename)
        if not parser:
            continue
        with parser:
            try:
                metadata = extractMetadata(parser)
            except Exception as err:
                print(err)
                metadata = None
        if not metadata:
            continue
        for line in metadata.exportPlaintext():
            toSearch = line.split(':')[0]
            info = line.split(':')[1]
            splitted = info.split()
            if search('Creation', toSearch):
                dateobj = datetime.datetime.strptime(
                    splitted[0], "%Y-%m-%d")
                month = months.get(f'{dateobj.month}')
                dirpath = f'{dateobj.year}/{month}/{dateobj.day}.{dateobj.month}.{dateobj.year}/'
                os.makedirs(dirpath, exist_ok=True)
                os.rename(filename, dirpath + filename)
