# Collab

![Build Status](https://github.com/arif/collab/actions/workflows/build.yaml/badge.svg)


## Environment Configuration

> You need to have Docker installed on your machine to run the project

Create and configure the `.env` file. You can simply do the following command:

```sh
cp .env.sample .env
```

Edit the `/etc/hosts` file for `django-hosts`

```
nano /etc/hosts
```

Add the following lines at the end of file

```
127.0.0.1 api-dev.collab
127.0.0.1 admin-dev.collab

# Save and exit with CTRL+C
```

🐼 Starting the project:

```sh
make up
```

### Commands

Run the following command to see available commands in a Makefile.

```sh
make help
```
