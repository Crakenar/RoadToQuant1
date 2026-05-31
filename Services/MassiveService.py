from typing import Optional, Iterator

from massive.rest.models import Agg
import yaml
from urllib3 import HTTPResponse

from FirstTimer.Entities import MassiveApi
from massive import RESTClient

DEFAULT_STOCK_ID_TEST = "AAPL"
API_KEY = "Aq3ISE8jsokzF9fhaheXlx4QfwqNBLZe"

def load_yaml_config():
    with open('Config/massive_api.yml', 'r') as f:
        return yaml.full_load(f)

CONFIG = load_yaml_config()
def get_stock_market_data(
        stock_name_id: Optional[str] = DEFAULT_STOCK_ID_TEST) -> Iterator[
                                                                     Agg] | HTTPResponse:
    client = RESTClient(API_KEY)
    print("Getting stock market data...")
    api_config = CONFIG.get('API')

    return client.list_aggs(
        stock_name_id,
        1,
        api_config['DEFAULT_TIMESTAMP'],
        api_config['DEFAULT_FROM_DATE'],
        api_config['DEFAULT_TO_DATE'],
        limit=api_config['DEFAULT_LIMIT'],
    )


def format_stock_market_data(
        stock_market_data: Iterator[Agg] | HTTPResponse,
        stock_name_id: Optional[str] = DEFAULT_STOCK_ID_TEST
) -> list[MassiveApi.AggData]:
    aggs: list[MassiveApi.AggData] = []
    for a in stock_market_data:
        aggs.append({
            'timestamp': a.timestamp,
            'number_of_transactions': a.transactions,
            'volume': a.volume,
            'close': a.close,
            'high': a.high,
            'low': a.low,
            'open': a.open,
            'vwap': a.vwap,
            'stock_id': stock_name_id
        })
    return aggs
