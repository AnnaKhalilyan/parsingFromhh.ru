import requests
from bs4 import BeautifulSoup
import csv

url = "https://orsk.hh.ru/search/vacancy?area=1571&professional_role=1&professional_role=2&professional_role=3&professional_role=10&professional_role=12&professional_role=34&professional_role=37&professional_role=55&professional_role=163&professional_role=68&professional_role=70&professional_role=71&professional_role=99&professional_role=170&withTopFilterCatalog=true"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

# print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

# print("vacancy-serp__vacancy" in response.text)

vacancies = soup.find_all(attrs={"data-qa": "vacancy-serp__vacancy"})

# print(len(vacancies))
# print(vacancies[0])


for vac in vacancies:
    title_tag = vac.find(attrs={"data-qa": "serp-item__title"})
    salary_tag = vac.find(attrs={"data-qa": "vacancy-serp__vacancy-compensation"})
    company_tag = vac.find(attrs={"data-qa": "vacancy-serp__vacancy-employer"})
    
    if title_tag:
        title = title_tag.text
        link = title_tag["href"]
        salary = salary_tag.text if salary_tag else "Не указана"
        company = company_tag.text if company_tag else "не указана"
        # print(title)
        # print(link)
        # print(salary)
        # print(company)
        # print("-" * 30)

with open("vacancies.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    
    writer.writerow(["Название", "Компания", "Зарплата", "Ссылка"])

    for vac in vacancies:
        title_tag = vac.find(attrs={"data-qa": "serp-item__title"})
        title = title_tag.text if title_tag else "Нет"
        link = title_tag["href"] if title_tag else "Нет"

        company_tag = vac.find(attrs={"data-qa": "vacancy-serp__vacancy-employer"})
        company = company_tag.text if company_tag else "Не указана"

        salary_tag = vac.find(attrs={"data-qa": "vacancy-serp__vacancy-compensation"})
        salary = salary_tag.text if salary_tag else "Не указана"

        writer.writerow([title, company, salary, link])