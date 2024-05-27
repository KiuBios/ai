import requests
import json
import os

from langchain.tools import BaseTool
from langchain.agents import AgentType
from typing import Optional, Type
from pydantic import BaseModel, Field

cwb_token = os.getenv('CWB_TOKEN', None)

# From CWB API
# https://opendata.cwb.gov.tw/dist/opendata-swagger.html#/%E9%A0%90%E5%A0%B1/get_v1_rest_datastore_F_C0032_001


class WeatherDataInput(BaseModel):
    """Get weather data input parameters."""
    location_name: str = Field(...,
                               description="The cities in Taiwan, it must be one of following 臺北市, 新北市, 臺中市, 臺南市, 雲林縣, 南投縣, 屏東縣, 嘉義市, 嘉義縣")


class WeatherDataTool(BaseTool):
    name = "get_weather_data"
    description = "Get the weather data for Taiwan"

    def _run(self,  location_name: str):
        weather_data_results = get_weather_data(
            location_name)

        return weather_data_results

    def _arun(self, location_name: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = WeatherDataInput


def get_weather_data(location_name=None):
    
    # url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-3999ADC3-3AB0-496D-BAF3-92E431E62341&locationName='
    url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-3999ADC3-3AB0-496D-BAF3-92E431E62341&locationName=%E5%AE%9C%E8%98%AD%E7%B8%A3,%E8%8A%B1%E8%93%AE%E7%B8%A3,%E8%87%BA%E6%9D%B1%E7%B8%A3,%E9%87%91%E9%96%80%E7%B8%A3,%E8%87%BA%E5%8C%97%E5%B8%82,%E6%96%B0%E5%8C%97%E5%B8%82,%E6%A1%83%E5%9C%92%E5%B8%82,%E8%87%BA%E4%B8%AD%E5%B8%82,%E8%87%BA%E5%8D%97%E5%B8%82,%E9%AB%98%E9%9B%84%E5%B8%82,%E5%9F%BA%E9%9A%86%E5%B8%82,%E6%96%B0%E7%AB%B9%E7%B8%A3,%E8%8B%97%E6%A0%97%E7%B8%A3,%E5%BD%B0%E5%8C%96%E7%B8%A3,%E5%8D%97%E6%8A%95%E7%B8%A3,%E5%B1%8F%E6%9D%B1%E7%B8%A3'
    # url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-3999ADC3-3AB0-496D-BAF3-92E431E62341&locationName=%E5%AE%9C%E8%98%AD%E7%B8%A3,%E8%8A%B1%E8%93%AE%E7%B8%A3,%E8%87%BA%E6%9D%B1%E7%B8%A3,%E6%BE%8E%E6%B9%96%E7%B8%A3,%E9%87%91%E9%96%80%E7%B8%A3,%E8%87%BA%E5%8C%97%E5%B8%82,%E6%96%B0%E5%8C%97%E5%B8%82,%E6%A1%83%E5%9C%92%E5%B8%82,%E8%87%BA%E4%B8%AD%E5%B8%82,%E8%87%BA%E5%8D%97%E5%B8%82,%E9%AB%98%E9%9B%84%E5%B8%82,%E5%9F%BA%E9%9A%86%E5%B8%82,%E6%96%B0%E7%AB%B9%E7%B8%A3,%E5%8D%97%E6%8A%95%E7%B8%A3,%E5%B1%8F%E6%9D%B1%E7%B8%A3'
    headers = {'accept': 'application/json'}

    query = {
        'Authorization': cwb_token}

    if location_name is not None:
        query['locationName'] = location_name

    response = requests.get(url, headers=headers, params=query)

    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code