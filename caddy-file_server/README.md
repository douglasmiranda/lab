# Serve static/media files with Caddy

Using [`file_server`](https://caddyserver.com/docs/caddyfile/directives/file_server#file-server).

## Goal

- Access: http://localhost/media/a.txt
- Load: a.txt
  - a.txt is inside ./media-root-local/
  - ./media-root-local/ is gonna be mounted inside Caddy container at /srv/media

## Notes

### Volumes

Replace ./media-root-local/ with any other dir, mounted volume, docker compose volume.

```yaml
services:
  caddy:
    ...
    volumes:
      - media_data:/srv/media
      ...

volumes:
  media_data: {}
  ...
```

### file_server or handle

- https://caddyserver.com/docs/caddyfile/directives/file_server#file-server
- https://caddyserver.com/docs/caddyfile/directives/handle#handle

Either works:

```
route {
	file_server /media/* {
		root /srv
	}
}
```
OR:

```
route {
    handle /media/* {
        root * /srv
        file_server
    }
}
```

### Cache

https://caddyserver.com/docs/caddyfile/directives/header#examples

```
header /media/* Cache-Control max-age=31536000
```
