import responses

from veryfi import Client


MOCK = {
    "pdf_url": "https://scdn.veryfi.com/checks/919ba4778c039560/78535c60-e371-40fd-ae78-6d0c019b2c35/067e7057-e38b-4c32-9d87-720e0a8e232f.pdf?Expires=1730233783&Signature=fbR-arwLoH1YC8GVK52SvvilH59eHWIYp1o2WXw5UWr0s0CjKkrJ1Bx-PORKVzLbnJHOoYJDC4lU1iiqdq4~yDyz~-ygRHTNxyT9BJovFSzCBAc3Gnzv7uWMNIp-9mdV0QGk-Fu25eZfwd56Dfd2ZhG-EzreCRfh66r6338UF4EaHK5SG5b4i-NwkDaZ~qRZC6jNzYUJOGbXexYPbQxF5tMinc97ok~~fLQ--r0HWr7SvQyJisUqDnKS0DMTQujDz-7lStMJmvvlQX0jmpdcsq8DBIR6SnWZxHA7tM-ydD27Jt8l753X3uNtZuao61CeGSpQP09CnWlctTewm4IHKQ__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
    "id": 4662680,
    "external_id": None,
    "created_date": "2024-10-29 20:14:43",
    "updated_date": "2024-10-29 20:14:43",
    "img_thumbnail_url": "https://scdn.veryfi.com/checks/919ba4778c039560/78535c60-e371-40fd-ae78-6d0c019b2c35/thumbnail.jpg?Expires=1730233783&Signature=Sy8RUK0FLkeyhI3tpR8d60j-4BWyUH82D1frNU5FGGgGqumWWer6JgXbqM2eoHrgz04kwtKMwC-UZME0AZa-HtZr8j6a7TRO6M2uT0GoCHNQKv7rNcWUPajn4GsdU8VyY3b8KDx7WaGLd3VXP1TWAIqhW~DC07ZzjWbJ3K~8Ieyztt6Naijb~JbDFgUuIcNu8oikfoK3GAE8vzyElU5ctX4nmG1H-BEySCY-eIjf7GVwvaKjnZjab4h0Ox8SIdRyqVp~sj7dwlAtMlJmv6TxsNS14EDi91pxWPcvQlD7JCyQOH6brsgD0pkYVa4JFBF7yUTnGS4NXcCTiqkBhLh1Tw__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
    "text": "THIS DOCUMENT WAS PRINTED ON PAPER CONTAINING ULTRAVIOLET FIBERS AND AN ARTIFICIAL WATERMARK ON BACK\n\n\t70-2328/719 IL\nNationwide\nis on your side\t\t\tOctober 4, 2021\t\tCheck No. 118408359\nPO Box 2344\nBrea, CA 92822-2344\nPay: One Thousand Three Hundred Eight And 45/100 Dollars\t\t\t$1,308.45\n\nPay to the\tDmitry Birulia\nOrder of:\t733 Long Bridge\nSan Francisco CA 94158\n\n\tAUTHORIZED SIGNATURE\nMemo :F-602441-2021092406733\t\t\t\t\tVOID AFTER SIX MONTHS\n\n⑈0118408359⑈ ⑆031923284⑆ 8765129397⑈",
    "meta": {},
    "amount": 1308.45,
    "amount_text": "One Thousand Three Hundred Eight And 45/100 Dollars",
    "bank_address": "Brea, CA 92822-2344",
    "bank_name": None,
    "fractional_routing_number": "70-2328/719",
    "routing_from_fractional": "071923284",
    "check_number": "0118408359",
    "date": "2021-10-04",
    "memo": "F-602441-2021092406733",
    "payer_address": "PO Box 2344",
    "payer_name": None,
    "receiver_address": "733 Long Bridge\nSan Francisco CA 94158",
    "receiver_name": "Dmitry Birulia",
    "is_signed": True,
    "is_endorsed": None,
    "endorsement": {"is_signed": None, "is_mobile_or_remote_deposit_only": None},
    "micr": {
        "routing_number": "031923284",
        "account_number": "8765129397",
        "serial_number": None,
        "raw": "C0118408359C A031923284A 8765129397C",
    },
}


@responses.activate
def test_process_check_url():

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/checks/",
        json=MOCK,
        status=200,
    )
    d = client.process_check_url(
        file_url="http://cdn-dev.veryfi.com/testing/veryfi-python/receipt_public.jpg"
    )
    assert d == MOCK


@responses.activate
def test_process_check():

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/checks/",
        json=MOCK,
        status=200,
    )
    d = client.process_check(file_path="tests/assets/receipt_public.jpg")
    assert d == MOCK


@responses.activate
def test_get_checks():
    mock = [MOCK]

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.GET,
        f"{client.versioned_url}/partner/checks/",
        json=mock,
        status=200,
    )
    d = client.get_checks()
    assert d == mock
