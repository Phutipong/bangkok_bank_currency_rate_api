import odoo
import requests
from odoo import api, fields, models
import datetime


class Currency(models.Model):
    _inherit = 'res.currency'

    def get_usd_rate(self):
        url = 'https://www.bangkokbank.com/api/exchangerateservice/GetChartfxrates/01/10/2024/08/10/2024/USD1/en'
        headers = {
            'accept': '/',
            'accept-language': 'en-US,en;q=0.9,th;q=0.8',
            'cache-control': 'no-cache',
            'cookie': 'A88DE7051AB3182EA14B95F6F7724293~000000000000000000000000000000~YAAQVZ42F1BXNW+SAQAA1KEDcRl8jKbaGiF0HUbAY6YIJFmabpQ7l18zSTZ80FCxhB89BZOdHbhnaD+N2CQkW2SRVwp/zTwmUhuxw9z9Q4ZZl3cskXF3kUEoIgZPpV1ylHDx/CLR+VPhQ+7V+KrV6X1BFGEtMWwjZz8/ceMyqYqyjmAm/+Wux+pPziYI+o8W5JMcFNVFZEVCr9Ap9sO6w7WwqO2GbaX24/iDDtgtpSun59F6ynNBlbLlP4uWjj7hlyz5q1hgC3iGbhynKpzQCL+DnRoi+eVha0VDpqatFAmkcG9xiY4J704R76biNsKxIK1ZmsFEWvWLKitqhF3i/h6a65mBg1Nom2+9I+4r/tzhglWivTsUWjSyMvPsnpsNFfX/a2Tbo8PMAki3BwQzen03eShsz7J/YYA5OINqHQ9SiQ/tDtCXcHGV4wBLx/2/MGFnn3k9Vdilib+IHkThv8I=", "/", ".bangkokbank.com',
            'ocp-apim-subscription-key': '7d1b09abe2ea413cbf95b2d99782ed37',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.bangkokbank.com/en/personal/other-services/view-rates/foreign-exchange-rates',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-arch': '"arm"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.90", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.90"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"macOS"',
            'sec-ch-ua-platform-version': '"15.0.1"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def update_usd_rate(self):
        result = self.get_usd_rate()

        usd = self.env.ref('base.USD') # get_record_by_xml_id

        for r in result:
            key = 'Ddate'
            if key in r:
                # assign date time object to new key of result
                r['DateObj'] = datetime.datetime.strptime(r[key], "%m/%d/%Y").date()

                existed_date = usd.rate_ids.filtered(lambda rate: rate.name == r['DateObj'])

                # incase of BuyingRates is "some string" instead of "33.00"
                try:
                    rate = float(r['BuyingRates'])
                except:
                    print("String Cannot convert To Float")
                    rate = 0
                try:
                    sell_rate = float(r['SellingRates'])
                except:
                    print("String Cannot convert To Float")
                    sell_rate = 0

                if not existed_date:
                    usd.rate_ids.create({
                        'name': r['DateObj'],
                        'currency_id': usd.id,
                        'rate': rate,
                        'sell_rate': sell_rate
                    })


