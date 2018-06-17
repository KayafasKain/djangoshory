from django.test import TestCase
from django.test import Client


# Create your tests here.

class ShortLinkTests(TestCase):
    client = Client()
    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['tops'], [])

    def test_make_short_link(self):
        response = self.client.post('/', {
            'basic_link': "https://www.audible.com/ep/youtube?source_code=PBVGBWS0808160056&cvosrc=social%20network%20influencer.Youtube.DemoRanch"
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn("short", response.url)