from django.core.management.base import BaseCommand

from main.bchd import transactions_tracker
from main.helpers import get_BCH_USD_price
from main.models import Funding, Block


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Fetching funding transactions with no transaction block...'))
        funding_txns_with_empty_block = Funding.objects.filter(
            transaction_block__isnull=True
        )
        count = funding_txns_with_empty_block.count()
        track_count = count

        for funding_txn in funding_txns_with_empty_block:
            block = transactions_tracker.get_funding_txn_block(funding_txn.transaction)
            price = get_BCH_USD_price(date=block.timestamp)

            Block.objects.filter(id=block.id).update(
                bch_usd_price=price
            )
            Funding.objects.filter(id=funding_txn.id).update(
                transaction_block=block
            )
            track_count -= 1
            self.stdout.write(self.style.SUCCESS(f'{track_count}  blocks left...'))
        self.stdout.write(self.style.SUCCESS(f'Filled blocks of {count} funding transactions.'))
