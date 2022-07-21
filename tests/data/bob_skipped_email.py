email = {
  "id": "181502aef9236df7",
  "threadId": "1815009a26004478",
  "labelIds": [
    "IMPORTANT",
    "CATEGORY_PERSONAL",
    "INBOX"
  ],
  "snippet": "Really, So there is no character limit for the sv kiki 95 address? Really...Hawaii to Samoa? Test Person Test Place, Test State, 12345 test_sender@gmail.com H/O: 000-000-0000 Cell: 000-000-0000 -----Original",
  "payload": {
    "partId": "",
    "mimeType": "text/plain",
    "filename": "",
    "headers": [
      {
        "name": "Delivered-To",
        "value": "test_recipient@gmail.com"
      },
      {
        "name": "Received",
        "value": "by 2002:a05:7000:db08:0:0:0:0 with SMTP id ks8csp39041mab;        Fri, 10 Jun 2022 17:30:00 -0700 (PDT)"
      },
      {
        "name": "X-Received",
        "value": "by 2002:a05:622a:44c:b0:304:e4a2:3db7 with SMTP id o12-20020a05622a044c00b00304e4a23db7mr29486546qtx.162.1654907399988;        Fri, 10 Jun 2022 17:29:59 -0700 (PDT)"
      },
      {
        "name": "ARC-Seal",
        "value": "i=1; a=rsa-sha256; t=1654907399; cv=none;        d=google.com; s=arc-20160816;        b=hzOI9ldUux6l8CQDfT5pCiqjlnfuWHb0dh5K4170O2yet3OYa4jxjj6Yrv1w1h8buU         O5vfxPcu2b9kZAt+01TGQFDT/h+7ygczmkUf/kbxOD+ZFOvEPCT2SS347LaOhUKqRzbE         8Po6lfOtLxFcAakNXHJ5/sKWnNo/4KaLLXkufIB1QT7589l+h43ac0NB4dO9pcJCQNbL         yVdD8cUTAQQLojo5ocoPixCJDPKB5xoXVEJyD9HFtcxrB7sIIxJ155Mi1auKZ7Gu7X4s         CrFAsKETzVYiS6XTLNS3+G+wAxZmLi9SyJcFbP3DGZClFfbrmJs8sZqBdI/y6ZNALbic         znSQ=="
      },
      {
        "name": "ARC-Message-Signature",
        "value": "i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;        h=content-language:thread-index:content-transfer-encoding         :mime-version:message-id:date:subject:in-reply-to:references:to:from         :dkim-signature;        bh=4qlKLHMkKZ4/60UJOHQebjWj5wHynJ0y3g1L0g95Ozw=;        b=GMG/V0TQXsN1bsQ6qkFqYDLQMeoSQaVWhKg6D7bTywjy0g2zy7IG4m20Mvk00C7zTz         Lx3Ta9kPoOjVtpelzWFTvPxPaV9tumCdE3pRB+FOUS7GEZ1MnsDcnVIBTnAXQ4sj1Hj4         ErlSv6WP0sEzEBdc84aTEgUoFxDHrwkOc31fuYbC5Xbcc01tQbM8mWs8/kquZM7ixZ5M         j4MWgO2TLHNXt/WzWMK6BzG0Hc5FrHdkKdcB/EKtHMhQqVSRGhFEXI/8Q5Ss+YzGBBHD         OTkgNrzS3+OtPlSGG43Y3cQ+s9f5CYh8NrxA2qFpmlJqDRJdSlAawnb48NTEEtlUa8gk         WC5A=="
      },
      {
        "name": "ARC-Authentication-Results",
        "value": "i=1; mx.google.com;       dkim=pass header.i=@gmail.com header.s=20210112 header.b=DowLJzEA;       spf=pass (google.com: domain of test_sender@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=test_sender@gmail.com;       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com"
      },
      {
        "name": "Return-Path",
        "value": "\u003ctest_sender@gmail.com\u003e"
      },
      {
        "name": "Received",
        "value": "from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])        by mx.google.com with SMTPS id j22-20020ae9c216000000b006a6790893cesor254360qkg.114.2022.06.10.17.29.59        for \u003ctest_recipient@gmail.com\u003e        (Google Transport Security);        Fri, 10 Jun 2022 17:29:59 -0700 (PDT)"
      },
      {
        "name": "Received-SPF",
        "value": "pass (google.com: domain of test_sender@gmail.com designates 209.85.220.41 as permitted sender) client-ip=209.85.220.41;"
      },
      {
        "name": "Authentication-Results",
        "value": "mx.google.com;       dkim=pass header.i=@gmail.com header.s=20210112 header.b=DowLJzEA;       spf=pass (google.com: domain of test_sender@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=test_sender@gmail.com;       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com"
      },
      {
        "name": "DKIM-Signature",
        "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=gmail.com; s=20210112;        h=from:to:references:in-reply-to:subject:date:message-id:mime-version         :content-transfer-encoding:thread-index:content-language;        bh=4qlKLHMkKZ4/60UJOHQebjWj5wHynJ0y3g1L0g95Ozw=;        b=DowLJzEARWfMGiGqIvmc9BpMTWiJz8ZT76VHkfkh+xrHCyhIylOIGSnfl+2zIXtwFe         2Q1G+eHbRcKCYlTHzUCUfXenMIQfpO8EYP0q+OZvcnYSDzhyMz7Le74A3ub2F9RFECDj         mSrRqF4sDGY+ArfI/vVVtfYPbcFCLrH9vpRq7zNrj/QAZItXXlIN+De3L0WTGluZE+wV         t+zXNbOlornpR5v3+0OCavhJ7LFrp8F0O7GJqUccNAkAnF8HeGGoO6MP3RVwcJXh1d3L         Nj7QF/ylIQY/AGeiL0CJkXGmuj8Cx78SWGZZ24786/JlO2B5P2iPhPMJ0lgLLkSYIUEN         jE1g=="
      },
      {
        "name": "X-Google-DKIM-Signature",
        "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=1e100.net; s=20210112;        h=x-gm-message-state:from:to:references:in-reply-to:subject:date         :message-id:mime-version:content-transfer-encoding:thread-index         :content-language;        bh=4qlKLHMkKZ4/60UJOHQebjWj5wHynJ0y3g1L0g95Ozw=;        b=nNEVLMvgi7zC3UkmQD1woFHVtk9BK8gvc+J8fb1zDDAlFXO5oyBJ45i1/T5d+FuI0C         Fs+07HZWJ0yNY6SwNtgVQw2ajbR0hjJoAzw+z5GMes/vlP/PTaIi/gRUL3BhOehXyEGi         J8U8Dh49DUn6vxg938lAC8kO/C+5BI1Fm2E8RwTDzZejOVXpS227lFJgQZhE+bQ7OdpM         tjlXihCxEwm5niDzgNPCu4FAA+WiRcnWiabsGYT2U4Y9W1vZUSD+q0jfJpiJ8mnpLkc3         dBz3pkV/MOp0Wn2sswiW/unSo6lPGQ5GQ/QTBVPA1ZBqR+OumPkMGMiutVriSe2sImwF         2Dng=="
      },
      {
        "name": "X-Gm-Message-State",
        "value": "AOAM5329DODmTlzhnXAA5VwKc72Vv3TIOCIYzpfSHiKBAGc62V8SUfCe ntJEhH9UquoeBP08HHVEEwIX1qFeOsA="
      },
      {
        "name": "X-Google-Smtp-Source",
        "value": "ABdhPJxrb856mvTwri2AG7El1B5DItWqw82+QtveTBlSgkE2/d9OVdZF/hWCNd4LSOO2trUBq/RA5w=="
      },
      {
        "name": "X-Received",
        "value": "by 2002:a05:620a:150b:b0:6a6:b079:4e40 with SMTP id i11-20020a05620a150b00b006a6b0794e40mr23007842qkk.184.1654907399190;        Fri, 10 Jun 2022 17:29:59 -0700 (PDT)"
      },
      {
        "name": "Return-Path",
        "value": "\u003ctest_sender@gmail.com\u003e"
      },
      {
        "name": "Received",
        "value": "from DESKTOP1SKUTBN ([5.62.49.88])        by smtp.gmail.com with ESMTPSA id c1-20020ac87d81000000b0030522a969e0sm427386qtd.60.2022.06.10.17.29.58        for \u003ctest_recipient@gmail.com\u003e        (version=TLS1_2 cipher=ECDHE-ECDSA-AES128-GCM-SHA256 bits=128/128);        Fri, 10 Jun 2022 17:29:58 -0700 (PDT)"
      },
      {
        "name": "From",
        "value": "Test Person \u003ctest_sender@gmail.com\u003e"
      },
      {
        "name": "To",
        "value": "\u003ctest_recipient@gmail.com\u003e"
      },
      {
        "name": "References",
        "value": "\u003cCAEVsuXW9ehyDdJOWJ91J3qFoLDmpahJvCs8h6N8nzgiAKyvgWw@mail.gmail.com\u003e"
      },
      {
        "name": "In-Reply-To",
        "value": "\u003cCAEVsuXW9ehyDdJOWJ91J3qFoLDmpahJvCs8h6N8nzgiAKyvgWw@mail.gmail.com\u003e"
      },
      {
        "name": "Subject",
        "value": "RE: Info (1/1)"
      },
      {
        "name": "Date",
        "value": "Fri, 10 Jun 2022 20:29:57 -0400"
      },
      {
        "name": "Message-ID",
        "value": "\u003c016a01d87d2a$61912430$24b36c90$@gmail.com\u003e"
      },
      {
        "name": "MIME-Version",
        "value": "1.0"
      },
      {
        "name": "Content-Type",
        "value": "text/plain; charset=\"utf-8\""
      },
      {
        "name": "Content-Transfer-Encoding",
        "value": "7bit"
      },
      {
        "name": "X-Mailer",
        "value": "Microsoft Outlook 14.0"
      },
      {
        "name": "Thread-Index",
        "value": "AQKv4ED6dovhUtA2+/dshqzVBgmwZ6uak3nA"
      },
      {
        "name": "Content-Language",
        "value": "en-us"
      },
      {
        "name": "X-Antivirus",
        "value": "AVG (VPS 220610-4, 6/10/2022), Outbound message"
      },
      {
        "name": "X-Antivirus-Status",
        "value": "Clean"
      }
    ],
    "body": {
      "size": 520,
      "data": "UmVhbGx5LA0KDQpTbyB0aGVyZSBpcyBubyBjaGFyYWN0ZXIgbGltaXQgZm9yIHRoZSBzdiBraWtpIDk1IGFkZHJlc3M_DQoNClJlYWxseS4uLkhhd2FpaSB0byBTYW1vYT8NCg0KVGVzdCBQZXJzb24NClRlc3QgUGxhY2UsIFRlc3QgU3RhdGUgMTIzNDUNCnRlc3Rfc2VuZGVyQGdtYWlsLmNvbQ0KSC9POiAwMDAtMDAwLTAwMDANCkNlbGw6IDAwMC0wMDAtMDAwMA0KDQotLS0tLU9yaWdpbmFsIE1lc3NhZ2UtLS0tLQ0KRnJvbTogdGVzdF9yZWNpcGllbnRAZ21haS5jb20gW21haWx0bzp0ZXN0X3JlY2lwaWVudEBnbWFpLmNvbV0gDQpTZW50OiBGcmlkYXksIEp1bmUgMTAsIDIwMjIgNzo1NCBQTQ0KVG86IHRlc3Rfc2VuZGVyQGdtYWlsLmNvbQ0KU3ViamVjdDogSW5mbyAoMS8xKQ0KDQpDb3JyZWN0aW9uIG9uIHRoYXQgbGFzdDogZnJvbSBIYXdhaWkgdG8gdGhlIFNhbW9hbiBpc2xhbmRzDQoNCg0KLS0gDQpUaGlzIGVtYWlsIGhhcyBiZWVuIGNoZWNrZWQgZm9yIHZpcnVzZXMgYnkgQVZHLg0KaHR0cHM6Ly93d3cuYXZnLmNvbQ0KDQo="
    }
  },
  "sizeEstimate": 6115,
  "historyId": "5154",
  "internalDate": "1654907397000"
}
