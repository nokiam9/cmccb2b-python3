import logging
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

DEFAULT_FILES_URLS_FIELD_KEY = 'url'

logger = logging.getLogger(__name__)


class AttachmentPipeline(FilesPipeline):
    """ Download attachment files for Pipeline """

    def get_media_requests(self, item, info):
        """ Get urls from item and request """
        files_urls_field_key = info.spider.settings.get(
            'FILES_URLS_FIELD_KEY', default=DEFAULT_FILES_URLS_FIELD_KEY)   # get settings from info.spider

        try:
            if not isinstance(item[self.files_urls_field], list):   # self.files_urls_field from FilesPipeline
                raise DropItem(u"Attachment urls field must be list type.")
        except KeyError:
            raise DropItem(u"Attachment urls field isn't existed.")

        try:
            item[self.files_result_field] = []      # self.files_result_field from FilesPipeline
        except KeyError:
            raise DropItem(u"Attachment files field isn't existed.")

        try:
            for x in item[self.files_urls_field]:
                yield Request(x[files_urls_field_key])
        except KeyError:
            raise DropItem(u'Incorrect list format of attachment urls field.')

    def item_completed(self, results, item, info):
        """ Insert results into item, if field is not existed, create it """

        for success, file_info_or_error in results:
            if success:
                item[self.files_result_field].append(file_info_or_error)
            else:
                raise DropItem(u'Some attachment urls download failed')
        return item

    # def file_path(self, request, response=None, info=None):
    #     """ Set filename of download file """
    #     # files.pipelines默认文件名是url的SHA1值（确保不重复），启用本函数将修改为url地址的文件名 """
    #     filename = request.url.split('/')[-1]
    #     return 'full/%s' % filename

