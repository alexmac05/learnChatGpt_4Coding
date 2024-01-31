import os
import pytest
from flask import Flask
from flask.testing import FlaskClient
from app import app

@pytest.fixture
def client() -> FlaskClient:
    """Create a test client for the app."""
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_index(client: FlaskClient):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Globoticket - Event Search' in response.data

def test_get_events(client: FlaskClient):
    """Test the get_events route."""
    response = client.get('/get_events?city=TestCity')
    assert response.status_code == 200
    data = response.json
    assert 'events' in data

def test_get_events_missing_city(client: FlaskClient):
    """Test the get_events route with missing city parameter."""
    response = client.get('/get_events')
    assert response.status_code == 400
    data = response.json
    assert 'error' in data

# Add more tests as needed for other routes and functionalities
