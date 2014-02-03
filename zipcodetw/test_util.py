#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zipcodetw.util import Address

def test_address_flat():

    tokens = Address.tokenize('臺北市大安區市府路1號')
    assert Address.flat(tokens, 1) == (u'臺北市', )
    assert Address.flat(tokens, 2) == (u'臺北市', u'大安區')
    assert Address.flat(tokens, 3) == (u'臺北市', u'大安區', u'市府路')
    assert Address.flat(tokens) == (u'臺北市', u'大安區', u'市府路', u'1號')

def test_address_init():

    expected_tokens = ((u'', u'', u'臺北', u'市'), (u'', u'', u'大安', u'區'), (u'', u'', u'市府', u'路'), (u'1', u'', u'', u'號'))

    # standard
    assert Address(u'臺北市大安區市府路1號').tokens == expected_tokens
    # 8-bit string
    assert Address('臺北市大安區市府路1號').tokens == expected_tokens
    # with spaces and commas
    assert Address('臺北市,　大　安區，市府路 1 號').tokens == expected_tokens

def test_address_init_subno():

    expected_tokens = ((u'', u'', u'臺北', u'市'), (u'', u'', u'大安', u'區'), (u'', u'', u'市府', u'路'), (u'1', u'1', u'', u'號'))

    # standard
    assert Address(u'臺北市大安區市府路1之1號').tokens == expected_tokens
    # 8-bit string
    assert Address('臺北市大安區市府路1之1號').tokens == expected_tokens
    # with spaces and commas
    assert Address('臺北市,　大　安區，市府路 1 之 1 號').tokens == expected_tokens
    # another type of subno
    assert Address(u'臺北市大安區市府路1-1號').tokens == expected_tokens

def test_address_repr():

    repr_str = "Address(tokens=((u'', u'', u'\u81fa\u5317', u'\u5e02'), (u'', u'', u'\u5927\u5b89', u'\u5340'), (u'', u'', u'\u5e02\u5e9c', u'\u8def'), (u'1', u'', u'', u'\u865f')), last_no_pair=(1, 0))"
    assert repr(Address('臺北市大安區市府路1號')) == repr_str
    assert repr(eval(repr_str)) == repr_str

from zipcodetw.util import Rule

def test_rule_init():

    rule = Rule('臺北市,中正區,八德路１段,全')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'八德', u'路'), (u'', u'', u'１', u'段'))
    assert rule.rule_tokens == (u'全', )

    rule = Rule('臺北市,中正區,三元街,單全')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'三元', u'街'))
    assert rule.rule_tokens == (u'單', u'全')

    rule = Rule('臺北市,中正區,三元街,雙  48號以下')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'三元', u'街'), (u'48', u'', u'', u'號'))
    assert rule.rule_tokens == (u'雙', u'以下')

    rule = Rule('臺北市,中正區,大埔街,單  15號以上')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'大埔', u'街'), (u'15', u'', u'', u'號'))
    assert rule.rule_tokens == (u'單', u'以上')

    rule = Rule('臺北市,中正區,中華路１段,單  25之   3號以下')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'中華', u'路'), (u'', u'', u'１', u'段'), (u'25', u'3', u'', u'號'))
    assert rule.rule_tokens == (u'單', u'以下')

    rule = Rule('臺北市,中正區,中華路１段,單  27號至  47號')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'中華', u'路'), (u'', u'', u'１', u'段'), (u'27', u'', u'', u'號'), (u'47', u'', u'', u'號'))
    assert rule.rule_tokens == (u'單', u'至')

    rule = Rule('臺北市,中正區,仁愛路１段,連   2之   4號以上')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'仁愛', u'路'), (u'', u'', u'１', u'段'), (u'2', u'4', u'', u'號'))
    assert rule.rule_tokens == (u'連', u'以上')

    rule = Rule('臺北市,中正區,杭州南路１段,　  14號含附號')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'杭州南', u'路'), (u'', u'', u'１', u'段'), (u'14', u'', u'', u'號'))
    assert rule.rule_tokens == (u'含附號',)

    rule = Rule('臺北市,大同區,哈密街,　  47附號全')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'大同', u'區'), (u'', u'', u'哈密', u'街'), (u'47', u'', u'', u'號'))
    assert rule.rule_tokens == (u'附號全',)

    rule = Rule('臺北市,大同區,哈密街,雙  68巷至  70號含附號全')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'大同', u'區'), (u'', u'', u'哈密', u'街'), (u'68', u'', u'', u'巷'), (u'70', u'', u'', u'號'))
    assert rule.rule_tokens == (u'雙', u'至', u'含附號全')

    rule = Rule('桃園縣,中壢市,普義,連  49號含附號以下')
    assert rule.tokens == ((u'', u'', u'桃園', u'縣'), (u'', u'', u'中壢', u'市'), (u'', u'', u'普義', u''), (u'49', u'', u'', u'號'))
    assert rule.rule_tokens == (u'連', u'含附號以下')

    rule = Rule('臺中市,西屯區,西屯路３段西平南巷,　   1之   3號及以上附號')
    assert rule.tokens == ((u'', u'', u'臺中', u'市'), (u'', u'', u'西屯', u'區'), (u'', u'', u'西屯', u'路'), (u'', u'', u'３', u'段'), (u'', u'', u'西平南', u'巷'), (u'1', u'3', u'', u'號'))
    assert rule.rule_tokens == (u'及以上附號',)

def test_rule_init_tricky_input():

    rule = Rule('新北市,中和區,連城路,雙 268之   1號以下')
    assert rule.tokens == ((u'', u'', u'新北', u'市'), (u'', u'', u'中和', u'區'), (u'', u'', u'連城', u'路'), (u'268', u'1', u'', u'號'))
    assert rule.rule_tokens == (u'雙', u'以下')

    rule = Rule('新北市,泰山區,全興路,全')
    assert rule.tokens == ((u'', u'', u'新北', u'市'), (u'', u'', u'泰山', u'區'), (u'', u'', u'全興', u'路'))
    assert rule.rule_tokens == (u'全',)

def test_rule_repr():

    repr_str = "Rule(tokens=((u'', u'', u'\u81fa\u5317', u'\u5e02'), (u'', u'', u'\u5927\u5b89', u'\u5340'), (u'', u'', u'\u5e02\u5e9c', u'\u8def'), (u'1', u'', u'', u'\u865f')), last_no_pair=(1, 0), rule_tokens=(u'\u4ee5\u4e0a',))"
    assert repr(Rule('臺北市大安區市府路1號以上')) == repr_str
    assert repr(eval(repr_str)) == repr_str

def test_rule_match():

    addr = Address(u'臺北市大安區市府路5號')

    # 全單雙
    assert     Rule(u'臺北市大安區市府路全').match(addr)
    assert     Rule(u'臺北市大安區市府路單全').match(addr)
    assert not Rule(u'臺北市大安區市府路雙全').match(addr)

    # 以上 & 以下
    assert not Rule(u'臺北市大安區市府路6號以上').match(addr)
    assert     Rule(u'臺北市大安區市府路6號以下').match(addr)
    assert     Rule(u'臺北市大安區市府路5號以上').match(addr)
    assert     Rule(u'臺北市大安區市府路5號').match(addr)
    assert     Rule(u'臺北市大安區市府路5號以下').match(addr)
    assert     Rule(u'臺北市大安區市府路4號以上').match(addr)
    assert not Rule(u'臺北市大安區市府路4號以下').match(addr)

    # 至
    assert not Rule(u'臺北市大安區市府路1號至4號').match(addr)
    assert     Rule(u'臺北市大安區市府路1號至5號').match(addr)
    assert     Rule(u'臺北市大安區市府路5號至9號').match(addr)
    assert not Rule(u'臺北市大安區市府路6號至9號').match(addr)

    # 附號
    assert not Rule(u'臺北市大安區市府路6號及以上附號').match(addr)
    assert     Rule(u'臺北市大安區市府路6號含附號以下').match(addr)
    assert     Rule(u'臺北市大安區市府路5號及以上附號').match(addr)
    assert     Rule(u'臺北市大安區市府路5號含附號').match(addr)
    assert not Rule(u'臺北市大安區市府路5附號全').match(addr)
    assert     Rule(u'臺北市大安區市府路5號含附號以下').match(addr)
    assert     Rule(u'臺北市大安區市府路4號及以上附號').match(addr)
    assert not Rule(u'臺北市大安區市府路4號含附號以下').match(addr)

    # 單雙 x 以上, 至, 以下
    assert     Rule(u'臺北市大安區市府路單5號以上').match(addr)
    assert not Rule(u'臺北市大安區市府路雙5號以上').match(addr)
    assert     Rule(u'臺北市大安區市府路單1號至5號').match(addr)
    assert not Rule(u'臺北市大安區市府路雙1號至5號').match(addr)
    assert     Rule(u'臺北市大安區市府路單5號至9號').match(addr)
    assert not Rule(u'臺北市大安區市府路雙5號至9號').match(addr)
    assert     Rule(u'臺北市大安區市府路單5號以下').match(addr)
    assert not Rule(u'臺北市大安區市府路雙5號以下').match(addr)

def test_rule_match_without_detail():

    addr = Address(u'臺北市大安區市府路5號')

    # 全單雙
    assert     Rule(u'全').match(addr)
    assert     Rule(u'單全').match(addr)
    assert not Rule(u'雙全').match(addr)

    # 以上 & 以下
    assert not Rule(u'6號以上').match(addr)
    assert     Rule(u'6號以下').match(addr)
    assert     Rule(u'5號以上').match(addr)
    assert     Rule(u'5號').match(addr)
    assert     Rule(u'5號以下').match(addr)
    assert     Rule(u'4號以上').match(addr)
    assert not Rule(u'4號以下').match(addr)

    # 至
    assert not Rule(u'1號至4號').match(addr)
    assert     Rule(u'1號至5號').match(addr)
    assert     Rule(u'5號至9號').match(addr)
    assert not Rule(u'6號至9號').match(addr)

    # 附號
    assert not Rule(u'6號及以上附號').match(addr)
    assert     Rule(u'6號含附號以下').match(addr)
    assert     Rule(u'5號及以上附號').match(addr)
    assert     Rule(u'5號含附號').match(addr)
    assert not Rule(u'5附號全').match(addr)
    assert     Rule(u'5號含附號以下').match(addr)
    assert     Rule(u'4號及以上附號').match(addr)
    assert not Rule(u'4號含附號以下').match(addr)

    # 單雙 x 以上, 至, 以下
    assert     Rule(u'單5號以上').match(addr)
    assert not Rule(u'雙5號以上').match(addr)
    assert     Rule(u'單1號至5號').match(addr)
    assert not Rule(u'雙1號至5號').match(addr)
    assert     Rule(u'單5號至9號').match(addr)
    assert not Rule(u'雙5號至9號').match(addr)
    assert     Rule(u'單5號以下').match(addr)
    assert not Rule(u'雙5號以下').match(addr)

def test_rule_match_short_target():

    rule = Rule('臺北市中正區丹陽街全')
    assert not rule.match(Address('臺北市'))
    assert not rule.match(Address('臺北市中正區'))
    assert not rule.match(Address('臺北市中正區仁愛路１段'))
    assert not rule.match(Address('臺北市中正區仁愛路１段1號'))

def test_rule_match_rule_all():

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

from zipcodetw.util import Directory

class TestDirectory(object):

    def setup(self):

        chp_csv_lines = '''郵遞區號,縣市名稱,鄉鎮市區,原始路名,投遞範圍
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
10063,臺北市,中正區,仁愛路２段,雙  66號以上'''.split('\n')

        self.dir_ = Directory()
        self.dir_.load_chp_csv(chp_csv_lines)

    def test_find(self):

        assert self.dir_.find_zipcodes('臺北市') == ['10058', '10079', '10070', '10079', '10068', '10068', '10051', '10041', '10051', '10041', '10002', '10051', '10048', '10001', '10043', '10042', '10010', '10042', '10065', '10066', '10068', '10069', '10067', '10072', '10055', '10051', '10052', '10055', '10060', '10056', '10056', '10062', '10063']
        assert self.dir_.find_zipcodes('臺北市中正區') == ['10058', '10079', '10070', '10079', '10068', '10068', '10051', '10041', '10051', '10041', '10002', '10051', '10048', '10001', '10043', '10042', '10010', '10042', '10065', '10066', '10068', '10069', '10067', '10072', '10055', '10051', '10052', '10055', '10060', '10056', '10056', '10062', '10063']
        assert self.dir_.find_zipcodes('臺北市中正區仁愛路１段') == ['10051', '10052']
        assert self.dir_.find_zipcodes('臺北市中正區仁愛路１段1號') == ['10051']

    def test_fuzzy_find(self):

        assert self.dir_.find('臺北市') == '100'
        assert self.dir_.find('臺北市中正區') == '100'
        assert self.dir_.find('臺北市中正區仁愛路１段') == '1005'
        assert self.dir_.find('臺北市中正區仁愛路１段1號') == '10051'

if __name__ == '__main__':
    import uniout
    test_dir = TestDirectory()
    test_dir.setup()
    test_dir.test_find()
    test_dir.test_fuzzy_find()
