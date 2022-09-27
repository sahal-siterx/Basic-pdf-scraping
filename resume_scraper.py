import pdfplumber
import json


class ResumeScraper :
    def __init__(self, file_name) :
        self.file_name = file_name
        self.data = None
        self.data_split_line = None

    def display_data(self) :
        print(self.data)

    def get_pdf_text(self) :
        with pdfplumber.open(self.file_name) as pdf :
            for page in pdf.pages :
                self.data = page.extract_text()
            self.data_split_line = self.data.splitlines()

    def personal_info(self) :
        personal = {
            'name' : self.data_split_line[0],
            'address' : self.data_split_line[1].split(',')[0],
            'place' : self.data_split_line[1].split(',')[1],
            'district' : self.data_split_line[1].split(',')[2],
            'state' : self.data_split_line[1].split(',')[3],
            'mobile' : self.data_split_line[2].split('|')[0].strip()
        }
        return personal

    def social_info(self) :
        social = {
            'email' : self.data_split_line[2].split('|')[1].strip().lower(),
            'github' : self.data_split_line[3].split()[1],
            'linkedin' : self.data_split_line[4].split()[1]
        }
        return social

    def additional_info(self) :
        more_info = dict()
        extra_info = self.data.split('Personal Details')
        extra_info = extra_info[1].split('Declaration')
        extra_info = extra_info[0].split('\n')

        for i in extra_info :
            if i == '' or i == ' ' :
                continue
            else :
                info = i.split(':')
                more_info[info[0].strip().replace(' ', '_').lower()] = info[1].strip()

        return more_info

    def get_about(self) :
        data_about_list = []
        data_split_about = self.data.split('Objective')[1]
        data_about_post = data_split_about.split('Education')[0]
        data_about_post = data_about_post.split('\n')

        for data in data_about_post :
            if data == '' or data == ' ' :
                continue
            data_about_list.append(data)

        data_about = ' '.join(data_about_list).replace('- ', '-')
        return data_about

    def get_education(self) :
        education = []
        data_split_education = self.data.split('Education', 1)[1]
        data_education = data_split_education.split('Skills')[0].strip().split('\n')
        
        if len(data_education)%3 != 0 :
            raise Exception('There is an Error in Education Data...')

        i=3
        while i <= len(data_education) :
            data_edu = data_education[i-3: i]

            print(data_edu)

            edu_info = {
                'institution' : data_edu[0].split(',')[0].strip(),
                'place' : data_edu[0].split(',', 1)[1].strip(),
                'studied' : data_edu[1].rsplit(' ', 2)[0].strip().replace('- ', '-'),
                'graduated' : '-'.join([data_edu[1].rsplit(' ', 2)[1], data_edu[1].rsplit(' ', 2)[2]])
            }

            education.append(edu_info)
            i+=3
        
        return education

    def get_skills(self) :
        data_skills_split = self.data.split('Skills')[1].strip()
        skills = data_skills_split.split('Projects')[0].strip().split('\n')
        return skills

    def get_projects(self) :
        projects = []
        data_projects_split = self.data.split('Projects')[1].strip()
        data_projects = data_projects_split.split('Personal Details')[0].strip().split('\n')

        i = 0
        while i < len(data_projects) :
            project = {
                'project_name' : data_projects[i],
                'project_description' : data_projects[i+1].replace('- ', '-')
            }

            projects.append(project)
            i+=2

        return projects



pdf = ResumeScraper('sahal_resume.pdf')
pdf.get_pdf_text()
pdf.display_data()
pdf.get_projects()