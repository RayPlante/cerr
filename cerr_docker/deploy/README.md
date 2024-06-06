# Deploy CDCS Docker

## 1. Customize the deployment

Update the .env file with values

``` bash
$ vim .env
```


| Variable | Description |
| ----------- | ----------- |
| PROJECT_NAME          | Name of the CDCS project to deploy (e.g. mdcs, nmrr) |
| PROJECT_VERSION       | Version of the project to deploy (e.g. latest, 2.6.0, 2.7.0) |
| HOSTNAME              | Hostname of the server |
| SERVER_URI            | URI of server |
| SERVER_NAME           | Name of the server |
| MONGO_ADMIN_USER      | Admin user for MongoDB |
| MONGO_ADMIN_PASS      | Admin password for MongoDB |
| MONGO_USER            | User for MongoDB |
| MONGO_PASS            | Password for MongoDB |
| MONGO_DB              | Name of the database (MongoDB) |
| POSTGRES_USER         | User for Postgres |
| POSTGRES_PASS         | Password for Postgres |
| POSTGRES_DB           | Name of the database (Postgres) |
| REDIS_PASS            | Password for Redis |
| DJANGO_SECRET_KEY     | Django Secret Key |
| NGINX_PORT_80         | Expose port 80 on host machine for NGINX |
| NGINX_PORT_443        | Expose port 443 on host machine for NGINX |
| MONGO_PORT            | Expose MongoDB port on host machine |
| MONGO_VERSION         | Version of the MongoDB image |
| REDIS_VERSION         | Version of the Redis image |
| POSTGRES_VERSION      | Version of the Postgres image |
| NGINX_VERSION         | Version of the NGINX image |
| MONITORING_SERVER_URI | (optional) URI of a monitoring server |


## 2. Deploy the stack

``` bash
$ ./docker_setup.sh
```

If using the HTTPS protocol, you can then run the following script to generate and copy self signed certificates to the container.
``` bash
$ ./docker_set_ssl.sh
```

## 3. Create the superuser

The superuser is the first user that will be added to the curator. This is the
main administrator on the platform. Once it has been created, any other user
can be added using the web interface.

```bash
$ ./docker_createsuperuser ${username} ${password} ${email}
```

Running the command without parameters will create a default superuser (admin/admin):

```bash
$ ./docker_createsuperuser
```

## 4. Access

By default, the cdcs is now available at http://127.0.0.1/


## 5. Troubeshoot

## Local deployment

When deploying locally, set `SERVER_URI` to the computer's IP address
and use the same same IP address **when accessing the CDCS via a web browser**:
- On Windows: use the command `ipconfig`
- On MacOS and Unix system: use the command `ifconfig`

**DO NOT** use localhost or 127.0.0.1 or some features may not work (even if the site seems up).

## Production deployment

- Set `SERVER_CONF` to `https`
- Update the file `nginx/https.conf` if necessary
- Mount your own `settings.py` file if necessary

## MongoDB RAM usage


From https://hub.docker.com/_/mongo
> By default Mongo will set the wiredTigerCacheSizeGB to a value
proportional to the host's total memory regardless of memory limits
you may have imposed on the container. In such an instance you will
want to set the cache size to something appropriate, taking into
account any other processes you may be running in the container
which would also utilize memory.

Having multiple mongodb containers on the same machine could be an
issue as each of them will try to use the same amount of RAM
from the host without taking into account the amount used by other
containers. This could lead to the server running out of memory.

### How to fix it?

The amount of RAM used by mongodb can be restricted by adding the
`--wiredTigerCacheSizeGB` option to the mongodb command:

**Example:**
```yml
command: "--auth --wiredTigerCacheSizeGB 8"
```

More information on MongoDB RAM usage can be found in the
[doc](https://docs.mongodb.com/manual/faq/diagnostics/#faq-memory)

