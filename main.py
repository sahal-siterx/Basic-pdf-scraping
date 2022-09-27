import resume_scraper as rs



def main() :
    pdf = rs.ResumeScraper('sahal_resume.pdf')
    pdf.resume_to_json()


if __name__ == '__main__' :
    main()
