from django.http import JsonResponse
from scraper.utils.scraper import BankBazaarLoanScraper

def run_scraper(request):
    scraper = BankBazaarLoanScraper()
    scraper.scrape_bankbazaar()
    return JsonResponse(scraper.loan_data, safe=False)
