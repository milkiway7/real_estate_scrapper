OTODOM_CONFIGURATION = {
    "url": "https://www.otodom.pl",
    "cookies_button_selector": "Akceptuję",
    "selectors": {
        "find_city_button": '[data-cy="search.form.location.button"]',
        "find_city_input": '[data-cy="search.form.location.input"]',
        "search_button": '#search-form-submit',
        "filter_button_container": '[data-sentry-component="DropdownSorting"]',
        "filter_button": '[data-cy="dropdown"]',
        "filter_newest": '#react-select-listingSorting-option-1',
        "offets_list": '[data-sentry-element="StyledList"]',
        "offer_container": 'li article[data-sentry-component="AdvertCard"] section',
        "next_page_button": 'a[title="Go to next Page"]',
        "offert":{
            "title": '[data-cy="adPageAdTitle"]',
            "address": 'a[href="#map"]',
            "price": '[data-cy="adPageHeaderPrice"]',
            "price_per_m2": '[aria-label="Cena za metr kwadratowy"]',
            "details_row":'div[data-sentry-element="ItemGridContainer"]',
            "company": '', # TODO: Add selector for company name
            "details_table":{
                "area": 'Powierzchnia:',
                "rooms": 'Liczba pokoi:',
                "heating": 'Ogrzewanie:',
                "floor": 'Piętro:',
                "rent": 'Czynsz:',
                "building_condition": 'Stan wykończenia:',
                "market": 'Rynek:',
                "ownership_form": 'Forma własności:',
                "available_from": 'Dostępne od:',
                "offer_type": 'Typ ogłoszeniodawcy:',
                "additional_info": 'Informacje dodatkowe:',
            },
            "construction_year": '[data-cy="adPageAdConstructionYear"]',
            "elevator": '[data-cy="adPageAdElevator"]',
            "windows": '[data-cy="adPageAdWindows"]',
            "energy_certificate": '[data-cy="adPageAdEnergyCertificate"]',
            "equipment": '[data-cy="adPageAdEquipment"]',
            "description": '[data-cy="adPageAdDescription"]'
            }
    }
}