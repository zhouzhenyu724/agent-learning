import asyncio

import httpx


async def fetch_topic(client: httpx.AsyncClient, topic: str) -> dict | None:
    try:
        response = await client.get(f"/topics/{topic}")
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        print(f"查询 {topic} 失败：HTTP {error.response.status_code}")
        return None
    except httpx.ReadTimeout:
        print(f"查询 {topic} 超时")
        return None

    return response.json()


def _mock_handler(request: httpx.Request) -> httpx.Response:
    topic = request.url.path.removeprefix("/topics/")
    if topic == "python":
        return httpx.Response(200, json={"topic": "Python", "hours": 4.0})
    if topic == "backend":
        return httpx.Response(200, json={"topic": "后端", "hours": 2.0})
    if topic == "unknown":
        return httpx.Response(404)
    if topic == "slow":
        raise httpx.ReadTimeout("slow", request=request)
    return httpx.Response(404)


async def main() -> None:
    transport = httpx.MockTransport(_mock_handler)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        python_topic, backend_topic = await asyncio.gather(
          fetch_topic(client, "python"),
          fetch_topic(client, "backend"),
        )
        print(python_topic)
        print(backend_topic)
        await fetch_topic(client, "unknown")
        await fetch_topic(client, "slow")


if __name__ == "__main__":
    asyncio.run(main())
