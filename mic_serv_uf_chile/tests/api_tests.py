import pytest
from os import getenv
from dependency_injector import providers
from mic_serv_uf_chile.core import Core
from mic_serv_uf_chile.adapters.db import DB
from datetime import date, timedelta


@pytest.fixture
def client():
	conf_file = getenv('MS_CONFIG')
	if conf_file is None:
		click.echo(
            click.style(
                'MS_CONFIG variable is not defined',
                fg='red',
                bold=True
            )
        )
		sys.exit(1)
	core_obj = Core()
	core_obj.config.from_yaml(conf_file)
	core_obj.db.override(providers.Singleton(DB, config=core_obj.config.db))
	core_obj.init_resources()
	flaskr = core_obj.web_app()
	with flaskr.test_client() as client:
		yield client

def test_validate_health_check(client):
    """Test response OK"""
    res = client.get('/uf/sii/2020-07-30')
    assert res.status == '200 OK'
    
def test_validate_less_out_range_date(client):
    """Test validation for out range date"""
    res = client.get('/uf/sii/2012-12-31')
    assert '2012-12-31 is lower than the last record of 2013-01-01.' == res.json['error']
    
def test_validate_greather_out_range_date(client):
    """Test validation for out range date"""
    param = date.today()
    param = param + timedelta(days=1)
    res = client.get(f'/uf/sii/{str(param)}')
    assert f'{str(param)} is greater than the current date {str(date.today())}.' == res.json['error']
    
def test_invalidate_date(client):
    """Test validation for out range date"""
    res = client.get('/uf/sii/2020-02-30')
    assert '2020-02-30 is an invalid date.' == res.json['error']

def test_check_sample_1(client):
    """Test correct response for sample"""
    res = client.get('/uf/sii/2020-07-30')
    assert '28.668,36' == res.json['value']
    assert '2020-07-30' == res.json['date']
    
def test_check_sample_2(client):
    """Test correct response for sample"""
    res = client.get('/uf/sii/2021-06-24')
    assert '29.692,04' == res.json['value']
    assert '2021-06-24' == res.json['date']