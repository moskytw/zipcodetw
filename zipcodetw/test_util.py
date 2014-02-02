#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zipcodetw.util import Address

def test_address_tokenize():

    expected_tokens = ((u'', u'', u'臺北', u'市'), (u'', u'', u'大安', u'區'), (u'', u'', u'市府', u'路'), (u'1', u'', u'', u'號'))

    # standard
    assert Address(u'臺北市大安區市府路1號').tokens == expected_tokens
    # 8-bit string
    assert Address('臺北市大安區市府路1號').tokens == expected_tokens
    # with spaces and commas
    assert Address('臺北市,　大　安區，市府路 1 號').tokens == expected_tokens

def test_address_tokenize_subno():

    expected_tokens = ((u'', u'', u'臺北', u'市'), (u'', u'', u'大安', u'區'), (u'', u'', u'市府', u'路'), (u'1', u'1', u'', u'號'))

    # standard
    assert Address(u'臺北市大安區市府路1之1號').tokens == expected_tokens
    # 8-bit string
    assert Address('臺北市大安區市府路1之1號').tokens == expected_tokens
    # with spaces and commas
    assert Address('臺北市,　大　安區，市府路 1 之 1 號').tokens == expected_tokens
    # another type of subno
    assert Address(u'臺北市大安區市府路1-1號').tokens == expected_tokens

def test_address_compare():

    addr = Address('臺北市大安區市府路5號')

    # general
    assert Address('臺北市大安區市府路1號') < addr
    assert Address('臺北市大安區市府路5號') == addr
    assert Address('臺北市大安區市府路9號') > addr

    # with subno
    assert Address('臺北市大安區市府路4-9號') < addr
    assert Address('臺北市大安區市府路5-1號') > addr

def test_address_compare_subno():

    addr = Address('臺北市大安區市府路5-5號')

    # general
    assert Address('臺北市大安區市府路5-1號') < addr
    assert Address('臺北市大安區市府路5-5號') == addr
    assert Address('臺北市大安區市府路5-9號') > addr

    # without subno
    assert Address('臺北市大安區市府路1號') < addr
    assert Address('臺北市大安區市府路9號') > addr

from zipcodetw.util import AddressRule

def test_address_rule_rule_tokens():

    addr = AddressRule('臺北市,中正區,八德路１段,全')
    assert addr.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'八德', u'路'), (u'', u'', u'１', u'段'))
    assert addr.rule_tokens == (u'全', )

    addr = AddressRule('臺北市,中正區,三元街,單全')
    assert addr.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'三元', u'街'))
    assert addr.rule_tokens == (u'單', u'全')

    addr = AddressRule('臺北市,中正區,三元街,雙  48號以下')
    assert addr.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'三元', u'街'), (u'48', u'', u'', u'號'))
    assert addr.rule_tokens == (u'雙', u'以下')

    addr = AddressRule('臺北市,中正區,大埔街,單  15號以上')
    assert addr.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'大埔', u'街'), (u'15', u'', u'', u'號'))
    assert addr.rule_tokens == (u'單', u'以上')

    addr = AddressRule('臺北市,中正區,中華路１段,單  25之   3號以下')
    assert addr.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'中華', u'路'), (u'', u'', u'１', u'段'), (u'25', u'3', u'', u'號'))
    assert addr.rule_tokens == (u'單', u'以下')

    addr = AddressRule('臺北市,中正區,中華路１段,單  27號至  47號')
    assert addr.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'中華', u'路'), (u'', u'', u'１', u'段'), (u'27', u'', u'', u'號'), (u'47', u'', u'', u'號'))
    assert addr.rule_tokens == (u'單', u'至')

    addr = AddressRule('臺北市,中正區,仁愛路１段,連   2之   4號以上')
    assert addr.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'仁愛', u'路'), (u'', u'', u'１', u'段'), (u'2', u'4', u'', u'號'))
    assert addr.rule_tokens == (u'連', u'以上')

    addr = AddressRule('臺北市,中正區,杭州南路１段,　  14號含附號')
    assert addr.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'杭州南', u'路'), (u'', u'', u'１', u'段'), (u'14', u'', u'', u'號'))
    assert addr.rule_tokens == (u'含附號',)

    addr = AddressRule('臺北市,大同區,哈密街,　  47附號全')
    assert addr.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'大同', u'區'), (u'', u'', u'哈密', u'街'), (u'47', u'', u'', u'號'))
    assert addr.rule_tokens == (u'附號全',)

    addr = AddressRule('臺北市,大同區,哈密街,雙  68巷至  70號含附號全')
    assert addr.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'大同', u'區'), (u'', u'', u'哈密', u'街'), (u'68', u'', u'', u'巷'), (u'70', u'', u'', u'號'))
    assert addr.rule_tokens == (u'雙', u'至', u'含附號全')

    # NOTE: It was 普義 (without 里).
    addr = AddressRule('桃園縣,中壢市,普義里,連  49號含附號以下')
    assert addr.tokens == ((u'', u'', u'桃園', u'縣'), (u'', u'', u'中壢', u'市'), (u'', u'', u'普義', u'里'), (u'49', u'', u'', u'號'))
    assert addr.rule_tokens == (u'連', u'含附號以下')

    addr = AddressRule('臺中市,西屯區,西屯路３段西平南巷,　   1之   3號及以上附號')
    assert addr.tokens == ((u'', u'', u'臺中', u'市'), (u'', u'', u'西屯', u'區'), (u'', u'', u'西屯', u'路'), (u'', u'', u'３', u'段'), (u'', u'', u'西平南', u'巷'), (u'1', u'3', u'', u'號'))
    assert addr.rule_tokens == (u'及以上附號',)

def test_address_rule_rule_tokens_tricky_input():

    addr = AddressRule('新北市,中和區,連城路,雙 268之   1號以下')
    assert addr.tokens == ((u'', u'', u'新北', u'市'), (u'', u'', u'中和', u'區'), (u'', u'', u'連城', u'路'), (u'268', u'1', u'', u'號'))
    assert addr.rule_tokens == (u'雙', u'以下')

    addr = AddressRule('新北市,泰山區,全興路,全')
    assert addr.tokens == ((u'', u'', u'新北', u'市'), (u'', u'', u'泰山', u'區'), (u'', u'', u'全興', u'路'))
    assert addr.rule_tokens == (u'全',)

def test_address_rule_match():

    addr = Address(u'臺北市大安區市府路5號')

    # 全單雙
    assert     AddressRule(u'臺北市大安區市府路全').match(addr)
    assert     AddressRule(u'臺北市大安區市府路單全').match(addr)
    assert not AddressRule(u'臺北市大安區市府路雙全').match(addr)

    # 以上 & 以下
    assert not AddressRule(u'臺北市大安區市府路6號以上').match(addr)
    assert     AddressRule(u'臺北市大安區市府路6號以下').match(addr)
    assert     AddressRule(u'臺北市大安區市府路5號以上').match(addr)
    assert     AddressRule(u'臺北市大安區市府路5號').match(addr)
    assert     AddressRule(u'臺北市大安區市府路5號以下').match(addr)
    assert     AddressRule(u'臺北市大安區市府路4號以上').match(addr)
    assert not AddressRule(u'臺北市大安區市府路4號以下').match(addr)

    # 至
    assert not AddressRule(u'臺北市大安區市府路1號至4號').match(addr)
    assert     AddressRule(u'臺北市大安區市府路1號至5號').match(addr)
    assert     AddressRule(u'臺北市大安區市府路5號至9號').match(addr)
    assert not AddressRule(u'臺北市大安區市府路6號至9號').match(addr)

    # 附號
    assert not AddressRule(u'臺北市大安區市府路6號及以上附號').match(addr)
    assert     AddressRule(u'臺北市大安區市府路6號含附號以下').match(addr)
    assert     AddressRule(u'臺北市大安區市府路5號及以上附號').match(addr)
    assert     AddressRule(u'臺北市大安區市府路5號含附號').match(addr)
    assert not AddressRule(u'臺北市大安區市府路5附號全').match(addr)
    assert     AddressRule(u'臺北市大安區市府路5號含附號以下').match(addr)
    assert     AddressRule(u'臺北市大安區市府路4號及以上附號').match(addr)
    assert not AddressRule(u'臺北市大安區市府路4號含附號以下').match(addr)

    # 單雙 x 以上, 至, 以下
    assert     AddressRule(u'臺北市大安區市府路單5號以上').match(addr)
    assert not AddressRule(u'臺北市大安區市府路雙5號以上').match(addr)
    assert     AddressRule(u'臺北市大安區市府路單1號至5號').match(addr)
    assert not AddressRule(u'臺北市大安區市府路雙1號至5號').match(addr)
    assert     AddressRule(u'臺北市大安區市府路單5號至9號').match(addr)
    assert not AddressRule(u'臺北市大安區市府路雙5號至9號').match(addr)
    assert     AddressRule(u'臺北市大安區市府路單5號以下').match(addr)
    assert not AddressRule(u'臺北市大安區市府路雙5號以下').match(addr)

if __name__ == '__main__':
    import uniout
    test_address_rule_match()
