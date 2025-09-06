# Readme
Run with:
```bash
uvicorn main:app --reload
```

Create a data.json to store members:
```json
{
  "clubs": {
    "amFOSS": {
      "name": "amFOSS",
      "members": [
        { "id": "AM.EN.U4AIE22069", "name": "Bob" },
        { "id": "AM.EN.U4AIE22050", "name": "Charlie" }
      ]
    },
    "Bi0s": {
      "name": "Bi0s",
      "members": [
        { "id": "AM.EN.U4AIE22006", "name": "Eve" },
        { "id": "AM.EN.U4AIE22007", "name": "Frank" }
      ]
    }
  }
}
```
## Running with Docker Compose

Create a .env file with your Cloudflare tunnel token:
```.env
CLOUDFLARE_TUNNEL_TOKEN=xxx
```

Start the containers:
```bash
docker compose up
```
