from flask import request, url_for, redirect
from urllib.parse import urlparse, urljoin
from datetime import datetime

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get('next'), request.args.get('next'):
        if not target:
            continue
        if is_safe_url(target):
            return target

def redirect_back(endpoint, **values):
    target = request.form['next'] if request.form and 'next' in request.form else request.args.get('next')
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


def logInf():
    return {
        'timestamp_utc': datetime.utcnow().timestamp(),
        'ip': request.remote_addr,
        'os': request.user_agent.platform,
        'browser': request.user_agent.browser,
        'v': request.user_agent.version,
        'lang': request.user_agent.language,
        'st': request.user_agent.string
    }