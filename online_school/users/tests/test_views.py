import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@pytest.mark.django_db
def test_home_page_access_authenticated(authenticate):
    url = reverse('home')
    response = authenticate.get(url)
    assert response.status_code == 200

def test_home_page_access_no_authenticated(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/users/accounts/login/?next=%s' % url

@pytest.mark.django_db
def test_registration_view(client, create_customuser_group):
    data = {
        'first_name': 'TestName',
        'last_name': 'TestSurname',
        'email': 'test@example.com',
        'phone': '1234567',
        'customuser_group': create_customuser_group.id, 
        'password1': 'us1passwd',
        'password2': 'us1passwd',
    }

    response_get = client.get(reverse('registration'))
    assert response_get.status_code == 200
    response = client.post(reverse('registration'), data)
    
    assert CustomUser.objects.filter(email='test@example.com').exists()
    assert response.status_code == 302
    assert response.url == reverse('home')
    # Проверка, что пользователь был добавлен в группу
    user = CustomUser.objects.get(email='test@example.com')
    assert user.customuser_group.id == data['customuser_group']
    assert user.customuser_group.id in user.groups.all().values_list('id', flat=True)