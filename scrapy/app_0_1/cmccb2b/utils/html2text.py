# -*- coding: utf-8-*-
import re

CHAR_ENTITIES = {'nbsp': ' ',
                 '160': ' ',
                 'lt': '<',
                 '60': '<',
                 'gt': '>',
                 '62': '>',
                 'amp': '&',
                 '38': '&',
                 'quot': '"',
                 '34': '"',
                 }


def filter_tags(htmlstr):
    """
    过滤HTML中的标签, 将HTML中js脚本和标签等信息去掉
    Usage:
        s = fp.read().decode()
        news = filter_tags(s)
    """
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA，这是不允许xml解析的内容
    re_script = re.compile(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', re.I | re.S)  # 匹配script脚本
    # Notice: js代码中有 <，导致无法过滤，改为.*?，非贪婪模式的任意字符，且设置re.S包含换行符
    # re_script = re.compile(r'<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # 原始代码
    ''' <\s*script[^>]*>[^<]*<\s*/\s*script\s*> 模式分析：
    <       以字符<开始
    \s*     可能出现的无限个，空白字符
    script  字符串script
    [^>]*   可能出现的的无限个，不是>的字符
    >       字符>
    [^<]*   可能出现的的无限个，不是<的字符，这是js的代码
    <       字符<
    \s*     可能出现的的无限个，空白字符
    /       字符／
    \s*     可能出现的的无限个，空白字符
    script  字符串script
    \s*     可能出现的的无限个，空白字符
    >       字符>
    re.I    忽略大小写
    '''
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    '''
    <       开始字符<
    /?      可能出现一次的，字符/
    \w+     至少出现一次的，单词字符[A-Za-Z0-9_]
    [^>]*   可能出现的，不是>的字符
    >       字符>
    '''
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    re_blank_line = re.compile('(\r\n|\n)+')  # 如果一个或者多个换行符
    re_tab = re.compile('\t+')

    s = re_cdata.sub('', htmlstr)       # 去掉CDATA
    s = re_script.sub('', s)            # 去掉SCRIPT
    s = re_style.sub('', s)             # 去掉style
    s = re_br.sub('\n', s)              # 将br转换为换行
    s = re_h.sub('', s)                 # 去掉所有的HTML标签
    s = re_comment.sub('', s)           # 去掉HTML注释
    s = re_blank_line.sub('\n', s)      # 只保留一个
    s = re_tab.sub('', s)

    s = _replace_char_entity(s)  # 继续替换实体字符
    return s


def _replace_char_entity(htmlstr):
    """
    替换常用HTML字符实体.
    使用正常的字符替换HTML中特殊的字符实体.
    你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
    """
    re_char_entity = re.compile(r'&#?(?P<name>\w+);')
    '''
    &               字符&
    #?              可能出现的，字符#
    (?P<name>\w+)   定义分组name，是一个\w+的单词
    ;               字符;
    '''
    sz = re_char_entity.search(htmlstr)
    while sz:
        # entity = sz.group()  # entity全称，如&gt; 本语句似乎无效，因为没有后续动作
        key = sz.group('name')  # 去除&;后entity,如&gt;为gt
        try:
            htmlstr = re_char_entity.sub(CHAR_ENTITIES[key], htmlstr, 1)  # 查找特殊字符表，替换第一个特殊字符
            sz = re_char_entity.search(htmlstr)  # 继续匹配pattern
        except KeyError:
            # 如果该特殊字符的替换表示不存在，则以空串代替，并继续匹配pattern
            htmlstr = re_char_entity.sub('', htmlstr, 1)
            sz = re_char_entity.search(htmlstr)
    return htmlstr

