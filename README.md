# Getting Started

```
docker build -t junction .
docker run --rm -it --name junction -p 127.0.0.1:5000:5000 junction
```

```
curl -X POST http://127.0.0.1:5000/ -d '{"text": "I love to hack on Junction"}'
```
