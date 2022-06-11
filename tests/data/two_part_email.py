email = {
  "id": "1814fe9b54831013",
  "threadId": "1814fe9b54831013",
  "labelIds": [
    "UNREAD",
    "CATEGORY_PERSONAL",
    "INBOX"
  ],
  "snippet": "Yep, I&#39;ve observed some pretty large emails going back and forth. I do double-check emails in cloudloop so if something gets lost I&#39;ll forward it, but so far the new integration has not failed",
  "payload": {
    "partId": "",
    "mimeType": "multipart/alternative",
    "filename": "",
    "headers": [
      {
        "name": "Delivered-To",
        "value": "test_recipient@gmail.com"
      },
      {
        "name": "Received",
        "value": "by 2002:a05:7000:db08:0:0:0:0 with SMTP id ks8csp7180mab;        Fri, 10 Jun 2022 16:18:45 -0700 (PDT)"
      },
      {
        "name": "X-Received",
        "value": "by 2002:a17:90b:3a87:b0:1e8:789d:c60 with SMTP id om7-20020a17090b3a8700b001e8789d0c60mr2071504pjb.77.1654903125077;        Fri, 10 Jun 2022 16:18:45 -0700 (PDT)"
      },
      {
        "name": "ARC-Seal",
        "value": "i=1; a=rsa-sha256; t=1654903125; cv=none;        d=google.com; s=arc-20160816;        b=UBgzh9FEvxt9GeOgL+10A1A53XPUK5P7AGGvI7/TSiKvBxGZN/InzUUjpaIwkJ6aYz         OWqJzOoQuLq+cplqRZAzpqnqzWbG7pmkb1hmFyrXdUNPKAp2sg33YRKEXoBWTJzO7Fhg         J4bwcHjWyF1Smo1pqmHRf6G5QPGA6aIDd3pyU7m/73lntdOVwUAls0qdAQ7zAZ6r491Y         PqalEWTLa+RIn2ECpEp7W5xnrzNcQgFgW1YCa4ZlLV0EkouZHcauucYm6nadVHpqTn0z         QD+OoKXuS+3U43dF2lIi4hPrZDiz+GJx4n9V5/0kfSfDD9wX9Mjtnot6nJQZoMlurTz3         IdFg=="
      },
      {
        "name": "ARC-Message-Signature",
        "value": "i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;        h=to:subject:message-id:date:from:mime-version:dkim-signature;        bh=c+h3XXm68+ZnovxdsAZGUOmcH/Gha1lZw3gIDwqIn78=;        b=JKuJGnuSGoZGlE0BHt+ed5ts9K5TIT0PlvozR0z+VJ4uvSF+kojE2MBLn0Nd0S92gk         9qCUsIPtGwzu4Gq8GBiuSHofqW5b/H16MOhP/VQ3me2A32qtss0l6htzGV52313QA5je         0ssVo726IhL/3Ob4u8lsdG/xOoFJcK7P6K0HiqEHfP4lvhGHd91MkFsaZM8BHiBKXGNM         BIIWapDGT7XxcJqcw+fhEgyLwyCr/FAloTBNTP6x+OUMJwiVxM1xUz8Ejk9CbbDvJfwM         axduKAuzud3Q0mQA/FlUc6TLWy/JEbmk7uLrpwDr1OlXsFYGCp5+ICgt1eOdHlnQKnYs         TN5w=="
      },
      {
        "name": "ARC-Authentication-Results",
        "value": "i=1; mx.google.com;       dkim=pass header.i=@gmail.com header.s=20210112 header.b=TBXj9n1h;       spf=pass (google.com: domain of test_sender@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=test_sender@gmail.com;       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com"
      },
      {
        "name": "Return-Path",
        "value": "\u003ctest_sender@gmail.com\u003e"
      },
      {
        "name": "Received",
        "value": "from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])        by mx.google.com with SMTPS id o19-20020a170903009300b0016253fae10fsor219369pld.190.2022.06.10.16.18.44        for \u003ctest_recipient@gmail.com\u003e        (Google Transport Security);        Fri, 10 Jun 2022 16:18:45 -0700 (PDT)"
      },
      {
        "name": "Received-SPF",
        "value": "pass (google.com: domain of test_sender@gmail.com designates 209.85.220.41 as permitted sender) client-ip=209.85.220.41;"
      },
      {
        "name": "Authentication-Results",
        "value": "mx.google.com;       dkim=pass header.i=@gmail.com header.s=20210112 header.b=TBXj9n1h;       spf=pass (google.com: domain of test_sender@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=test_sender@gmail.com;       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com"
      },
      {
        "name": "DKIM-Signature",
        "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=gmail.com; s=20210112;        h=mime-version:from:date:message-id:subject:to;        bh=c+h3XXm68+ZnovxdsAZGUOmcH/Gha1lZw3gIDwqIn78=;        b=TBXj9n1hvwP2YH/CRVj4pLKd4R9PlbmgD7UCqTkLECvn0cFCl+3ux1CCRTvmx0xqEJ         C5H1I+3AFix1YViAOv4QQt6zAO2NVHxXX1aznb73rb/v/nHI8oFzfXfllo98fGZozwID         AFKyAvXmLa8H2h6Nq5F09Nts/K4GrrCoOSh/CkK99BT9nx2K7NsxYfpsAxpoGbaSJMeP         dWkFzwhXUOnw4DDtBhvwrr9FUF+n+ni25XXAu1fjQxp2/cxeI+yOZ3E3OlkwovOio9ZJ         w2TgsHF8/MdsXDXLDwE97fNDTLFZwTUOnxGwjg3wbNDo7zMZj1G29aBooGuCND9tPiJU         6Atg=="
      },
      {
        "name": "X-Google-DKIM-Signature",
        "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=1e100.net; s=20210112;        h=x-gm-message-state:mime-version:from:date:message-id:subject:to;        bh=c+h3XXm68+ZnovxdsAZGUOmcH/Gha1lZw3gIDwqIn78=;        b=aEHrlSTZGv2+iDv0mKfy6Tc7rVEc0VNUaxGse2xicKbkigdVQkfhp2Vh0E2Y0tVVRv         ysrk5bjlT7WYlWZiiRmhKp94f3WqsrDDnAT31U4326qwbGYAWwChd3kRvWXwBuU+/p0k         qJsCa7Jg1ew7AXpWlajfVmOVbQhlMs2qTGHzzEbv9i4/ey6sZgoXX7GL8ekcgZSZnDt5         ore1NcrbMis7yEygSDsQ5Ocl7mNk+Ief64KxYfJ3iEVmOUYzh4rl9u2EF/AacMV3nESN         +aj1m4BNerKmJ4Qme0IzF0XZO183kOHt2KKpf/MAfzwvIqITWA37SNkB3FqTfpvtGpAR         lSIQ=="
      },
      {
        "name": "X-Gm-Message-State",
        "value": "AOAM532Qi9tWJkzJlSmNBVotE1KlK3xo2P0DZn6J2XrnnhV9d2VUa4xT UrBDKsKp0CZlogmP2vvBmsGGQj25vaVWy53frtn1oLe4AjA="
      },
      {
        "name": "X-Google-Smtp-Source",
        "value": "ABdhPJw9o3KRdMvTy21WdTqkjj7dyBTumfm1epuT0xlpSGOeZlcIDBGznVltuTPhsZhlB5lKBu7Btci1MuhPV54G4kw="
      },
      {
        "name": "X-Received",
        "value": "by 2002:a17:902:bd83:b0:167:8dd5:6a5a with SMTP id q3-20020a170902bd8300b001678dd56a5amr23932115pls.114.1654903123934; Fri, 10 Jun 2022 16:18:43 -0700 (PDT)"
      },
      {
        "name": "MIME-Version",
        "value": "1.0"
      },
      {
        "name": "From",
        "value": "Peter Dowdy \u003ctest_sender@gmail.com\u003e"
      },
      {
        "name": "Date",
        "value": "Fri, 10 Jun 2022 16:18:32 -0700"
      },
      {
        "name": "Message-ID",
        "value": "\u003cCAMBVeGgUHji=P-5Pv5YGMUkKX_ORRhFrV0wo_LzTeVOEhxXBMA@mail.gmail.com\u003e"
      },
      {
        "name": "Subject",
        "value": "full emails"
      },
      {
        "name": "To",
        "value": "test_recipient@gmail.com"
      },
      {
        "name": "Content-Type",
        "value": "multipart/alternative; boundary=\"000000000000d7030405e12028ca\""
      }
    ],
    "body": {
      "size": 0
    },
    "parts": [
      {
        "partId": "0",
        "mimeType": "text/plain",
        "filename": "",
        "headers": [
          {
            "name": "Content-Type",
            "value": "text/plain; charset=\"UTF-8\""
          }
        ],
        "body": {
          "size": 216,
          "data": "WWVwLCBJJ3ZlIG9ic2VydmVkIHNvbWUgcHJldHR5IGxhcmdlIGVtYWlscyBnb2luZyBiYWNrIGFuZCBmb3J0aC4gSSBkbw0KZG91YmxlLWNoZWNrIGVtYWlscyBpbiBjbG91ZGxvb3Agc28gaWYgc29tZXRoaW5nIGdldHMgbG9zdCBJJ2xsIGZvcndhcmQgaXQsDQpidXQgc28gZmFyIHRoZSBuZXcgaW50ZWdyYXRpb24gaGFzIG5vdCBmYWlsZWQgdG8gZGVsaXZlciBhbnl0aGluZw0K"
        }
      },
      {
        "partId": "1",
        "mimeType": "text/html",
        "filename": "",
        "headers": [
          {
            "name": "Content-Type",
            "value": "text/html; charset=\"UTF-8\""
          }
        ],
        "body": {
          "size": 243,
          "data": "PGRpdiBkaXI9Imx0ciI-WWVwLCBJJiMzOTt2ZSBvYnNlcnZlZCBzb21lIHByZXR0eSBsYXJnZSBlbWFpbHMgZ29pbmcgYmFjayBhbmQgZm9ydGguIEkgZG8gZG91YmxlLWNoZWNrIGVtYWlscyBpbiBjbG91ZGxvb3Agc28gaWYgc29tZXRoaW5nIGdldHMgbG9zdCBJJiMzOTtsbCBmb3J3YXJkIGl0LCBidXQgc28gZmFyIHRoZSBuZXcgaW50ZWdyYXRpb24gaGFzIG5vdCBmYWlsZWQgdG8gZGVsaXZlciBhbnl0aGluZzwvZGl2Pg0K"
        }
      }
    ]
  },
  "sizeEstimate": 5275,
  "historyId": "4885",
  "internalDate": "1654903112000"
}
