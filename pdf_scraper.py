import pdfplumber
import json



with pdfplumber.open('sahal_resume.pdf') as pdf :
  for page in pdf.pages :
    data = page.extract_text()
    data = data.replace("\ufb01", "fi")
    # print(data)


data_split_line = data.splitlines()
# print(data_split_line)


#########################################################
# Objective

data_split_objective = data.split('Objective')
data_objective_post = data_split_objective[1]
data_objective_split = data_objective_post.split('Education')
data_objective = ' '.join(data_objective_split[0].split('\n'))
# print(data_split_objective)
# print(data_split_objective[1])
# print(data_objective)
#########################################################


#########################################################
# Education

data_split_education = data.split('Education', 1)
data_education_post = data_split_education[1]
data_education_split = data_education_post.split('Skills', 1)
data_education = data_education_split[0]
data_education = data_education.split('\n')
data_education.remove('')
data_education.remove('')

# print(data_education)


if len(data_education)%3 != 0 :
  raise Exception('There is an Error in education data')


i=3
education = []

while i <= len(data_education) :
  data_edu = data_education[i-3:i]
  # print(data)

  edu_info = {
    'institution': data_edu[0].split(',', 1)[0],
    'place' : data_edu[0].split(',', 1)[1],
    'studied' : data_edu[1].rsplit(' ', 2)[0].strip(),
    'graduated' : '-'.join([data_edu[1].rsplit(' ', 2)[1], data_edu[1].rsplit(' ', 2)[2]])
  }

  education.append(edu_info)
  i+=3
#########################################################

#########################################################
# Skills

skills = []

data_split_skills = data.split('Skills')
data_skills_post = data_split_skills[1].split('Projects')
data_skills = data_skills_post[0]

data_skills = data_skills.split('\n')
data_skills.remove('')
data_skills.remove('')

for skill in data_skills :
  # print(skill.strip())

  # if 'Postgresql and Mongodb' in skill :
    # breakpoint()
  skills.append(skill.strip())

# print(data_skills)
# print(skills)
#########################################################


#########################################################
# Projects

projects = []

data_split_project = data.split('Projects')
data_post_project = data_split_project[1]
data_projects = data_post_project.split('Personal Details')
data_projects = data_projects[0]
data_projects = data_projects.split('\n')
data_projects.remove('')
data_projects.remove('')

i=0
while i < len(data_projects) :
  project = {
    'project_name' : data_projects[i],
    'project_description' : data_projects[i+1]
  }

  projects.append(project)
  i+=2

# print(projects)
#########################################################


#########################################################
# Additional infos

additional_info = dict()

data_split_extra = data.split('Personal Details')
data_extra_post = data_split_extra[1]
data_extra = data_extra_post.split('Declaration')
data_extra = data_extra[0]
data_extra = data_extra.split('\n')

# print(data_extra)

for i in data_extra :
  if i == '' or i == ' ' :
    continue
  else :
    info = i.split(':')
    
    additional_info[info[0].strip().replace(' ', '_').lower()] = info[1].strip()

    # print(additional_info)

#########################################################


#########################################################
# Final Dictionary
data_dict = dict()


data_dict['name'] = data_split_line[0]
data_dict['address'] = data_split_line[1].split(',')[0]
data_dict['place'] = data_split_line[1].split(',')[1]
data_dict['district'] = data_split_line[1].split(',')[1]
data_dict['state'] = data_split_line[1].split(',')[1]
data_dict['mobile'] = data_split_line[2].split('|')[0]
data_dict['email'] = data_split_line[2].split('|')[1]
data_dict['github'] = data_split_line[3].split()[1]
data_dict['linkedin'] = data_split_line[4].split()[1]
data_dict['about'] = data_objective
data_dict['education'] = education
data_dict['skills'] = skills
data_dict['project'] = projects
data_dict['additional_info'] = additional_info
#########################################################


person = json.dumps(data_dict, indent=4)
print(person)

