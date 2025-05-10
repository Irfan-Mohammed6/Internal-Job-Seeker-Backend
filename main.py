from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

app = FastAPI()

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cookie': '__stp=eyJ2aXNpdCI6InJldHVybmluZyIsInV1aWQiOiI3NmFkZGRlNy01NzUzLTQxNTUtODllMS1hNDFjNzVkMjNhOTYifQ==; hardcoded_posts_isp_v_43=3%7C1748874541; _fbp=fb.1.1735809010996.349226451936556409; ists=0; pdc_new=24818a6fcda6625cc1041c2e2e34a8ef; pdcVersion=2; u=1; lv=1; l=2onuchx3vgf%2F994powm28ol; is_logged_in=1; specialization_popup_DS=1%7C1748948468; user_id_cookie=23692244; csrf_cookie_name=19582f152cc1d40d4b2e3fb517f1c5a1; role=student; isc=81t8mrbjd23o075oh0cfbmd1pcb7tn52; persistentSessionDateTimeStamp=1746729000; _clck=j4cbrm%7C2%7Cfvr%7C0%7C1239; _gid=GA1.2.1159561490.1746780892; moe_uuid=aa3df14a-9ce5-406e-92ba-cc6b7532158e; PHPSESSID=4h9lotqd69du1a33k8ucbr85t0s9ihpq; persistentSession=f4e93948b8d6355c; sessionToken=0c247fa2; toUpdatePersistentSession=2; _gcl_au=1.1.692884343.1739220488.623508002.1746780904.1746780904; internshipFiltersEncoded=%7B%22employment_type%22%3A%22job%22%2C%22categories%22%3A%5B%22Front%20End%20Development%22%2C%22Javascript%20Development%22%2C%22Web%20Development%22%5D%2C%22locations%22%3A%5B%22Bangalore%22%5D%2C%22work_from_home%22%3Atrue%2C%22remote_job%22%3Atrue%2C%22job_internship_checked%22%3Afalse%7D; internshipSearchUrl=%2Fjobs%2Ffront-end-development%252Cjavascript-development%252Cweb-development-jobs-in-bangalore%2Fwork-from-home%2Fexperience-1%2F; detailPageReferrer=https%3A%2F%2Finternshala.com%2Fjobs%2Ffront-end-development%2Cjavascript-development%2Cweb-development-jobs-in-bangalore%2Fwork-from-home%2Fexperience-1%2F; applicationReferral=search_filters; nav_bottom_courses_amber_dot=1%7C1747386279; _ga=GA1.2.38482686.1676037170; AWSALB=GAxtyz5eX7p9WtisiO2VTfvOrH2IF07yyyIiQqP2+sVAbldnYi2wxvxhDH/rzt737ezKUVXUJotxY9WEeFFeRWDv+Y375GyYJgrtl5f0cDKbOTDmLUfr97zgU8nw; AWSALBCORS=GAxtyz5eX7p9WtisiO2VTfvOrH2IF07yyyIiQqP2+sVAbldnYi2wxvxhDH/rzt737ezKUVXUJotxY9WEeFFeRWDv+Y375GyYJgrtl5f0cDKbOTDmLUfr97zgU8nw; _ga_XHNTE5RRF4=GS2.1.s1746780891$o274$g1$t1746781727$j60$l0$h0'
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
