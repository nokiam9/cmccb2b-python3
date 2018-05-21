from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

FILES_URLS_FIELD = 'attachment_urls'
FILES_URLS_SUB_FIELD = 'url'
FILES_FIELD = 'attachment_files'


class AttachmentPipeline(FilesPipeline):
    """ Download attachment files for Pipeline """
    # def file_path(self, request, response=None, info=None):
    #     """ files.pipelines默认文件名是url的SHA1值（确保不重复），启用本函数将修改为url地址的文件名 """
    #     filename = request.url.split('/')[-1]
    #     return 'full/%s' % filename

    def get_media_requests(self, item, info):
        for doc in item[FILES_URLS_FIELD]:
            yield Request(doc[FILES_URLS_SUB_FIELD])

    def item_completed(self, results, item, info):
        for success, file_info_or_error in results:
            if success:
                item[FILES_FIELD].append(file_info_or_error)
            else:
                raise DropItem(u'Some attachment urls download failed')
        return item


