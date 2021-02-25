from flask import request
from urllib.parse import urlparse, urljoin


# from https://security.openstack.org/guidelines/dg_avoid-unvalidated-redirects.html
def is_safe_redirect_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return (
        redirect_url.scheme in ("http", "https")
        and host_url.netloc == redirect_url.netloc
    )


def get_safe_redirect(url):

    if url and is_safe_redirect_url(url):
        return url

    url = request.referrer
    if url and is_safe_redirect_url(url):
        return url

    return "/"
