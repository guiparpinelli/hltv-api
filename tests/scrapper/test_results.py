from hltv_api.scrapper.results import collect_results


def test_collect_all_latest_100_results_data_from_results_page(results_html):
    results = collect_results(results_html)
    assert len(results) == 100
