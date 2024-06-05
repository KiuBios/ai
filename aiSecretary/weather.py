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
    # 一般天氣預報-今明36小時天氣預報，臺灣各縣市天氣預報資料及國際都市天氣預報
    url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-3999ADC3-3AB0-496D-BAF3-92E431E62341&locationName=%E9%87%91%E9%96%80%E7%B8%A3,%E8%87%BA%E5%8C%97%E5%B8%82,%E6%96%B0%E5%8C%97%E5%B8%82,%E6%A1%83%E5%9C%92%E5%B8%82,%E8%87%BA%E4%B8%AD%E5%B8%82,%E8%87%BA%E5%8D%97%E5%B8%82,%E9%AB%98%E9%9B%84%E5%B8%82&elementName='
    # 臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來1週天氣預報
    # url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=CWA-3999ADC3-3AB0-496D-BAF3-92E431E62341&locationName=%E9%87%91%E9%96%80%E7%B8%A3,%E8%87%BA%E5%8C%97%E5%B8%82,%E6%96%B0%E5%8C%97%E5%B8%82,%E6%A1%83%E5%9C%92%E5%B8%82,%E8%87%BA%E4%B8%AD%E5%B8%82,%E8%87%BA%E5%8D%97%E5%B8%82,%E9%AB%98%E9%9B%84%E5%B8%82&elementName=PoP12h,T,Wx,WeatherDescription'
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