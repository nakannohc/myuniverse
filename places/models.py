# -*- coding: utf-8 -*-
from django.db import models

keywords = [u'ธนาคาร',  u'ATM',  u'CDM',  u'บริษัทเงินทุน',  u'บริษัทเครดิตฟองซิเอร์',
            u'บริษัทหลักทรัพย์',  u'ออมสิน',  u'ธกส',  u'ธอส',  u'ธสน',  u'ธนาคารอิสลาม',
            u'SME Bank',  u'ประกัน',  u'แคปปิตอล โอเค',  u'เจเนอรัล คาร์ด เซอร์วิสเซส',
            u'ซิตี้ คอนซูเมอร์',  u'เทสโก้ คาร์ด',  u'บัตรกรุงไทย',  u'บัตรกรุงศรีอยุธยา',
            u'อยุธยา แคปปิตอล',  u'อิออน ธนสินทรัพย์',  u'อีซี่บาย',  u'ลิสซิ่ง',  u'แฟคตอริ่ง',
            u'กรุงไทยธุรกิจลีสซิ่ง',  u'แคปปิตอล โอเค',  u'เงินติดล้อ',  u'เงินสดทันใจ',
            u'จี แคปปิตอล',  u'เจ เอ็ม ที เน็ทเวอร์ค เซอร์วิสเซ็ส',  u'เจ เอ็ม ที พลัส',
            u'เจเนอรัล คาร์ด เซอร์วิสเซส',  u'ซิงเกอร์ประเทศไทย',  u'ซิตี้คอร์ป ลิสซิ่ง(ประเทศไทย)',
            u'ไซเบอร์เนตติคส์',  u'โตโยต้าลิสซิ่ง',  u'เทสโก้ คาร์ด เซอร์วิสเซส',  u'ไทยพาณิชย์ลีสซิ่ง',
            u'ไทยเอซ แคปปิตอล',  u'บัตรกรุงไทย',  u'บัตรกรุงศรีอยุธยา',  u'พรอมิส (ประเทศไทย)',
            u'มีนาลิสซิ่ง',  u'เมืองไทย ลิสซิ่ง',  u'แมคคาเล กรุ๊พ',  u'รีโซลูชั่น เวย์',  u'วัฒนาธนวินทรัพย์',
            u'วี แคช เอ็นเตอร์ไพรส์',  u'ศักดิ์สยามพาณิชย์ลิสซิ่ง',  u'สยามเจเนอรัลแฟคตอริ่ง',  u'สินมิตร',
            u'อยุธยา แคปปิตอล เซอร์วิสเซส',  u'อยุธยา แคปปิตอล ออโต้ ลีส',  u'อินเทลลิเจนท์ ทีที. พาวเวอร์',
            u'อิออน ธนสินทรัพย์ (ไทยแลนด์)',  u'อีซี่ บาย',  u'เอเซียเสริมกิจลีสซิ่ง',  u'ไอร่า แอนด์ ไอฟุล',
            u'เงินติดล้อ',  u'เงินสดทันใจ',  u'โดเมสติค แคปปิตอล 2015',  u'ทีเค เงินสดทันใจ',
            u'ไทยเอช แคปปิตอล',  u'ปิยะระยองกรุ๊ป',  u'พี.เอส.เอ็น.ลีสซิ่ง',  u'มีนาลีสซิ่ง',
            u'เมืองไทย ลีสซิ่ง',  u'แมคคาเล กรุ๊พ',  u'ไมด้า ลีสซิ่ง',  u'สหไพบูลย์(2558)',
            u'อินเทลลิเจนท์ ทีที พาวเวอร์',  u'พสิษฐ์ภาคิณ',  u'สหกรณ์',  u'กลุ่มเกษตกร',  u'กลุ่มอาชีพ',
            u'กองทุนหมู่บ้าน',  u'ออมทรัพย์เพื่อการผลิต',  u'การเงินชุมชน',  u'กลุ่มสัจจะ',  u'family mart',
            u'max valu',  u'max value',  u'108 shop',  u'cp freshmart',  u'บิ๊กซี',  u'เทสโก้',
            u'makro',  u'ห้างสรรพสินค้า',  u'ศูนย์การค้า',  u'ไปรษณีย์',  u'AIS',  u'telewiz',  u'เทเลวิซ',
            u'ทรูช็อป',  u'Dtac',  u'ดีแทค',  u'ศูนย์บริการ ทีโอที',  u'ศูนย์บริการ TOT',  u'เจมาร์ท',
            u'ปั๊มน้ำมัน',  u'ตู้เติมเงิน', u'ลอว์สัน', u'Lawson', u'CJ express']

class Grid(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=250)
    place_type = models.CharField(max_length=50)
    zone = models.CharField(max_length=50, blank=True, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    x = models.IntegerField()
    y = models.IntegerField()
    keyword = models.CharField(max_length=250)
    count_place = models.IntegerField(default=0)
    scanned = models.BooleanField(default=False)


class Place(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=250)
    lat = models.FloatField()
    lng = models.FloatField()
    address = models.TextField()
    place_id = models.CharField(max_length=250, null=True)
    permanently_closed = models.BooleanField(default=False)
    place_detail = models.TextField(null=True)
    grid = models.ForeignKey(Grid, blank=True, null=True)


class KeywordSummary(models.Model):
    def __unicode__(self):
        return self.keyword

    keyword = models.CharField(max_length=250)
    grid_count = models.IntegerField()
    grid_complete = models.IntegerField()
