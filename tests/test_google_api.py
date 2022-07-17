from google_api import GMailMessage
from tests.data import bob_skipped_email, two_part_email

def test__dissect_message__no_parts():
    sut = GMailMessage(max_message_size='250', message_whitelist=["test_sender@gmail.com"])
    message_from, message_subject, message_text = sut._dissect_message(bob_skipped_email.email['payload'])
    assert message_from == 'test_sender@gmail.com'
    assert message_subject == 'RE: Info (1/1)'
    assert message_text == 'Really,\r\n\r\nSo there is no character limit for the sv kiki 95 address?\r\n\r\nReally...Hawaii to Samoa?\r\n\r\nTest Person\r\nTest Place, Test State 12345\r\ntest_sender@gmail.com\r\nH/O: 000-000-0000\r\nCell: 000-000-0000\r\n\r\n-----Original Message-----\r\nFrom: test_recipient@gmai.com [mailto:test_recipient@gmai.com] \r\nSent: Friday, June 10, 2022 7:54 PM\r\nTo: test_sender@gmail.com\r\nSubject: Info (1/1)\r\n\r\nCorrection on that last: from Hawaii to the Samoan islands\r\n\r\n\r\n-- \r\nThis email has been checked for viruses by AVG.\r\nhttps://www.avg.com\r\n\r\n'

def test__dissect_message__two_parts():
    sut = GMailMessage(max_message_size='250', message_whitelist=["test_sender@gmail.com"])
    message_from, message_subject, message_text = sut._dissect_message(two_part_email.email['payload'])
    assert message_from == "test_sender@gmail.com"
    assert message_subject == "full emails"
    assert message_text == "Yep, I've observed some pretty large emails going back and forth. I do\r\ndouble-check emails in cloudloop so if something gets lost I'll forward it,\r\nbut so far the new integration has not failed to deliver anything\r\n"