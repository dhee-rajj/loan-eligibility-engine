# scraper/management/commands/scrape_loans.py
from django.core.management.base import BaseCommand
from scraper.utils.scraper import get_loan_data
import json

class Command(BaseCommand):
    help = "Scrape loan data and print to stdout"

    def handle(self, *args, **kwargs):
        data = get_loan_data()
        self.stdout.write(json.dumps(data, indent=2))
