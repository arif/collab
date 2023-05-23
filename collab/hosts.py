import environ
from django_hosts import host, patterns

env = environ.Env()
hosts = env.dict('DJANGO_HOSTS', default={})

host_patterns = patterns(
    'collab',
    host(hosts.get('admin', 'admin'), 'urls.admin', name='admin'),
    host(hosts.get('api', 'api'), 'urls.api', name='api'),
)
