from bs4 import BeautifulSoup

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
            other_postal_with_tz = session.query(PostalCode).filter(
                PostalCode.city_ref == postal_code.city_ref,
                PostalCode.timezone.is_not(None)
            ).first()
            if other_postal_with_tz:
                postal_code.timezone = other_postal_with_tz.timezone
                session.commit()
                return other_postal_with_tz.timezone
            with ChromeWrapper() as driver:
                driver.get(f'https://postal-codes.cybo.com/russia/{self.postal_code_str}')
                redirect_url = driver.current_url
                cached_url = f'https://webcache.googleusercontent.com/search?q=cache%3A{redirect_url}'
                driver.get(cached_url)
                source = driver.page_source
                soup = BeautifulSoup(source, 'html.parser')
                time_zone_td = soup.find_all('td', text='Timezone')
                if time_zone_td:
                    timezone = time_zone_td[0].parent.find_all('td')[-1].text
                else:
                    driver.save_body_screenshot()
                    return None
            postal_code.timezone = timezone
            session.commit()
            return timezone
