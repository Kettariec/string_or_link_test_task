import aiohttp
import asyncio


async def is_url(string):
    return string.startswith("http://") or string.startswith("https://")


async def check_methods(url):
    methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]
    result = {}
    async with aiohttp.ClientSession() as session:
        for method in methods:
            try:
                async with session.request(method, url, timeout=5) as response:
                    result[method] = response.status
            except aiohttp.ClientError:
                pass
    return result


async def main():
    n = int(input("Введите количество строк: "))
    strings = [input(f"Строка {i + 1}: ") for i in range(n)]

    result = {}
    for string in strings:
        if not await is_url(string):
            print(f'Строка "{string}" не является ссылкой.')
            continue

        print(f'Проверяется ссылка: {string}')
        methods = await check_methods(string)
        if methods:
            result[string] = methods

    print("\nРезультат работы программы:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
