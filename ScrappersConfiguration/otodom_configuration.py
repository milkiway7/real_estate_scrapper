OTODOM_CONFIGURATION = {
    "url": "https://www.otodom.pl",
    "cookies_button_selector": "Akceptuję",
    "selectors": {
        "find_city_button": '[data-cy="search.form.location.button"]',
        "find_city_input": '[data-cy="search.form.location.input"]',
        "search_button": '#search-form-submit',
        "filter_button_container": '[data-cy="dropdown"]',
        "filter_button": '[data-sentry-component="DropdownSorting"]',
        "filter_newest": '#react-select-listingSorting-option-1',
        "offets_list": '[data-sentry-element="StyledList"]',
        "offer_container": 'li article[data-cy="listing-item"] section',
        "next_page_button": 'li[title="Go to next Page"]',
        "offert":{
            "title": '[data-cy="adPageAdTitle"]',
            "address": 'a[href="#map"]',
            "price": '[data-cy="adPageHeaderPrice"]',
            "price_per_m2": '[aria-label="Cena za metr kwadratowy"]',
            
            "info_container": 'div[data-sentry-element="StyledListContainer"]',
            "offer_type": '[data-cy="adPageAdType"]',
            "company": '',
            "area": '[data-cy="adPageAdArea"]',
            "rooms": '[data-cy="adPageAdRooms"]',
            "heating": '[data-cy="adPageAdHeating"]',
            "floor": '[data-cy="adPageAdFloor"]',
            "rent": '[data-cy="adPageAdRent"]',
            "building_condition": '[data-cy="adPageAdBuildingCondition"]',
            "market": '[data-cy="adPageAdMarket"]',
            "ownership_form": '[data-cy="adPageAdOwnershipForm"]',
            "available_from": '[data-cy="adPageAdAvailable"]',
            "additional_info": '[data-cy="adPageAdAdditionalInfo"]',
            "construction_year": '[data-cy="adPageAdConstructionYear"]',
            "elevator": '[data-cy="adPageAdElevator"]',
            "windows": '[data-cy="adPageAdWindows"]',
            "energy_certificate": '[data-cy="adPageAdEnergyCertificate"]',
            "equipment": '[data-cy="adPageAdEquipment"]',
            "description": '[data-cy="adPageAdDescription"]'
            }
    }
}