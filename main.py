from vk_methods import get_group_info_by_shortname, get_group_wall_by_search, download_photos_into_folder_by_urls
from functools import reduce



def _attachments_mapping(x):
    tp = x['type']
    if tp == 'doc':
        return x['doc']['url']
    elif tp == 'photo':
        return next(filter(lambda y: y['type'] == 'z', x['photo']['sizes']))['url']
    return None


if __name__ == '__main__':
    res = get_group_info_by_shortname(input('Введи имя группы\n'))
    if 'error' in res:
        if res['error']['error_code'] == 100:
            print('Имя группы неверно')
            exit()
    group_id = res['response'][0]['id']
    res = get_group_wall_by_search(group_id, input('Введи поисковую строку (хэштег)\n'))
    types = ['doc', 'gif', 'photo']
    urls = list(filter(lambda x: x is not None, reduce(lambda a, x: a + list(map(_attachments_mapping, x.get('attachments', []))), res, [])))
    download_photos_into_folder_by_urls(input('Введите папку\n'), urls=urls)
    print('Готово!')
