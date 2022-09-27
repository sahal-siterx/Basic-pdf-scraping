import sys
from os import path
from resume_scraper import ResumeScraper



if len(sys.argv) < 2:
    raise Exception('Please enter the file to extract')
elif len(sys.argv) > 2:
    raise Exception('Please pass only one file to extract at a time')
else:
    file_name = sys.argv[1]
    if not path.isfile(file_name):
        raise Exception('Oops... This file does not exist!')



def main():
    pdf = ResumeScraper(file_name)
    pdf.resume_to_json()


if __name__ == '__main__':
    main()
