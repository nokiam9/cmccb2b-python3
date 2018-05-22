from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

FILES_URLS_FIELD = 'attachment_urls'
FILES_URLS_FIELD_KEY = 'url'
FILES_FIELD = 'attachment_files'


class AttachmentPipeline(FilesPipeline):
    """ Download attachment files for Pipeline """
    # def file_path(self, request, response=None, info=None):
    #     """ files.pipelines默认文件名是url的SHA1值（确保不重复），启用本函数将修改为url地址的文件名 """
    #     filename = request.url.split('/')[-1]
    #     return 'full/%s' % filename

    def get_media_requests(self, item, info):
        """ Get urls from item and request """
        try:
            if not isinstance(item[FILES_URLS_FIELD], list):
                raise DropItem(u'Incorrect format of attachment urls field.')
            for doc in item[FILES_URLS_FIELD]:
                yield Request(doc[FILES_URLS_FIELD_KEY])
        except KeyError:
            raise DropItem(u'Incorrect format of attachment urls field .')

    def item_completed(self, results, item, info):
        """ Insert results into item, if field is not existed, create it """
        try:
            if not isinstance(item[FILES_FIELD], list):
                item[FILES_FIELD] = []
        except KeyError:
            item[FILES_FIELD] = []

        for success, file_info_or_error in results:
            if success:
                item[FILES_FIELD].append(file_info_or_error)
            else:
                raise DropItem(u'Some attachment urls download failed')
        return item


