from bs4 import BeautifulSoup
from selenium import webdriver

from database import SessionLocal
from models.postal_code import PostalCode


class ETL:
    def __init__(self, postal_code_str: str):
        self.postal_code_str = postal_code_str

    def get_timezone_title(self) -> str:
        with SessionLocal() as session:
            postal_code = session.query(PostalCode).filter(PostalCode.index == self.postal_code_str).first()
            if postal_code is None:
                raise ValueError(f"Postal code {self.postal_code_str} not found")
            with webdriver.Chrome() as driver:
                driver.get(f'https://postal-codes.cybo.com/russia/{self.postal_code_str}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                table = soup.find('table', class_='nw-table')
            timezone = table.find('td', text='Timezone').parent.find_all('td')[-1].text
            postal_code.timezone = timezone
            session.commit()
            return timezone
