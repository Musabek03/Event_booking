import pytest
from .models import Category

@pytest.mark.django_db
def test_get_category(api_client):
    Category.objects.create(name="Qosiqshilar", slug="qosiqshilar")

    response = api_client.get('/api/category/')


    assert response.status.code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == "Qosiqshilar"