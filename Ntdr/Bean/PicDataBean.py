import struct
import os
import sys
sys.path.append(os.path.abspath("../tool"))
from typeProperty import typed_property


class PicDataBean(object):
    __slots__ = ['_usage', '_file_ext', '_md_5', '_device_category', '_device_id', '_size',
                 '_data_nums', '_data_num', '_data']
    usage = typed_property('usage', str)
    file_ext = typed_property('file_ext', str)
    md_5 = typed_property("md_5", str)
    device_category = typed_property("device_category", str)
    device_id = typed_property("device_id", int)
    size = typed_property("size", int)  # data的大小
    data_nums = typed_property("data_nums", int)
    data_num = typed_property("data_num", int)
    data = typed_property("data", bytes)
    IMAGE_PATH = "../saveImage"
    ENCODE_TYPE = "utf-8"

    def __init__(self, *, file_ext, md_5, device_category, device_id, size, data_nums, data_num, data):
        self.usage = "image_data"
        self.file_ext = file_ext
        self.md_5 = md_5
        self.device_category = device_category
        self.device_id = device_id
        self.size = size
        self.data_nums = data_nums
        self.data_num = data_num
        self.data = data

    def format_(self):
        '''
        整个bean的格式方式
        :return:
        '''

        return "!16s8s32s16siiii" + str(self.size) + "s"

    @staticmethod
    def format_without_pic():
        '''
        去除了data
        :return:
        '''
        return "!16s8s32s16siiii"

    @property
    def all_data(self):
        return (
            self.usage, self.file_ext,
            self.md_5,
            self.device_category,
            self.device_id,
            self.size,
            self.data_nums,
            self.data_num,
            self.data
        )

    @property
    def pack_data(self):
        '''
        将Bean打包，返回已经按照format格式打包的数据包
        :return:
        '''
        __pack_data_ = tuple(
            map(lambda m: m.encode(PicDataBean.ENCODE_TYPE) if type(m) == str else m, self.all_data)
        )
        return struct.pack(self.format_(), *__pack_data_)

    @staticmethod
    def unpack_date(pack_data):
        # 这里有问题的，data不应该被编码。而应该是保存起来
        pic_data = pack_data[88:]
        str_data = pack_data[:88]

        unpack_data_ = tuple(
            map(lambda m: m.decode(PicDataBean.ENCODE_TYPE).strip("\x00") if type(m) == bytes else m,
                struct.unpack(PicDataBean.format_without_pic(), str_data))
        )

        bean = PicDataBean(file_ext=unpack_data_[1], md_5=unpack_data_[2], device_category=unpack_data_[3],
                           device_id=unpack_data_[4],
                           size=unpack_data_[5], data_nums=unpack_data_[6], data_num=unpack_data_[7], data=pic_data)
        # with open(os.path.join(PicDataBean.IMAGE_PATH,bean.md_5+bean.file_ext),'ab') as f:
        # f.write(bean.data)
        return bean

    def send(self, __send, addr):
        __send.send_apply(self.pack_data, addr)
