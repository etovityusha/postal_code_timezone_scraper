from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from chrome_wrapper import ChromeWrapper
from database import SessionLocal
from models.postal_code import PostalCode


class ETL:
    def __init__(self, postal_code_str: str):
        self.postal_code_str = postal_code_str

    def set_timezone_title(self) -> str | None:
        with SessionLocal() as session:
            postal_code = session.query(PostalCode).filter(PostalCode.index == self.postal_code_str).first()
            if postal_code is None:
                raise ValueError(f"Postal code {self.postal_code_str} not found")
            if postal_code.timezone is not None:
                return postal_code.timezone
            with ChromeWrapper() as driver:
                driver.get(f'https://postal-codes.cybo.com/search/?q={self.postal_code_str}&pl=&i=&t=')
                try:
                    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'nw-table')))
                except TimeoutException:
                    driver.save_body_screenshot()
                    return
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                tables = soup.find_all('table', class_='nw-table')
                if not tables:
                    print('No tables found')
                    driver.save_body_screenshot()
                    return
            table = tables[0]
            timezone = table.find('td', text='Timezone').parent.find_all('td')[-1].text
            postal_code.timezone = timezone
            session.commit()
            return timezone
