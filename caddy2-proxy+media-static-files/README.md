# Caddy serving static files + reverse_proxy

```
docker-compose up
```

- Direct flask access: http://localhost:8000
- Caddy pointing to flask (reverse_proxy): http://localhost/
- Static file access through Caddy: http://localhost/media/dog.jpg
