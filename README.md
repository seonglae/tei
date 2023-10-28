# TEI Python

Text Embeddings Inference (TEI)'s unofficial python wrapper library for batch processing with asyncio.

# Get Started

```sh
pip install teicli
```

```py
from tei import TEIClient

client = TEIClient()
client.embed_sync("Hello world!")
# [0.010536194, 0.05859375, 0.022262....

routine = client.embed_batch(["Hello world!", "Hello world!", "Hello world!"])
# [[0.010536194, 0.05859375, 0.022262....
```

You need to run own text-embeddings-inference server. Check [here](https://github.com/huggingface/text-embeddings-inference)

```sh
docker run --gpus all -p 8080:80 -v $volume:/data --pull always ghcr.io/huggingface/text-embeddings-inference:0.3.0 --model-id $model --revision
 $revision
```
