from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

app = FastAPI()

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'text/html',
    'Cookie': 'YOUR_COOKIE_HERE'  # If necessary for authentication
}

@app.get("/internshala", tags=["Internships"])
def get_openings():
    urls = [
        "https://internshala.com/jobs/front-end-development,javascript-development,web-development-jobs-in-bangalore/work-from-home/experience-1/",
        "https://internshala.com/jobs/front-end-development,javascript-development,web-development-jobs-in-bangalore/work-from-home/experience-1/page-2/"
    ]

    all_jobs = []

    for url in urls:
        try:
            res = requests.get(url, headers=headers)
            if res.status_code != 200:
                continue

            soup = BeautifulSoup(res.text, 'html.parser')
            internships = soup.find_all('div', class_='individual_internship')

            for job in internships:
                container = job.find('div', class_='internship_meta')
                if not container:
                    continue

                job_tag = container.find('a', class_='job-title-href')
                if not job_tag:
                    continue

                job_title = job_tag.text.strip()
                job_link = "https://internshala.com" + job_tag['href']
                company = container.find('p', class_='company-name').text.strip()

                details = job.find_all('div', class_='row-1-item')
                location = experience = salary = ""
                for item in details:
                    icon = item.find('i')
                    if not icon: continue
                    if "ic-16-home" in icon['class']:
                        location = item.text.strip()
                    elif "ic-16-briefcase" in icon['class']:
                        experience = item.text.strip()
                    elif "ic-16-money" in icon['class']:
                        salary_tags = item.find_all('span')
                        salaries = [tag.text.strip() for tag in salary_tags if tag.text.strip()]
                        salary = salaries[0] if salaries else ""

                job_data = {
                    "title": job_title,
                    "company": company,
                    "location": location,
                    "experience": experience,
                    "salary": salary,
                    "link": job_link
                }
                all_jobs.append(job_data)

        except Exception as e:
            print(f"Error: {e}")
            continue

    return {"jobs": all_jobs}
