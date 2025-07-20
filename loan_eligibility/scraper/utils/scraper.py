#!/usr/bin/env python3
"""
BankBazaar Personal Loan Scraper using requests + rule-based eligibility
Can be used as a script or imported as a module.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BankBazaarLoanScraper:
    def __init__(self):
        self.loan_data = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0'
        })

    def parse_interest_rate(self, rate_text):
        if not rate_text:
            return None, None
        rates = re.findall(r'(\d+(?:\.\d+)?)%', str(rate_text))
        if not rates:
            return None, None
        elif len(rates) == 1:
            return float(rates[0]), float(rates[0])
        else:
            return float(rates[0]), float(rates[1])

    def estimate_eligibility(self, min_rate):
        if min_rate is None:
            return {'min_income_monthly': 25000, 'credit_score': 700}
        if min_rate < 11:
            return {'min_income_monthly': 40000, 'credit_score': 750}
        elif min_rate < 14:
            return {'min_income_monthly': 30000, 'credit_score': 700}
        else:
            return {'min_income_monthly': 20000, 'credit_score': 650}

    def scrape_bankbazaar(self):
        url = "https://www.bankbazaar.com/personal-loan-interest-rate.html"
        logger.info(f"Scraping {url}...")
        response = self.session.get(url, timeout=15)
        if response.status_code != 200:
            logger.error("Failed to fetch data from BankBazaar")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        if not table:
            logger.warning("No table found on the page")
            return []

        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                bank_name = cols[0].get_text(strip=True)
                rate_text = cols[1].get_text(strip=True)
                min_rate, _ = self.parse_interest_rate(rate_text)
                eligibility = self.estimate_eligibility(min_rate)

                self.loan_data.append({
                    'source': 'BankBazaar',
                    'bank_name': bank_name,
                    'product_name': f"{bank_name} Personal Loan",
                    'min_credit_score': eligibility['credit_score'],
                    'min_income_monthly': eligibility['min_income_monthly'],
                    'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                })

        return self.loan_data


def get_loan_data():
    scraper = BankBazaarLoanScraper()
    return scraper.scrape_bankbazaar()


if __name__ == "__main__":
    data = get_loan_data()
    print(json.dumps(data, indent=2, ensure_ascii=False))
