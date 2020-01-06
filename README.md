# Couchbase Python Playground

## Prerequisites

Docker Compose configuration will:
* Use the official Couchbase image: https://hub.docker.com/_/couchbase/
* Store the database and data set in a local dir: ./couch

Couchbase Python bindings can be installed:
```bash
$> brew install libcouchbase
$> pip install couchbase
```

(or use pipenv with local Pipfile):
```bash
$> brew install libcouchbase
$> pipenv install
```

## Couchbase Startup

### 1. Boot Container
You can boot the docker image in a local container yourself, forwarding
the administrative port to take a look:

```bash
> docker run -d -p 8091:8091 couchbase
Unable to find image 'couchbase:latest' locally
latest: Pulling from library/couchbase
e80174c8b43b: Pull complete
d1072db285cc: Pull complete
858453671e67: Pull complete
3d07b1124f98: Pull complete
a6617e5d0deb: Pull complete
2b44f72ba1b2: Pull complete
2c14b6328f18: Pull complete
5715e0078c42: Pull complete
4e5bcf56f863: Pull complete
487f7cbee64b: Pull complete
21bbdc4493ed: Pull complete
b015ab4db859: Pull complete
c145cb8ade88: Pull complete
Digest: sha256:9a49fee7ff14a48c0e2913b6a93d403f057cb8bace973351c3b5918c775a30f0
Status: Downloaded newer image for couchbase:latest
2f0a53784c77d578402e0747490c546fd5dd0623dadf68d388fb09a57dbf7c0c

> docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                                                                NAMES
2f0a53784c77        couchbase           "/entrypoint.sh couc…"   32 seconds ago      Up 30 seconds       8092-8096/tcp, 11207/tcp, 11210-11211/tcp, 0.0.0.0:8091->8091/tcp, 18091-18096/tcp   confident_hamilton
```

You may instead want to leverage the Docker Compose configuration to open all standard node communicative ports and mount a volume to persist your data between sessions. docker-compose.yml example:

```yaml
version: "3"
services:
  db1:
    image: couchbase
    ports:
      - 8091-8094:8091-8094
      - 11210:11210
    volumes:
      - ./couch:/opt/couchbase/var
```

With this in place, you can startup your cluster with a simple:

```bash
$> docker-compose up
```

... and bring it down by terminating the process. If you use `-d` option to `up` command, you can terminate the cluster with:

```bash
$> docker-compose down
```

### 2. Admin UI

Once Couchbase is up and running within Docker, open http://localhost:8091 in browser to access Couchbase administrative panel.

Select `Setup New Cluster` and give the new cluster a name.

First time, you will have to create and Administrator user. Recommend a simple credential here for local development:
* username: Administrator
* password: password

Creating the default couchbase setup is recommended, but will require your docker to have more memory. This can be done by going into your docker settings under `Advanced` and upping memory from 2GB to at least 3GB, 4+ is recommended.

Your system should reveal itself as a **Cluster** with a single **Node**, likely at a Docker-internal IP address (e.g., 172.*).

In order for authentication by most application libraries to work, your cluster should offer a `default` bucket:

1. Navigate to "Buckets" admin screen
1. Add a new bucket with default settings named "default"
1. Ready!

### 3. App-Specific Bucket

You will want to create a bucket per-application. From the "Buckets" navigation add a new bucket, named as needed.

You will want to configure a user for access of this bucket from your applications. Couchbase provides an "Application" security level, which allows you to simply create a user that will have privilege to manipulate data within a bucket, but do nothing administratively. This is done using RBAC Role Base Access Control.

Create a user, assign them "Application" rights to your bucket and remember their credentials for use in your connections.


### 4. Connection Issues

If you have connection issues, try using the `sdk-doctor` tool to diagnose connectivity problems to your cluster.

Details: https://github.com/couchbaselabs/sdk-doctor 

