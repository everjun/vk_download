import re
import requests
import os
import vk_settings


def make_request(method, **kwargs):
    request = vk_settings.API_URL_METHODS
    request += method
    kwargs['access_token'] = vk_settings.SERVICE_TOKEN
    kwargs['v'] = vk_settings.VERSION
    response = requests.get(request, params=kwargs)
    return response.json()


def get_group_info_by_shortname(shortname):
    if re.match('public\d+', shortname):
        shortname = shortname[len('public'):]
    return make_request('groups.getById', group_id=shortname)


def get_group_wall_by_search(group_id, search_string=''):
    offset = 0
    result = []
    limit = 100
    wall = make_request('wall.search', owner_id='-%s' % group_id, query=search_string)
    count = wall['response']['count']
    result += wall['response']['items']
    while offset < count:
        wall = make_request('wall.search', owner_id='-%s' % group_id, query=search_string, offset=offset)
        result += wall['response']['items']
        offset += limit
    return result


def download_photos_into_folder_by_urls(folder, urls=[]):
    for i, url in enumerate(urls):
        print('%s / %s' % (i, len(urls)))
        if url.endswith('jpg'):
            name = 'pic_%s.jpg' % i
        else:
            name = 'pic_%s.gif' % i
            url += '.gif'
        with open(os.path.join(folder, name), 'wb') as handle:
            response = requests.get(url, stream=True)

            if not response.ok:
                print
                response

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
