import os
import pandas as pd
import requests
import time
import zipfile

from django.conf import settings
from django.core.cache import cache
from stocks.constants import MarketType


class KoreaInvestAPI:
    def __init__(self):
        if settings.USE_SIMULATED_API:
            self.app_key = settings.SIM_APP_KEY
            self.app_secret = settings.SIM_APP_SECRET
            self.api_domain = settings.SIM_API_DOMAIN
        else:
            self.app_key = settings.LIVE_APP_KEY
            self.app_secret = settings.LIVE_APP_SECRET
            self.api_domain = settings.LIVE_API_DOMAIN

        self.token_cache_key = 'korea_invest_api_token'
        self.token_expiry_time = 1430 * 60  # 1430분(23시간 50분) * 60초

    def get_headers(self):
        return {
            'Content-Type': 'application/json; charset=UTF-8'
        }

    def get_token(self):
        token = cache.get(self.token_cache_key)
        if token:
            return token

        response = self.request_token_from_api()

        if 'access_token' in response:
            token = response['access_token']
            cache.set(self.token_cache_key, token, timeout=self.token_expiry_time)
            return token
        else:
            return None

    def request_token_from_api(self):
        url = f"{self.api_domain}/oauth2/tokenP"
        headers = self.get_headers()
        body = {
            'grant_type': 'client_credentials',
            'appkey': self.app_key,
            'appsecret': self.app_secret
        }

        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve access token.: {response.json()}")
            return {"error": f"Failed to get token, status code: {response.status_code}"}

    def download_and_extract_stock_data(self, base_dir, market=MarketType.KOSPI, verbose=False):    
        """
        종목 코드 파일 다운로드 (코스피, 코스닥)
        """
        print(market)
        if verbose:
            print(f"Current directory is {base_dir}")

        url_mapping = {
            MarketType.KOSPI: "https://new.real.download.dws.co.kr/common/master/kospi_code.mst.zip",
            MarketType.KOSDAQ: "https://new.real.download.dws.co.kr/common/master/kosdaq_code.mst.zip"
        }

        if market not in url_mapping:
            raise ValueError(f"Unsupported market type: {market}")

        url = url_mapping[market]
        zip_path = os.path.join(base_dir, f"{market}_code.zip")

        # 파일 다운로드
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # 파일 저장
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # 압축 해제
        with zipfile.ZipFile(zip_path, 'r') as kospi_zip:
            kospi_zip.extractall(base_dir)

        os.remove(zip_path)

    def get_stock_data_dataframe(self, base_dir, market=MarketType.KOSPI):
        """
        종목코드 파일 정제(코스피, 코스닥)
        """
        file_name = os.path.join(base_dir, f"{market.value.lower()}_code.mst")
        tmp_fil1 = os.path.join(base_dir, f"{market.value.lower()}_code_part1.tmp")
        tmp_fil2 = os.path.join(base_dir, f"{market.value.lower()}_code_part2.tmp")

        if market == MarketType.KOSPI:
            end_offset = 228
            part1_columns = ['단축코드', '표준코드', '한글명']
            field_specs = [2, 1, 4, 4, 4,
                        1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1,
                        1, 9, 5, 5, 1,
                        1, 1, 2, 1, 1,
                        1, 2, 2, 2, 3,
                        1, 3, 12, 12, 8,
                        15, 21, 2, 7, 1,
                        1, 1, 1, 1, 9,
                        9, 9, 5, 9, 8,
                        9, 3, 1, 1, 1
                        ]
            part2_columns = ['그룹코드', '시가총액규모', '지수업종대분류', '지수업종중분류', '지수업종소분류',
                            '제조업', '저유동성', '지배구조지수종목', 'KOSPI200섹터업종', 'KOSPI100',
                            'KOSPI50', 'KRX', 'ETP', 'ELW발행', 'KRX100',
                            'KRX자동차', 'KRX반도체', 'KRX바이오', 'KRX은행', 'SPAC',
                            'KRX에너지화학', 'KRX철강', '단기과열', 'KRX미디어통신', 'KRX건설',
                            'Non1', 'KRX증권', 'KRX선박', 'KRX섹터_보험', 'KRX섹터_운송',
                            'SRI', '기준가', '매매수량단위', '시간외수량단위', '거래정지',
                            '정리매매', '관리종목', '시장경고', '경고예고', '불성실공시',
                            '우회상장', '락구분', '액면변경', '증자구분', '증거금비율',
                            '신용가능', '신용기간', '전일거래량', '액면가', '상장일자',
                            '상장주수', '자본금', '결산월', '공모가', '우선주',
                            '공매도과열', '이상급등', 'KRX300', 'KOSPI', '매출액',
                            '영업이익', '경상이익', '당기순이익', 'ROE', '기준년월',
                            '시가총액', '그룹사코드', '회사신용한도초과', '담보대출가능', '대주가능'
                            ]
        elif market == MarketType.KOSDAQ:
            end_offset = 222
            part1_columns = ['단축코드','표준코드','한글종목명']
            field_specs = [2, 1,
                        4, 4, 4, 1, 1,
                        1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1,
                        1, 1, 1, 1, 9,
                        5, 5, 1, 1, 1,
                        2, 1, 1, 1, 2,
                        2, 2, 3, 1, 3,
                        12, 12, 8, 15, 21,
                        2, 7, 1, 1, 1,
                        1, 9, 9, 9, 5,
                        9, 8, 9, 3, 1,
                        1, 1
                        ]
            part2_columns = ['증권그룹구분코드','시가총액 규모 구분 코드 유가',
                            '지수업종 대분류 코드','지수 업종 중분류 코드','지수업종 소분류 코드','벤처기업 여부 (Y/N)',
                            '저유동성종목 여부','KRX 종목 여부','ETP 상품구분코드','KRX100 종목 여부 (Y/N)',
                            'KRX 자동차 여부','KRX 반도체 여부','KRX 바이오 여부','KRX 은행 여부','기업인수목적회사여부',
                            'KRX 에너지 화학 여부','KRX 철강 여부','단기과열종목구분코드','KRX 미디어 통신 여부',
                            'KRX 건설 여부','(코스닥)투자주의환기종목여부','KRX 증권 구분','KRX 선박 구분',
                            'KRX섹터지수 보험여부','KRX섹터지수 운송여부','KOSDAQ150지수여부 (Y,N)','주식 기준가',
                            '정규 시장 매매 수량 단위','시간외 시장 매매 수량 단위','거래정지 여부','정리매매 여부',
                            '관리 종목 여부','시장 경고 구분 코드','시장 경고위험 예고 여부','불성실 공시 여부',
                            '우회 상장 여부','락구분 코드','액면가 변경 구분 코드','증자 구분 코드','증거금 비율',
                            '신용주문 가능 여부','신용기간','전일 거래량','주식 액면가','주식 상장 일자','상장 주수(천)',
                            '자본금','결산 월','공모 가격','우선주 구분 코드','공매도과열종목여부','이상급등종목여부',
                            'KRX300 종목 여부 (Y/N)','매출액','영업이익','경상이익','단기순이익','ROE(자기자본이익률)',
                            '기준년월','전일기준 시가총액 (억)','그룹사 코드','회사신용한도초과여부','담보대출가능여부','대주가능여부'
                            ]

        with open(file_name, mode="r", encoding="cp949") as f, open(tmp_fil1, mode="w", encoding="utf-8") as wf1, open(tmp_fil2, mode="w", encoding="utf-8") as wf2:
            for row in f:
                rf1 = row[0:len(row) - end_offset]
                rf1_1 = rf1[0:9].rstrip()
                rf1_2 = rf1[9:21].rstrip()
                rf1_3 = rf1[21:].strip()
                wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + '\n')
                rf2 = row[-end_offset:]
                wf2.write(rf2)

        df1 = pd.read_csv(tmp_fil1, header=None, names=part1_columns, encoding='utf-8')
        df2 = pd.read_fwf(tmp_fil2, widths=field_specs, names=part2_columns, encoding='utf-8')
        df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)

        os.remove(tmp_fil1)
        os.remove(tmp_fil2)
        
        print("Data processing completed.")
        return df

    def fetch_daily_stock_data(self, ticker, start_date, end_date, period_code, adj_price_flag=0):
        """
        날짜에 대한 주식 금액 데이터 가져오기
        """
        authorization  = self.get_token()
        if not authorization:
            return {"error": "Failed to authenticate"}

        url = f"{self.api_domain}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {authorization}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": "FHKST03010100",       # 실전투자/모의투자
            "custtype": "P"                 # 개인:P, 법인:B
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",          # J: 주식,ETF,ETN
            "FID_INPUT_ISCD": ticker,               # 종목번호 (6자리)
            "FID_INPUT_DATE_1": start_date,         # 조회 시작일자 (ex. 20220501)
            "FID_INPUT_DATE_2": end_date,           # 조회 종료일자 (ex. 20220530)
            "FID_PERIOD_DIV_CODE": period_code,     # 기간 분류 코드 (D: 일봉, W: 주봉, M: 월봉, Y: 년봉)
            "FID_ORG_ADJ_PRC": adj_price_flag,      # 수정주가 여부 (0: 수정주가, 1: 원주가)
        }
        time.sleep(0.5)
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            # print(f"Failed to fetch stock data: {response.json()}")
            return {"error": f"Failed to fetch data, status code: {response.status_code}"}
