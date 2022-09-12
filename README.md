# CE-Registry

The CDCS Circular Economy Registry customization code repository

# Circular Economy Resource Registry (CERR)

This repository contains the files necessary to build and do a test deployment
of the NIST Circular Economy Resource Registry (CERR). It is built and deployed much
like other CDCS-based applications. There are two primary steps to get started:

1. Build the CERR image
1. Deploy the CERR application stack using `docker-compose`

Please see below for further details on these two steps.

## Building the CERR image

The files related to building and deploying CERR are located in the
`/cerr_docker` folder, and are structured in the same way as the
`cdcs-docker` [repository](https://github.com/usnistgov/cdcs-docker), which
was used as inspiration for how to build this project.

You will have to have Docker and `docker-compose` installed, so make sure those
are working on your system before getting started.

To build the CERR image (which will be named `cerr`), navigate to the
`/cerr_docker/build` folder and run:

```bash
docker-compose build
```

This may take a while the first time it runs, but you shouldn't have to make
any changes to the local settings (the `.env` file) for this stage of the
process. That command should eventually end with an output something like the
following:

```text
Successfully built 53104b86f2d8
Successfully tagged cerr:2.16.0-4
```

You can confirm that the Docker image built and is available on your machine
by looking at the images that docker knows about with the `image list` command
and confirming that `cerr` is present in the list:

```bash
$ docker image list
REPOSITORY    TAG        IMAGE ID       CREATED              SIZE
cerr         2.16.0-4   53104b86f2d8   About a minute ago   1.27GB
```

## Deploying the CERR application

Once you have the CERR image built from the previous section, move to the
`./cerr_docker/deploy` directory to deploy the actual application:

```bash
cd ../deploy     # if you're in the ./cerr_docker/deploy folder, this should work
```

For a simple local test deployment, you'll need to make a few changes to the
`.env` file in this directory before trying to bring up the application stack.
Consult the `README.md` file in the `deploy/` folder for more details, but at
the very least, you'll need to change the following three lines:

```bash
HOSTNAME=192.168.1.5
SERVER_URI=http://192.168.1.5
ALLOWED_HOSTS=*
```

Changing `HOSTNAME` and `SERVER_URI` to your local IP address is required to
make things work locally. Make sure not to use `localhost`, or your Docker
interface's IP address, but rather the one that is assigned to your host
machine by your router or network admin. Also change `ALLOWED_HOSTS` to `*`
to make sure you can access the test deployment from any connected IP.
Alternatively, you could restrict this value to a comma-separated list of hosts
that you want to be able to access the application, but sometimes this causes
unexpected issues, so `*` is easier (although slightly less secure, since
anyone on your network will be able to connect to the application while you're
developing it).

It's also recommended (even for development) to change any of the password
values in `./cerr_docker/deploy/.env` that have a value of `changeme` to some
random values, since these values will be used to secure the underlying
services running in Docker containers. It's not critical for development, but
_definitely_ change these if you're running any sort of production instance.

If you've made changes to the version of the docker image in the
`./cerr_docker/build/.env` file, you should change the `IMAGE_VERSION`
variable as well to match, or you might use an older image version, and you'll
wonder why none of your changes are visible. Alternatively, you could try
setting both to something like `latest` if you're making many rapid changes
and don't want to tag a new image version each time.

Once you have these changes made, save the `.env` file and run:

```bash
docker-compose up -d
docker exec -u root nmrr_cdcs chmod -R o+w /usr/local/lib/python3.7/site-packages/cerr_curate_app/
docker-compose restart
docker exec -u root nmrr_cdcs chmod -R o-w /usr/local/lib/python3.7/site-packages/cerr_curate_app/
```

This command will pull any docker images needed and bring them up according
to the specification in the `docker-compose.yml` file. 
It is needed here to update the permissions of cerr_curate_app to apply the migrations to the database (when restarting the container).
The permissions are then set back to normal.
Once they are all up, you _should_ be able to access the application by visiting your local IP in
your browser, at something like http://192.168.1.5 (or whatever your IP
address is).
If the application appears to be up, you'll need to create an
admin user to do anything useful, using the
`./cerr_docker/deploy/docker_createsuperuser.sh` script, which can be run from
the terminal by providing a username (`admin` in the example here`) and a
password:

```bash
./docker_createsuperuser.sh admin "<whatever_password_you_choose>"
```

You should also run the `docker_update_xslt.sh` script, which will
automatically associate the XSLT files in the `./cerr_docker/build/cdcs/cerr`
folder with the schema, so any records that are entered will be displayed with
the customized XSLT files defined in that folder (you also have to provide
an administrator username and password, so use whatever you defined in the
last step):

```bash
./docker_update_xslt.sh admin "<whatever_password_you_chose>"
```

That should get you fully up and running. If something went wrong, check that
the various services are running by running the following from the
`./cerr_docker/deploy/` folder:

```bash
$ docker-compose ps
       Name                     Command               State                    Ports
------------------------------------------------------------------------------------------------------
nmrr_cdcs            /docker-entrypoint.sh nmrr       Up
nmrr_cdcs_mongo      docker-entrypoint.sh --auth      Up      27017/tcp
nmrr_cdcs_nginx      /docker-entrypoint.sh ngin ...   Up      0.0.0.0:443->443/tcp, 0.0.0.0:80->80/tcp
nmrr_cdcs_postgres   docker-entrypoint.sh postgres    Up      5432/tcp
nmrr_cdcs_redis      docker-entrypoint.sh redis ...   Up      6379/tcp
```

If something's not working right, you can view the logs of all the services
by running `docker-compose logs` from the same folder. Alternatively, you can
add the name of a service as specified in the `docker-compose.yml` file
(e.g. `docker-compose logs cerr`) to look at the logs from a single container.
Finally, you can add the `--follow` argument and the log file will stay open
in your terminal and you can watch the output as it comes in.

Good luck!

## Actual deployment strategy

Adam Morey and Bob Bagwill are in charge of the server running the test
deployment (`newton.nist.gov`) -- contact them for access if you need.
The production deployment server has not been identified yet, but the process
should be relatively similar in that case, too.
The deployment files are in `/data/workspace/cdcsstage/deploy/cerr/` and
are roughly analagous to what is in the the `./cerr_docker/deploy` folder of
this repository, with some changes to account for the more "production-ready"
deployment.

In general, the process is to build an image of `cerr` from this repository,
tag it properly, push it to Docker Hub, and then use that image to deploy
the application on the remote server (`newton` and wherever the public
deployment ends up running). Building the image can be done from anywhere
(most likely your local machine), and you'll have to be part of the
[`nistodi`](https://hub.docker.com/orgs/nistodi) organization on Docker Hub
to push the image (contact Adam Morey if needed). In general the process looks
like the following:

```bash
# build the cerr image like described before...
$ docker-compose build
Successfully built 53104b86f2d8
Successfully tagged cerr:2.16.0-4

# add a tag to the image that will put it in the right place on Docker Hub:
# make sure to change the version number (after the ":" character) to match
# whatever has been built by the last command
# note: the prefix must be "nistodi/cdcs..." since that's expected by the
# deployment configuration
$ docker tag cerr:2.16.0-4 nistodi/cdcs_ce:2.16.0-4

# push the newly tagged image up to docker hub:
# (you may have to run `docker login` first)
$ docker push nistodi/cdcs_ce:2.16.0-4
```

The image is now ready to be used on Docker Hub for deployment.
