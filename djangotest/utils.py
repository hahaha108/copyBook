import math


def custompaginator(num_pages, current_page, max_page):
    middle = math.ceil(max_page / 2)
    # 特殊情况，最大页数小于最大显示的页数
    if num_pages < max_page:
        start = 1
        end = num_pages
    else:
        # 当前页小于等于middle+1 时。
        if current_page <= middle +1:
            start = 1
            end = max_page
        else:
            start = current_page - middle
            end = current_page + middle - 1
            # 当前页在尾巴的情况
            if current_page + middle > num_pages:
                start = num_pages - max_page + 1
                end = num_pages
    return start,end