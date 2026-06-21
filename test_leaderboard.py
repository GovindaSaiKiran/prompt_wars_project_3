import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        res = await client.get("http://localhost:8000/api/v1/leaderboard/")
        print("Status Code:", res.status_code)
        print("Response:", res.json())

if __name__ == "__main__":
    asyncio.run(main())
