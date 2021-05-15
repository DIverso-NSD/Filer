# Filler

Сервис загрузки файлов по HTTP

# Example

```python
import requests
import os

headers = {
    "Token": "xxx"
}

file = "NVR.zip"
file_size = os.stat(file).st_size

res = requests.post(
    "http://localhost:5500/files",
    json={"file_name": file, "file_size": file_size},
    headers=headers,
)

file_id = res.json()["file_id"]

last_byte = 0
with open(file, "rb") as f:
    chunk = f.read(5 * 1024 * 1024)  # 5 MB

    while len(chunk) > 0:
        last_byte += len(chunk)
        resp = requests.put(
            f"http://localhost:5500/files/{file_id}",
            headers=headers,
            files={"file_data": chunk},
            params={"last_byte": last_byte},
        )
        print(resp.json())
        chunk = f.read(5 * 1024 * 1024)

```
