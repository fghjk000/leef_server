from rest_framework.test import APITestCase, APIClient
from product.models import Product
from leef.models import User, Token


class ProductAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(name='test_name', password='test_pass')
        self.token = Token.objects.create(user=self.user, key='test_key')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.product = Product.objects.create(
            name='Test', price=100, category='Test_Cate', image='url', user=self.user)

    def test_get_products(self):
        response = self.client.get('/product/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        data = {'name': 'new_name', 'price': 150, 'category': 'test_cate', 'image': 'url', 'user': self.user.id}
        response = self.client.post('/product/products/', data=data, format='json')
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['name'], 'new_name')
        self.assertEqual(response_data['price'], 150)
        self.assertEqual(response_data['category'], 'test_cate')
        self.assertEqual(response_data['image'], 'url')
        self.assertEqual(response_data['user'], self.user.id)

    def test_update_product(self):
        data = {'name': 'up_Name', 'price': 200}
        response = self.client.patch(f'/product/products/{self.product.id}/', data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'up_Name')
        self.assertEqual(self.product.price, 200)

    def test_delete_product(self):
        response = self.client.delete(f'/product/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)
