from django.test import override_settings

from bedrock.pocketfeed import api
from bedrock.pocketfeed.models import PocketArticle

import json
import pytest
import responses
from mock import patch
from pathlib2 import Path


TEST_DATA = Path(__file__).with_name('test_data')


def get_test_file_content(filename):
    with TEST_DATA.joinpath(filename).open() as fh:
        return fh.read()


def setup_responses():
    responses.add(responses.POST, 'http://www.test.com', json=json.loads(get_test_file_content('articles.json')))


@responses.activate
@override_settings(POCKET_API_URL='http://www.test.com')
def test_get_articles_data():
    setup_responses()
    articles = api.get_articles_data()
    assert len(articles['recommendations']) == 3
    assert articles['recommendations'][0]['id'] == 2262198874
    assert articles['recommendations'][1]['id'] == 2248108002


@responses.activate
@pytest.mark.django_db
@override_settings(POCKET_API_URL='http://www.test.com')
def test_refresh_articles():
    setup_responses()
    updated, deleted = PocketArticle.objects.refresh()
    assert updated == 3
    assert deleted == 0
    articles = PocketArticle.objects.all()
    assert len(articles) == 3
    article = articles.get(pocket_id=2248108002)
    assert article.domain == 'economist.com'
    assert article.url == 'https://www.economist.com/the-world-if/2018/07/07/what-if-people-were-paid-for-their-data'
