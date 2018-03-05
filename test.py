#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import io
import six
from zipcodetw.util import Address

def test_address_init():

    expected_tokens = [('', '', '臺北', '市'), ('', '', '大安', '區'), ('', '', '市府', '路'), ('1', '', '', '號')]
    assert Address('臺北市大安區市府路1號').tokens == expected_tokens
    assert Address('臺北市大安區市府路1號').tokens == expected_tokens

def test_address_init_subno():

    expected_tokens = [('', '', '臺北', '市'), ('', '', '大安', '區'), ('', '', '市府', '路'), ('1', '之1', '', '號')]
    assert Address('臺北市大安區市府路1之1號').tokens == expected_tokens
    assert Address('臺北市大安區市府路1之1號').tokens == expected_tokens

def test_address_init_tricky_input():

    assert Address('桃園縣中壢市普義').tokens == [('', '', '桃園', '縣'), ('', '', '中壢', '市'), ('', '', '普義', '')]
    assert Address('桃園縣中壢市普義10號').tokens == [('', '', '桃園', '縣'), ('', '', '中壢', '市'), ('', '', '普義', ''), ('10', '', '', '號')]

    assert Address('臺北市中山區敬業1路').tokens == [('', '', '臺北', '市'), ('', '', '中山', '區'), ('', '', '敬業1', '路')]
    assert Address('臺北市中山區敬業1路10號').tokens == [('', '', '臺北', '市'), ('', '', '中山', '區'), ('', '', '敬業1', '路'), ('10', '', '', '號')]

def test_address_init_normalization():

    expected_tokens = [('', '', '臺北', '市'), ('', '', '大安', '區'), ('', '', '市府', '路'), ('1', '之1', '', '號')]
    assert Address('臺北市大安區市府路1之1號').tokens == expected_tokens
    assert Address('台北市大安區市府路1之1號').tokens == expected_tokens
    assert Address('臺北市大安區市府路１之１號').tokens == expected_tokens
    assert Address('臺北市　大安區　市府路 1 之 1 號').tokens == expected_tokens
    assert Address('臺北市，大安區，市府路 1 之 1 號').tokens == expected_tokens
    assert Address('臺北市, 大安區, 市府路 1 之 1 號').tokens == expected_tokens
    assert Address('臺北市, 大安區, 市府路 1 - 1 號').tokens == expected_tokens

def test_address_init_normalization_chinese_number():

    assert Address.normalize('八德路') == '八德路'
    assert Address.normalize('三元街') == '三元街'

    assert Address.normalize('三號') == '3號'
    assert Address.normalize('十八號') == '18號'
    assert Address.normalize('三十八號') == '38號'

    assert Address.normalize('三段') == '3段'
    assert Address.normalize('十八路') == '18路'
    assert Address.normalize('三十八街') == '38街'

    assert Address.normalize('信義路一段') == '信義路1段'
    assert Address.normalize('敬業一路') == '敬業1路'
    assert Address.normalize('愛富三街') == '愛富3街'

def test_address_flat():

    addr = Address('臺北市大安區市府路1之1號')
    assert addr.flat(1) == addr.flat(-3) == '臺北市'
    assert addr.flat(2) == addr.flat(-2) == '臺北市大安區'
    assert addr.flat(3) == addr.flat(-1) == '臺北市大安區市府路'
    assert addr.flat() == '臺北市大安區市府路1之1號'

def test_address_repr():

    if six.PY2:
        repr_str = "Address(u'\\u81fa\\u5317\\u5e02\\u5927\\u5b89\\u5340\\u5e02\\u5e9c\\u8def1\\u865f')"
    else:
        repr_str = "Address('臺北市大安區市府路1號')"
    assert repr(Address('臺北市大安區市府路1號')) == repr_str
    assert repr(eval(repr_str)) == repr_str

from zipcodetw.util import Rule

def test_rule_init():

    rule = Rule('臺北市,中正區,八德路１段,全')
    assert rule.tokens == [('', '', '臺北', '市'), ('', '', '中正', '區'), ('', '', '八德', '路'), ('', '', '1', '段')]
    assert rule.rule_tokens == set(['全'])

    rule = Rule('臺北市,中正區,三元街,單全')
    assert rule.tokens == [('', '', '臺北', '市'), ('', '', '中正', '區'), ('', '', '三元', '街')]
    assert rule.rule_tokens == set(['單', '全'])

    rule = Rule('臺北市,中正區,三元街,雙  48號以下')
    assert rule.tokens == [('', '', '臺北', '市'), ('', '', '中正', '區'), ('', '', '三元', '街'), ('48', '', '', '號')]
    assert rule.rule_tokens == set(['雙', '以下'])

    rule = Rule('臺北市,中正區,大埔街,單  15號以上')
    assert rule.tokens == [('', '', '臺北', '市'), ('', '', '中正', '區'), ('', '', '大埔', '街'), ('15', '', '', '號')]
    assert rule.rule_tokens == set(['單', '以上'])

    rule = Rule('臺北市,中正區,中華路１段,單  25之   3號以下')
    assert rule.tokens == [('', '', '臺北', '市'), ('', '', '中正', '區'), ('', '', '中華', '路'), ('', '', '1', '段'), ('25', '之3', '', '號')]
    assert rule.rule_tokens == set(['單', '以下'])

    rule = Rule('臺北市,中正區,中華路１段,單  27號至  47號')
    assert rule.tokens == [('', '', '臺北', '市'), ('', '', '中正', '區'), ('', '', '中華', '路'), ('', '', '1', '段'), ('27', '', '', '號'), ('47', '', '', '號')]
    assert rule.rule_tokens == set(['單', '至'])

    rule = Rule('臺北市,中正區,仁愛路１段,連   2之   4號以上')
    assert rule.tokens == [('', '', '臺北', '市'), ('', '', '中正', '區'), ('', '', '仁愛', '路'), ('', '', '1', '段'), ('2', '之4', '', '號')]
    assert rule.rule_tokens == set([ '以上'])

    rule = Rule('臺北市,中正區,杭州南路１段,　  14號含附號')
    assert rule.tokens == [('', '', '臺北', '市'), ('', '', '中正', '區'), ('', '', '杭州南', '路'), ('', '', '1', '段'), ('14', '', '', '號')]
    assert rule.rule_tokens == set(['含附號'])

    rule = Rule('臺北市,大同區,哈密街,　  47附號全')
    assert rule.tokens == [('', '', '臺北', '市'), ('', '', '大同', '區'), ('', '', '哈密', '街'), ('47', '', '', '號')]
    assert rule.rule_tokens == set(['附號全'])

    rule = Rule('臺北市,大同區,哈密街,雙  68巷至  70號含附號全')
    assert rule.tokens == [('', '', '臺北', '市'), ('', '', '大同', '區'), ('', '', '哈密', '街'), ('68', '', '', '巷'), ('70', '', '', '號')]
    assert rule.rule_tokens == set(['雙', '至', '含附號全'])

    rule = Rule('桃園縣,中壢市,普義,連  49號含附號以下')
    assert rule.tokens == [('', '', '桃園', '縣'), ('', '', '中壢', '市'), ('', '', '普義', ''), ('49', '', '', '號')]
    assert rule.rule_tokens == set(['含附號以下'])

    rule = Rule('臺中市,西屯區,西屯路３段西平南巷,　   1之   3號及以上附號')
    assert rule.tokens == [('', '', '臺中', '市'), ('', '', '西屯', '區'), ('', '', '西屯', '路'), ('', '', '3', '段'), ('', '', '西平南', '巷'), ('1', '之3', '', '號')]
    assert rule.rule_tokens == set(['及以上附號'])

def test_rule_init_tricky_input():

    rule = Rule('新北市,中和區,連城路,雙 268之   1號以下')
    assert rule.tokens == [('', '', '新北', '市'), ('', '', '中和', '區'), ('', '', '連城', '路'), ('268', '之1', '', '號')]
    assert rule.rule_tokens == set(['雙', '以下'])

    rule = Rule('新北市,泰山區,全興路,全')
    assert rule.tokens == [('', '', '新北', '市'), ('', '', '泰山', '區'), ('', '', '全興', '路')]
    assert rule.rule_tokens == set(['全'])

def test_rule_repr():

    if six.PY2:
        repr_str = "Rule(u'\\u81fa\\u5317\\u5e02\\u5927\\u5b89\\u5340\\u5e02\\u5e9c\\u8def1\\u865f\\u4ee5\\u4e0a')"
    else:
        repr_str = "Rule('臺北市大安區市府路1號以上')"
    assert repr(Rule('臺北市大安區市府路1號以上')) == repr_str
    assert repr(eval(repr_str)) == repr_str

def test_rule_match():

    # standard address w/ standard rules

    addr = Address('臺北市大安區市府路5號')

    # 全單雙
    assert     Rule('臺北市大安區市府路全').match(addr)
    assert     Rule('臺北市大安區市府路單全').match(addr)
    assert not Rule('臺北市大安區市府路雙全').match(addr)

    # 以上 & 以下
    assert not Rule('臺北市大安區市府路6號以上').match(addr)
    assert     Rule('臺北市大安區市府路6號以下').match(addr)
    assert     Rule('臺北市大安區市府路5號以上').match(addr)
    assert     Rule('臺北市大安區市府路5號').match(addr)
    assert     Rule('臺北市大安區市府路5號以下').match(addr)
    assert     Rule('臺北市大安區市府路4號以上').match(addr)
    assert not Rule('臺北市大安區市府路4號以下').match(addr)

    # 至
    assert not Rule('臺北市大安區市府路1號至4號').match(addr)
    assert     Rule('臺北市大安區市府路1號至5號').match(addr)
    assert     Rule('臺北市大安區市府路5號至9號').match(addr)
    assert not Rule('臺北市大安區市府路6號至9號').match(addr)

    # 附號
    assert not Rule('臺北市大安區市府路6號及以上附號').match(addr)
    assert     Rule('臺北市大安區市府路6號含附號以下').match(addr)
    assert     Rule('臺北市大安區市府路5號及以上附號').match(addr)
    assert     Rule('臺北市大安區市府路5號含附號').match(addr)
    assert not Rule('臺北市大安區市府路5附號全').match(addr)
    assert     Rule('臺北市大安區市府路5號含附號以下').match(addr)
    assert     Rule('臺北市大安區市府路4號及以上附號').match(addr)
    assert not Rule('臺北市大安區市府路4號含附號以下').match(addr)

    # 單雙 x 以上, 至, 以下
    assert     Rule('臺北市大安區市府路單5號以上').match(addr)
    assert not Rule('臺北市大安區市府路雙5號以上').match(addr)
    assert     Rule('臺北市大安區市府路單1號至5號').match(addr)
    assert not Rule('臺北市大安區市府路雙1號至5號').match(addr)
    assert     Rule('臺北市大安區市府路單5號至9號').match(addr)
    assert not Rule('臺北市大安區市府路雙5號至9號').match(addr)
    assert     Rule('臺北市大安區市府路單5號以下').match(addr)
    assert not Rule('臺北市大安區市府路雙5號以下').match(addr)

def test_rule_match_gradual_address():

    # standard rule w/ gradual addresses

    rule = Rule('臺北市中正區丹陽街全')
    assert not rule.match(Address('臺北市'))
    assert not rule.match(Address('臺北市中正區'))
    assert not rule.match(Address('臺北市中正區仁愛路１段'))
    assert not rule.match(Address('臺北市中正區仁愛路１段1號'))

    rule = Rule('臺北市,中正區,仁愛路１段,　   1號')
    assert not rule.match(Address('臺北市'))
    assert not rule.match(Address('臺北市中正區'))
    assert not rule.match(Address('臺北市中正區仁愛路１段'))
    assert     rule.match(Address('臺北市中正區仁愛路１段1號'))

def test_rule_match_rule_all():

    # Be careful of the 全! It will bite you!

    rule = Rule('臺北市,中正區,八德路１段,全')
    assert     rule.match(Address('臺北市中正區八德路１段1號'))
    assert     rule.match(Address('臺北市中正區八德路１段9號'))
    assert not rule.match(Address('臺北市中正區八德路２段1號'))
    assert not rule.match(Address('臺北市中正區八德路２段9號'))

    rule = Rule('臺北市,中正區,三元街,單全')
    assert     rule.match(Address('臺北市中正區三元街1號'))
    assert not rule.match(Address('臺北市中正區三元街2號'))
    assert not rule.match(Address('臺北市中正區大埔街1號'))

    rule = Rule('臺北市,大同區,哈密街,　  45巷全')
    assert     rule.match(Address('臺北市大同區哈密街45巷1號'))
    assert     rule.match(Address('臺北市大同區哈密街45巷9號'))
    assert not rule.match(Address('臺北市大同區哈密街46巷1號'))
    assert not rule.match(Address('臺北市大同區哈密街46巷9號'))

def test_rule_match_tricky_input():

    # The address matched by it must have a even number.
    rule  = Rule('信義路一段雙全')

    addr1 = Address('信義路一段')
    addr2 = Address('信義路一段1號')
    addr3 = Address('信義路一段2號')

    assert not rule.match(addr1)
    assert not rule.match(addr2)
    assert     rule.match(addr3)

def test_rule_match_subno():

    rule = Rule('臺北市,中正區,杭州南路１段,　  14號含附號')
    assert not rule.match(Address('臺北市中正區杭州南路1段13號'))
    assert not rule.match(Address('臺北市中正區杭州南路1段13-1號'))
    assert     rule.match(Address('臺北市中正區杭州南路1段14號'))
    assert     rule.match(Address('臺北市中正區杭州南路1段14-1號'))
    assert not rule.match(Address('臺北市中正區杭州南路1段15號'))
    assert not rule.match(Address('臺北市中正區杭州南路1段15-1號'))

    rule = Rule('臺北市,大同區,哈密街,　  47附號全')
    assert not rule.match(Address('臺北市大同區哈密街46號'))
    assert not rule.match(Address('臺北市大同區哈密街46-1號'))
    assert not rule.match(Address('臺北市大同區哈密街47號'))
    assert     rule.match(Address('臺北市大同區哈密街47-1號'))
    assert not rule.match(Address('臺北市大同區哈密街48號'))
    assert not rule.match(Address('臺北市大同區哈密街48-1號'))

    rule = Rule('臺北市,大同區,哈密街,雙  68巷至  70號含附號全')
    assert not rule.match(Address('臺北市大同區哈密街66號'))
    assert not rule.match(Address('臺北市大同區哈密街66-1巷'))
    assert not rule.match(Address('臺北市大同區哈密街67號'))
    assert not rule.match(Address('臺北市大同區哈密街67-1巷'))
    assert     rule.match(Address('臺北市大同區哈密街68巷'))
    assert     rule.match(Address('臺北市大同區哈密街68-1號'))
    assert not rule.match(Address('臺北市大同區哈密街69號'))
    assert not rule.match(Address('臺北市大同區哈密街69-1巷'))
    assert     rule.match(Address('臺北市大同區哈密街70號'))
    assert     rule.match(Address('臺北市大同區哈密街70-1號'))
    assert not rule.match(Address('臺北市大同區哈密街71號'))
    assert not rule.match(Address('臺北市大同區哈密街71-1號'))

    rule = Rule('桃園縣,中壢市,普義,連  49號含附號以下')
    assert     rule.match(Address('桃園縣中壢市普義48號'))
    assert     rule.match(Address('桃園縣中壢市普義48-1號'))
    assert     rule.match(Address('桃園縣中壢市普義49號'))
    assert     rule.match(Address('桃園縣中壢市普義49-1號'))
    assert not rule.match(Address('桃園縣中壢市普義50號'))
    assert not rule.match(Address('桃園縣中壢市普義50-1號'))

    rule = Rule('臺中市,西屯區,西屯路３段西平南巷,　   2之   3號及以上附號')
    assert not rule.match(Address('臺中市西屯區西屯路3段西平南巷1號'))
    assert not rule.match(Address('臺中市西屯區西屯路3段西平南巷1-1號'))
    assert not rule.match(Address('臺中市西屯區西屯路3段西平南巷2號'))
    assert not rule.match(Address('臺中市西屯區西屯路3段西平南巷2-2號'))
    assert     rule.match(Address('臺中市西屯區西屯路3段西平南巷2-3號'))
    assert     rule.match(Address('臺中市西屯區西屯路3段西平南巷3號'))
    assert     rule.match(Address('臺中市西屯區西屯路3段西平南巷3-1號'))
    assert     rule.match(Address('臺中市西屯區西屯路3段西平南巷4號'))
    assert     rule.match(Address('臺中市西屯區西屯路3段西平南巷4-1號'))

from zipcodetw.util import Directory

class TestDirectory(object):

    def setup(self):

        chp_csv_lines = io.BytesIO('''郵遞區號,縣市名稱,鄉鎮市區,原始路名,投遞範圍
10058,臺北市,中正區,八德路１段,全
10079,臺北市,中正區,三元街,單全
10070,臺北市,中正區,三元街,雙  48號以下
10079,臺北市,中正區,三元街,雙  50號以上
10068,臺北市,中正區,大埔街,單  15號以上
10068,臺北市,中正區,大埔街,雙  36號以上
10051,臺北市,中正區,中山北路１段,單   3號以下
10041,臺北市,中正區,中山北路１段,雙  48號以下
10051,臺北市,中正區,中山南路,單   5號以下
10041,臺北市,中正區,中山南路,雙  18號以下
10002,臺北市,中正區,中山南路,　   7號
10051,臺北市,中正區,中山南路,　   9號
10048,臺北市,中正區,中山南路,單  11號以上
10001,臺北市,中正區,中山南路,　  20號
10043,臺北市,中正區,中華路１段,單  25之   3號以下
10042,臺北市,中正區,中華路１段,單  27號至  47號
10010,臺北市,中正區,中華路１段,　  49號
10042,臺北市,中正區,中華路１段,單  51號以上
10065,臺北市,中正區,中華路２段,單  79號以下
10066,臺北市,中正區,中華路２段,單  81號至 101號
10068,臺北市,中正區,中華路２段,單 103號至 193號
10069,臺北市,中正區,中華路２段,單 195號至 315號
10067,臺北市,中正區,中華路２段,單 317號至 417號
10072,臺北市,中正區,中華路２段,單 419號以上
10055,臺北市,中正區,丹陽街,全
10051,臺北市,中正區,仁愛路１段,　   1號
10052,臺北市,中正區,仁愛路１段,連   2之   4號以上
10055,臺北市,中正區,仁愛路２段,單  37號以下
10060,臺北市,中正區,仁愛路２段,雙  48號以下
10056,臺北市,中正區,仁愛路２段,單  39號至  49號
10056,臺北市,中正區,仁愛路２段,雙  48之   1號至  64號
10062,臺北市,中正區,仁愛路２段,單  51號以上
10063,臺北市,中正區,仁愛路２段,雙  66號以上
20201,基隆市,中正區,義一路,　   1號
20241,基隆市,中正區,義一路,連   2號以上
20250,基隆市,中正區,義二路,全
20241,基隆市,中正區,義三路,單全
20248,基隆市,中正區,漁港一街,全
20249,基隆市,中正區,漁港二街,全
20249,基隆市,中正區,漁港三街,全
20249,基隆市,中正區,調和街,全
20248,基隆市,中正區,環港街,全
20243,基隆市,中正區,豐稔街,全
20249,基隆市,中正區,觀海街,全
36046,苗栗縣,苗栗市,大埔街,全
81245,高雄市,小港區,豐田街,全
81245,高雄市,小港區,豐登街,全
81245,高雄市,小港區,豐善街,全
81245,高雄市,小港區,豐街,全
81245,高雄市,小港區,豐點街,全
81257,高雄市,小港區,寶山街,全
81362,高雄市,左營區,大中一路,單 331號以上
81362,高雄市,左營區,大中一路,雙 386號以上
81362,高雄市,左營區,大中二路,單 241號以下
81368,高雄市,左營區,大中二路,雙 200號以下
81369,高雄市,左營區,大中二路,雙 202號至 698號
81369,高雄市,左營區,大中二路,單 243號至 479號
81365,高雄市,左營區,大中二路,單 481號以上
81354,高雄市,左營區,大中二路,雙 700號以上
81357,高雄市,左營區,大順一路,單  91號至  95號
81357,高雄市,左營區,大順一路,雙  96號至 568號
81357,高雄市,左營區,大順一路,單 201號至 389巷'''.encode('utf-8'))

        self.dir_ = Directory(':memory:', keep_alive=True)
        self.dir_.load_chp_csv(chp_csv_lines)

    def test_find(self):

        # It retuns a partial zipcode when the address doesn't match any rule in
        # our directory.

        # 10043,臺北市,中正區,中華路１段,單  25之   3號以下
        assert self.dir_.find('臺北市中正區中華路１段25號') == '10043'
        assert self.dir_.find('臺北市中正區中華路１段25-2號') == '10043'
        assert self.dir_.find('臺北市中正區中華路１段25-3號') == '10043'
        assert self.dir_.find('臺北市中正區中華路１段25-4號') == '100'
        assert self.dir_.find('臺北市中正區中華路１段26號') == '100'

        # 10042,臺北市,中正區,中華路１段,單  27號至  47號
        assert self.dir_.find('臺北市中正區中華路１段25號') == '10043'
        assert self.dir_.find('臺北市中正區中華路１段26號') == '100'
        assert self.dir_.find('臺北市中正區中華路１段27號') == '10042'
        assert self.dir_.find('臺北市中正區中華路１段28號') == '100'
        assert self.dir_.find('臺北市中正區中華路１段29號') == '10042'
        assert self.dir_.find('臺北市中正區中華路１段45號') == '10042'
        assert self.dir_.find('臺北市中正區中華路１段46號') == '100'
        assert self.dir_.find('臺北市中正區中華路１段47號') == '10042'
        assert self.dir_.find('臺北市中正區中華路１段48號') == '100'
        assert self.dir_.find('臺北市中正區中華路１段49號') == '10010'

        # 10010,臺北市,中正區,中華路１段,　  49號
        assert self.dir_.find('臺北市中正區中華路１段48號') == '100'
        assert self.dir_.find('臺北市中正區中華路１段49號') == '10010'
        assert self.dir_.find('臺北市中正區中華路１段50號') == '100'

        # 10042,臺北市,中正區,中華路１段,單  51號以上
        assert self.dir_.find('臺北市中正區中華路１段49號') == '10010'
        assert self.dir_.find('臺北市中正區中華路１段50號') == '100'
        assert self.dir_.find('臺北市中正區中華路１段51號') == '10042'
        assert self.dir_.find('臺北市中正區中華路１段52號') == '100'
        assert self.dir_.find('臺北市中正區中華路１段53號') == '10042'

    def test_find_gradually(self):

        assert self.dir_.find('臺北市') == '100'
        assert self.dir_.find('臺北市中正區') == '100'
        assert self.dir_.find('臺北市中正區仁愛路１段') == '1005'
        assert self.dir_.find('臺北市中正區仁愛路１段1號') == '10051'

    def test_find_middle_token(self):

        assert self.dir_.find('左營區') == '813'
        assert self.dir_.find('大中一路') == '81362'
        assert self.dir_.find('大中二路') == '813'
        assert self.dir_.find('左營區大中一路') == '81362'
        assert self.dir_.find('左營區大中二路') == '813'

        assert self.dir_.find('小港區') == '812'
        assert self.dir_.find('豐街') == '81245'
        assert self.dir_.find('小港區豐街') == '81245'

        assert self.dir_.find('中正區') == ''

        assert self.dir_.find('大埔街') == ''
        assert self.dir_.find('台北市大埔街') == '10068'
        assert self.dir_.find('苗栗縣大埔街') == '36046'
