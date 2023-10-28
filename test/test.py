import asyncio

from tei import TEIClient

client = TEIClient(port=8080)
client.health()

loop = asyncio.new_event_loop()
client.embed_sync("Hello world!")
routine = client.embed("Hello world!")
asyncio.run(routine)

routine = client.embed_batch(["Hello world!", "Hello world!", "Hello world!"])
asyncio.run(routine)

print(client.info())

print(client.metrics())
