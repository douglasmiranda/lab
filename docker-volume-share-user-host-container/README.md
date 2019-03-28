# Docker bind volume shared between host and container

If you search you'll find that volumes and permissions issues are very common. (not only in Docker)

This is an example of how to kinda overcome a problem that happens a lot when you want to share 
your project code inside your host machine with your container where it is running in fact.

(You can search for "docker volumes uid" and see everyone talking about solutions)

- https://docs.docker.com/storage/volumes/
- https://docs.docker.com/storage/bind-mounts/
- https://docs.docker.com/compose/compose-file/#volumes
- https://docs.docker.com/engine/reference/builder/#volume
- https://github.com/moby/moby/issues/2259


The default first user UID for some common Operating Systems:

Ubuntu/Debian: 1001
MacOS: 501

But you can get the UID for your current user with:

```
id -u $USER
```

My user is "douglas", so in my terminal: id -u douglas
Will give me: 1001


For automating, you want to use something more like:
```bash
$(id -u $USER)
# OR
$(id -u $(whoami))
```

It will give you the id for your current user logged on to the terminal.

Try yourself:

```bash
docker build -t docker-volume-share-example --build-arg UID=1001 .

docker run --rm -it -v "$PWD/code:/myapp/code" docker-volume-share-example sh
```

OR

```
docker-compose build

docker-compose up
```

Look for `UID` in the Dockerfile for the default value.

In docker-compose.yml you'll see how to set build args, for more consult the documentation:

- https://docs.docker.com/compose/compose-file/#args
- https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
- https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg

---

## What about the production environment

In production, you'll probably build your image (hopefully in your CI/CD) adding the code to the image with the `COPY` command 
on the Dockerfile. After that you can fix permissions, ownership, everything you need freely, because your container is your domain
now, no nonsense of volume sharing, at least for your code.

- https://docs.docker.com/engine/reference/builder/#copy

When you need to use volumes, let's say your Database, uploaded files, things like that, you probably be using named volumes, Docker manages
them, so it's a breeze to use. (most of the time)

- https://docs.docker.com/compose/compose-file/#volumes

In a multi-host/distributed environment, you will have bigger problems than permissions and ownership. So let's stop here.
