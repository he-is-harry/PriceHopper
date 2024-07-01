# Code is modified from https://github.com/MarioVilas/googlesearch/blob/master/googlesearch/__init__.py
# Do not use for commercial use

import os
import random
import sys
import time
import ssl

from http.cookiejar import LWPCookieJar
import requests
from urllib.parse import quote_plus, urlparse, parse_qs

try:
    from bs4 import BeautifulSoup
    is_bs4 = True
except ImportError:
    from BeautifulSoup import BeautifulSoup
    is_bs4 = False

__all__ = [

    # Main search function.
    'search',

    # Shortcut for "get lucky" search.
    'lucky',

    # Miscellaneous utility functions.
    'get_random_user_agent', 'get_tbs',
]

# URL templates to make Google searches.
url_home = "https://www.google.%(tld)s/"
url_search = "https://www.google.%(tld)s/search?lr=lang_%(lang)s&" \
             "q=%(query)s&btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&" \
             "cr=%(country)s&filter=0"
url_next_page = "https://www.google.%(tld)s/search?lr=lang_%(lang)s&" \
                "q=%(query)s&start=%(start)d&tbs=%(tbs)s&safe=%(safe)s&" \
                "cr=%(country)s&filter=0"
url_search_num = "https://www.google.%(tld)s/search?lr=lang_%(lang)s&" \
                 "q=%(query)s&num=%(num)d&btnG=Google+Search&tbs=%(tbs)s&" \
                 "&safe=%(safe)scr=%(country)s&filter=0"
url_next_page_num = "https://www.google.%(tld)s/search?lr=lang_%(lang)s&" \
                    "q=%(query)s&num=%(num)d&start=%(start)d&tbs=%(tbs)s&" \
                    "safe=%(safe)s&cr=%(country)s&filter=0"
url_parameters = (
    'hl', 'q', 'num', 'btnG', 'start', 'tbs', 'safe', 'cr', 'filter')

# Cookie jar. Stored at the user's home folder.
# If the cookie jar is inaccessible, the errors are ignored.
home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'   # Use the current folder on error.
cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass

# Default user agent, unless instructed by the user to change it.
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'

# Load the list of valid user agents from the install folder.
# The search order is:
#   * user_agents.txt.gz
#   * user_agents.txt
#   * default user agent
try:
    install_folder = os.path.abspath(os.path.split(__file__)[0])
    try:
        user_agents_file = os.path.join(install_folder, 'user_agents.txt.gz')
        import gzip
        fp = gzip.open(user_agents_file, 'rb')
        try:
            user_agents_list = [_.strip() for _ in fp.readlines()]
        finally:
            fp.close()
            del fp
    except Exception:
        user_agents_file = os.path.join(install_folder, 'user_agents.txt')
        with open(user_agents_file) as fp:
            user_agents_list = [_.strip() for _ in fp.readlines()]
except Exception:
    user_agents_list = [USER_AGENT]


# Get a random user agent.
def get_random_user_agent():
    """
    Get a random user agent string.

    :rtype: str
    :return: Random user agent string.
    """
    return random.choice(user_agents_list)


# Helper function to format the tbs parameter.
def get_tbs(from_date, to_date):
    """
    Helper function to format the tbs parameter.

    :param datetime.date from_date: Python date object.
    :param datetime.date to_date: Python date object.

    :rtype: str
    :return: Dates encoded in tbs format.
    """
    from_date = from_date.strftime('%m/%d/%Y')
    to_date = to_date.strftime('%m/%d/%Y')
    return 'cdr:1,cd_min:%(from_date)s,cd_max:%(to_date)s' % vars()


# Request the given URL and return the response page, using the cookie jar.
# If the cookie jar is inaccessible, the errors are ignored.
# Harry's Note: Code was changes to use the requests library to allow for the use
# of proxies
def get_page(url, proxy = None, user_agent=None, verify_ssl=True):
    """
    Request the given URL and return the response page, using the cookie jar.

    :param str url: URL to retrieve.
    :param str user_agent: User agent for the HTTP requests.
        Use None for the default.
    :param bool verify_ssl: Verify the SSL certificate to prevent
        traffic interception attacks. Defaults to True.

    :rtype: str
    :return: Web page retrieved for the given URL.

    :raises IOError: An exception is raised on error.
    :raises urllib2.URLError: An exception is raised on error.
    :raises urllib2.HTTPError: An exception is raised on error.
    """
    if user_agent is None:
        user_agent = USER_AGENT
    headers = {
        "User-Agent": user_agent,
    }
    s = requests.Session()
    if proxy:
        s.proxies = {}
        s.proxies["http"] = proxy
        s.proxies["https"] = proxy
    s.cookies = cookie_jar

    response = s.get(url, headers=headers, verify=verify_ssl)
    html = response.text
    response.close()
    try:
        cookie_jar.save()
    except Exception:
        pass
    return html

# Filter links found in the Google result pages HTML code.
# Returns None if the link doesn't yield a valid result.
def filter_result(link, include_google_links=False):
    try:
        # Decode hidden URLs.
        if link.startswith('/url?'):
            o = urlparse(link, 'http')
            link = parse_qs(o.query).get('q')[0]

        o = urlparse(link, 'http')

        # Check if the link is an absolute URL.
        if not o.netloc:
            return None

        # If excluding Google links, return None if 'google' is in the domain.
        if not include_google_links and 'google' in o.netloc:
            return None

        return link

    except Exception:
        pass


# Returns a generator that yields URLs.
def search(query, tld='com', lang='en', tbs='0', safe='off', num=10, start=0,
           stop=None, pause=2.0, country='', extra_params=None,
           user_agent=None, verify_ssl=True, include_google_links=False, proxy=None):
    """
    Search the given query string using Google.

    :param str query: Query string. Must NOT be url-encoded.
    :param str tld: Top level domain.
    :param str lang: Language.
    :param str tbs: Time limits (i.e "qdr:h" => last hour,
        "qdr:d" => last 24 hours, "qdr:m" => last month).
    :param str safe: Safe search.
    :param int num: Number of results per page.
    :param int start: First result to retrieve.
    :param int stop: Last result to retrieve.
        Use None to keep searching forever.
    :param float pause: Lapse to wait between HTTP requests, measured in seconds.
        A lapse too long will make the search slow, but a lapse too short may
        cause Google to block your IP. Your mileage may vary!
    :param str country: Country or region to focus the search on. Similar to
        changing the TLD, but does not yield exactly the same results.
        Only Google knows why...
    :param dict extra_params: A dictionary of extra HTTP GET
        parameters, which must be URL encoded. For example if you don't want
        Google to filter similar results you can set the extra_params to
        {'filter': '0'} which will append '&filter=0' to every query.
    :param str user_agent: User agent for the HTTP requests.
        Use None for the default.
    :param bool verify_ssl: Verify the SSL certificate to prevent
        traffic interception attacks. Defaults to True.
    :param bool include_google_links: Includes links pointing to a Google domain.
        Defaults to False.

    :rtype: generator of str
    :return: Generator (iterator) that yields found URLs.
        If the stop parameter is None the iterator will loop forever.
    """
    # Set of hashes for the results found.
    # This is used to avoid repeated results.
    hashes = set()

    # Count the number of links yielded.
    count = 0

    # Prepare the search string.
    query = quote_plus(query)

    # If no extra_params is given, create an empty dictionary.
    # We should avoid using an empty dictionary as a default value
    # in a function parameter in Python.
    if not extra_params:
        extra_params = {}

    # Check extra_params for overlapping.
    for builtin_param in url_parameters:
        if builtin_param in extra_params.keys():
            raise ValueError(
                'GET parameter "%s" is overlapping with \
                the built-in GET parameter',
                builtin_param
            )

    # Grab the cookie from the home page.
    get_page(url_home % vars(), user_agent=user_agent, verify_ssl=verify_ssl, proxy=proxy)

    # Prepare the URL of the first request.
    if start:
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()
    else:
        if num == 10:
            url = url_search % vars()
        else:
            url = url_search_num % vars()

    # Loop until we reach the maximum result, if any (otherwise, loop forever).
    while not stop or count < stop:

        # Remember last count to detect the end of results.
        last_count = count

        # Append extra GET parameters to the URL.
        # This is done on every iteration because we're
        # rebuilding the entire URL at the end of this loop.
        for k, v in extra_params.items():
            k = quote_plus(k)
            v = quote_plus(v)
            url = url + ('&%s=%s' % (k, v))

        # Sleep between requests.
        # Keeps Google from banning you for making too many requests.
        time.sleep(pause)

        # Request the Google Search results page.
        html = get_page(url, user_agent=user_agent, verify_ssl=verify_ssl, proxy=proxy)

        # Parse the response and get every anchored URL.
        if is_bs4:
            soup = BeautifulSoup(html, 'html.parser')
        else:
            soup = BeautifulSoup(html)
        try:
            anchors = soup.find(id='search').findAll('a')
            # Sometimes (depending on the User-agent) there is
            # no id "search" in html response...
        except AttributeError:
            # Remove links of the top bar.
            gbar = soup.find(id='gbar')
            if gbar:
                gbar.clear()
            anchors = soup.findAll('a')

        # Process every anchored URL.
        for a in anchors:

            # Get the URL from the anchor tag.
            try:
                link = a['href']
            except KeyError:
                continue

            # Filter invalid links and links pointing to Google itself.
            link = filter_result(link, include_google_links)
            if not link:
                continue

            # Discard repeated results.
            h = hash(link)
            if h in hashes:
                continue
            hashes.add(h)

            # Yield the result.
            yield link

            # Increase the results counter.
            # If we reached the limit, stop.
            count += 1
            if stop and count >= stop:
                return

        # End if there are no more results.
        # XXX TODO review this logic, not sure if this is still true!
        if last_count == count:
            break

        # Prepare the URL for the next request.
        start += num
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()


# Shortcut to single-item search.
# Evaluates the iterator to return the single URL as a string.
def lucky(*args, **kwargs):
    """
    Shortcut to single-item search.

    Same arguments as the main search function, but the return value changes.

    :rtype: str
    :return: URL found by Google.
    """
    return next(search(*args, **kwargs))

# if __name__ == "__main__":
#     proxyList = ["67.43.227.227:22079",
#                 "72.10.164.178:31173",
#                 "184.168.124.233:5000",
#                 "72.10.160.90:14005",
#                 "67.43.227.230:31661",
#                 "67.43.236.20:1301",
#                 "72.10.160.170:2975",
#                 "50.28.7.107:80",
#                 "67.43.228.253:16355",
#                 "72.10.164.178:11809"]
#     for proxy in proxyList:
#         print("Trying: " + proxy)
#         try:
#             for j in search("walmart avocados", tld="ca", num=10, stop=20, pause=2):
#                 print(j)
#         except:
#             continue