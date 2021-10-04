import asyncio

import aiohttp

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

# ad2c251a297beb27f2ccec8690055287


weather_router = APIRouter()


async def requests(session, city):
    async with session.get(
            f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=c4cbd5a2c52a90888cf3be7c25c65b79&units=metric&lang=eng&cnt=1') as response:
        return await response.json()


async def get_weather(city):
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(requests(session, city))
        return result


@weather_router.get('/weather/{city}/')
async def get_city(city: str):
    try:
        response = await get_weather(city=city)

        instance = {
            "City": city,
            "Temperature": response[0].get('list')[0].get('main').get('temp'),
            "Feel like": response[0].get('list')[0].get('main').get('feels_like'),
            "Wind speed": response[0].get('list')[0].get('wind').get('speed'),
            "Description": response[0].get('list')[0].get('weather')[0].get('description'),
        }
        return JSONResponse(content=instance, status_code=200)
    except:
        raise HTTPException(status_code=404, detail="City is not found")
