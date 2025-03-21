import responses

from veryfi import Client


MOCK = {
    "pdf_url": "https://scdn.veryfi.com/w8s/919ba4778c039560/64ea51e9-4293-4a0e-99a6-8c3cd0a4f7ab/8468d271-2943-46e7-b9a2-3dd0372d3648.pdf?Expires=1730234368&Signature=e1bOil~yK4P4uKYLxX1NPfHA3PxiTxd-Ds4HVnjNXxY22D-ng2NGJQQrWAst5E0ionsdkkFPc7mKy0fp6MkmwnZF~I-j8e1P9fhbI-T-0NhiDji4gp6xt4~vm-i9MG34K~Xa3TWPA~kMbQ~Hj2gjiMMniXsH6HeqH99yfl-Vt2ZWEMdWl3~ZlMWEpnPVIzDXdDBc~uRYCOS0KiLD2pfNAORYwp1ayNiuhiJzucJPAfRuK00y0BoUEPBmBS-aLa62VhNYVKmUPtVNobS2MjcGcnqnBhOZlbw0B5VTLNqrSIgKSVy6I6Co4zAwLjgviQyoPArVtgmJR8UNdFRk9LuDqw__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
    "id": 4662698,
    "external_id": None,
    "created_date": "2024-10-29 20:24:28",
    "updated_date": "2024-10-29 20:24:28",
    "img_thumbnail_url": "https://scdn.veryfi.com/w8s/919ba4778c039560/64ea51e9-4293-4a0e-99a6-8c3cd0a4f7ab/thumbnail.jpg?Expires=1730234368&Signature=ch2MJSewRZV3LkSlMVKMK1~BXsUiO~wNT5bSllXXv1N85jGIqsJHYTkrTaL1fXSZERLXBC6DFIzOcgSYB~zPu3r3nzr7v2Q-WBc~jk8tSxRWGg4eYLkwW34h-RwhckXuiH6UCo6Q01SF6P4RAt9~YL4mIXOLmeahsjFQ-w0VHVuqsBQrsVJYoft7N-VXGgo-SRxKHBKX1eWEqYkV3hZJHslUxQvb0V1m3hEBuKHlj4gX5LcEHv-8wj90QlFujFUkRjJpMLqgsi3z-McQSOHNBc6fi3WqOWspiPzzUTQMqMswRPnkOMTlOIqNBoDO6oOrOIHR4CNtN6DZx9KjGTFSCQ__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
    "certify_checkbox": False,
    "field_1_name": None,
    "field_2_country": None,
    "field_3_disregarded_entity_name": None,
    "field_4_checkbox_central_issue_bank": False,
    "field_4_checkbox_complex_trust": False,
    "field_4_checkbox_corporation": False,
    "field_4_checkbox_disregarded_entity": False,
    "field_4_checkbox_estate": False,
    "field_4_checkbox_foreign_government_controlled_entity": False,
    "field_4_checkbox_foreign_government_integral_part": False,
    "field_4_checkbox_grantor_trust": False,
    "field_4_checkbox_hybrid_no": False,
    "field_4_checkbox_hybrid_yes": False,
    "field_4_checkbox_international_organization": False,
    "field_4_checkbox_partnership": False,
    "field_4_checkbox_private_foundation": False,
    "field_4_checkbox_simple_trust": False,
    "field_4_checkbox_tax_exempt_organization": False,
    "field_5_checkbox_active_nffe": False,
    "field_5_checkbox_certain_investment_entities_that_do_not_maintain_financial_accounts": False,
    "field_5_checkbox_certified_deemed_compliant_ffi_low_value_accounts": False,
    "field_5_checkbox_certified_deemed_compliant_limited_life_debt_investment_entity": False,
    "field_5_checkbox_certified_deemed_compliant_nonregistering_local_bank": False,
    "field_5_checkbox_certified_deemed_compliant_sponsored_closely_held_investment_vehicle": False,
    "field_5_checkbox_direct_reporting_nffe": False,
    "field_5_checkbox_entity_wholly_owned_exempt": False,
    "field_5_checkbox_excepted_inter_affiliate_ffi": False,
    "field_5_checkbox_excepted_nonfiancial_entity_bankruptcy": False,
    "field_5_checkbox_excepted_nonfiancial_group_entity": False,
    "field_5_checkbox_excepted_nonfiancial_start_up": False,
    "field_5_checkbox_excepted_territory_nffe": False,
    "field_5_checkbox_exempt_retirement_plans": False,
    "field_5_checkbox_foreign_government": False,
    "field_5_checkbox_international_organization": False,
    "field_5_checkbox_nonparticipating_ffi": False,
    "field_5_checkbox_nonprofit": False,
    "field_5_checkbox_nonreporting_iga_ffi": False,
    "field_5_checkbox_not_financial_account": False,
    "field_5_checkbox_organization_501c": False,
    "field_5_checkbox_owner_documented_ffi": True,
    "field_5_checkbox_participating_ffi": False,
    "field_5_checkbox_passive_nffe": False,
    "field_5_checkbox_publicly_traded_nffe": False,
    "field_5_checkbox_registered_deemed_compliant_ffi": False,
    "field_5_checkbox_reporting_model_one_ffi": False,
    "field_5_checkbox_reporting_model_two_ffi": False,
    "field_5_checkbox_restricted_distributor": False,
    "field_5_checkbox_sponsored_direct_reporting_nffe": False,
    "field_5_checkbox_sponsored_ffi": False,
    "field_5_checkbox_territory_financial_institutions": False,
    "field_6_address": None,
    "field_6_city": None,
    "field_6_country": None,
    "field_7_mailing_city": None,
    "field_7_mailing_country": None,
    "field_7_mailing_street": None,
    "field_8_tin": None,
    "field_9a_giin": None,
    "field_9b_foreign_tin": None,
    "field_9c_checkbox_tin_not_required": False,
    "field_10_reference_number": None,
    "field_11_checkbox_branch_nonparticipating_ffi": False,
    "field_11_checkbox_participating_ffi": False,
    "field_11_checkbox_reporting_model_one_ffi": False,
    "field_11_checkbox_reporting_model_two_ffi": False,
    "field_11_checkbox_us_branch": False,
    "field_12_disregarded_entity_city": None,
    "field_12_disregarded_entity_country": None,
    "field_12_disregarded_entity_street": None,
    "field_13_disregarded_entity_giin": None,
    "field_14a_checkbox": False,
    "field_14a_resident_of": None,
    "field_14b_checkbox_active_trade_or_business_test": False,
    "field_14b_checkbox_benefit_items": False,
    "field_14b_checkbox_derivative_benefits_test": False,
    "field_14b_checkbox_favorable": False,
    "field_14b_checkbox_government": False,
    "field_14b_checkbox_no_lob_article_in_treaty": False,
    "field_14b_checkbox_other_tax_exempt": False,
    "field_14b_checkbox_other": False,
    "field_14b_checkbox_ownership_and_base_erosion_test": False,
    "field_14b_checkbox_publicly_traded_corporation": False,
    "field_14b_checkbox_subsidiary_of_publicly_traded_corporation": False,
    "field_14b_checkbox_tax_exempt_pension": False,
    "field_14b_other_article": None,
    "field_14c_checkbox_dividends": False,
    "field_15_special_rates_article": None,
    "field_15_special_rates_explanation": None,
    "field_15_special_rates_income_type": None,
    "field_15_special_rates_percentage": None,
    "field_16_name": None,
    "field_17a_checkbox": False,
    "field_17b_checkbox": False,
    "field_18_checkbox": False,
    "field_19_checkbox": False,
    "field_20_name": None,
    "field_21_checkbox": False,
    "field_22_checkbox": False,
    "field_23_checkbox": False,
    "field_24a_checkbox": False,
    "field_24b_checkbox": False,
    "field_24c_checkbox": False,
    "field_24d_checkbox": False,
    "field_25a_checkbox": False,
    "field_25b_checkbox": False,
    "field_25c_checkbox": False,
    "field_26_checkbox_model_one": False,
    "field_26_checkbox_model_two": False,
    "field_26_checkbox_trustee_foreign": False,
    "field_26_checkbox_trustee_us": False,
    "field_26_checkbox": False,
    "field_26_country": None,
    "field_26_treated_as": None,
    "field_26_trustee_name": None,
    "field_27_checkbox": False,
    "field_28a_checkbox": False,
    "field_28b_checkbox": False,
    "field_29a_checkbox": False,
    "field_29b_checkbox": False,
    "field_29c_checkbox": False,
    "field_29d_checkbox": False,
    "field_29e_checkbox": False,
    "field_29f_checkbox": False,
    "field_30_checkbox": False,
    "field_31_checkbox": False,
    "field_32_checkbox": False,
    "field_33_checkbox": False,
    "field_33_date": None,
    "field_34_checkbox": False,
    "field_34_date": None,
    "field_35_checkbox": False,
    "field_35_date": None,
    "field_36_checkbox": False,
    "field_37a_checkbox": False,
    "field_37a_name": None,
    "field_37b_checkbox": False,
    "field_37b_market_name": None,
    "field_37b_name": None,
    "field_38_checkbox": False,
    "field_39_checkbox": False,
    "field_40a_checkbox": False,
    "field_40b_checkbox": False,
    "field_40c_checkbox": False,
    "field_41_checkbox": False,
    "field_42_name": None,
    "field_43_checkbox": False,
    "passive_nffe_owners": [],
    "signature_date": None,
    "signature_name": None,
    "signed": True,
}


@responses.activate
def test_process_w8_url():

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/w-8ben-e/",
        json=MOCK,
        status=200,
    )
    d = client.process_w8_document_url(
        file_url="http://cdn-dev.veryfi.com/testing/veryfi-python/receipt_public.jpg"
    )
    assert d == MOCK


@responses.activate
def test_process_w8():

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/w-8ben-e/",
        json=MOCK,
        status=200,
    )
    d = client.process_w8_document(file_path="tests/assets/receipt_public.jpg")
    assert d == MOCK


@responses.activate
def test_get_w8s():
    mock = [MOCK]

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.GET,
        f"{client.versioned_url}/partner/w-8ben-e/",
        json=mock,
        status=200,
    )
    d = client.get_w8s()
    assert d == mock
