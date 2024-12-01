from django.test import TestCase
from stocks.services import KoreaInvestAPI

class KoreaInvestAPITestCase(TestCase):
    def test_place_cash_order(self):
        api = KoreaInvestAPI()
        response = api.place_cash_order(
            pdno="005930",          # 삼성전자
            ord_dvsn="00",          # 00:지정가, 01:시장가
            ord_qty=1,              # 주문수량
            ord_unpr=60000,         # 주문단가
            order_type="BUY",       # BUY:매수, SELL:매도
        )
        self.assertIn("error", response)
        self.assertNotEqual(response.get("error"), "Failed to authenticate")
