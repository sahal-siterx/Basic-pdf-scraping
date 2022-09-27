import pdfplumber
import json


class ResumeScraper:
    def __init__(self, file_name):
        self.file_name:str = file_name
        self.pdf_data = ''
        self.person_data = dict()

    def display_data(self):
        print(self.pdf_data)

    def get_pdf_text(self):
        with pdfplumber.open(self.file_name) as pdf:
            for page in pdf.pages:
                self.pdf_data += page.extract_text()
            
            self.pdf_data = self.pdf_data.replace('\ufb01', 'fi')

    def get_personal_info(self):
        data_split_line = self.pdf_data.splitlines()

        personal = {
            'name': data_split_line[0],
            'address': data_split_line[1].split(',')[0],
            'place': data_split_line[1].split(',')[1],
            'district': data_split_line[1].split(',')[2],
            'state': data_split_line[1].split(',')[3],
            'mobile': data_split_line[2].split('|')[0].strip()
        }

        # Data from Personal Details in the pdf
        extra_info = self.pdf_data.split('Personal Details')
        extra_info = extra_info[1].split('Declaration')
        extra_info = extra_info[0].split('\n')

        for i in extra_info:
            if i == '' or i == ' ':
                continue
            else:
                info = i.split(':')
                personal[info[0].strip().replace(' ', '_').lower()] = info[1].strip()
        
        return personal

    def get_social_info(self):
        data_split_line = self.pdf_data.splitlines()

        social = {
            'email': data_split_line[2].split('|')[1].strip().lower(),
            'github': data_split_line[3].split()[1],
            'linkedin': data_split_line[4].split()[1]
        }
        return social


    def get_about(self) :
        data_split_about = self.pdf_data.split('Objective')[1]
        data_about = data_split_about.split('Education')[0].strip().replace('\n', ' ').replace('- ', '-')
        return data_about

    def get_education(self):
        education = []
        data_split_education = self.pdf_data.split('Education', 1)[1]
        data_education = data_split_education.split('Skills')[0].strip().split('\n')
        
        if len(data_education)%3 != 0:
            raise Exception('Education Data is not a multiple of three.')

        i=3
        while i <= len(data_education):
            data_edu = data_education[i-3: i]


            edu_info = {
                'institution': data_edu[0].split(',')[0].strip(),
                'place': data_edu[0].split(',', 1)[1].strip(),
                'studied': data_edu[1].rsplit(' ', 2)[0].strip().replace('- ', '-'),
                'graduated': '-'.join([data_edu[1].rsplit(' ', 2)[1], data_edu[1].rsplit(' ', 2)[2]])
            }

            education.append(edu_info)
            i+=3
        
        return education

    def get_skills(self):
        data_skills_split = self.pdf_data.split('Skills')[1].strip()
        skills = data_skills_split.split('Projects')[0].strip().split('\n')
        return skills

    def get_projects(self):
        projects = []
        data_projects_split = self.pdf_data.split('Projects')[1].strip()
        data_projects = data_projects_split.split('Personal Details')[0].strip().split('\n')

        i = 0
        while i < len(data_projects):
            project = {
                'project_name': data_projects[i],
                'project_description': data_projects[i+1].replace('- ', '-')
            }

            projects.append(project)
            i+=2

        return projects


    def resume_to_json(self):
        self.get_pdf_text()
        self.person_data['personal_info'] = self.get_personal_info()
        self.person_data['social_info'] = self.get_social_info()
        self.person_data['about'] = self.get_about()
        self.person_data['education'] = self.get_education()
        self.person_data['skills'] = self.get_skills()
        self.person_data['projects'] = self.get_projects()

        file_name = self.file_name.replace('pdf', 'json')

        with open(file_name, 'w') as json_file:
            json.dump(self.person_data, json_file, indent=4)


a = ResumeScraper('sahal_resume.pdf')
a.get_pdf_text()
a.get_personal_info()