from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Business, BusinessCategory

User = get_user_model()


class BranchAdminOwnershipTests(APITestCase):
    """Business Admin / Branch Admin RBAC boundaries: a Business Admin (owner of a
    parent business) can manage their branches even after reassigning a branch to a
    different Branch Admin login, but that Branch Admin can never reach the parent
    business or a sibling branch, and only the parent's owner may archive/reset a
    branch — never the branch's own admin or an unrelated user.
    """

    def setUp(self):
        self.category = BusinessCategory.objects.create(name='Test Cat', slug='test-cat', icon='🏪')
        self.business_admin = User.objects.create_user(
            username='ba', email='ba@example.com', password='pass12345', role=User.Role.BUSINESS_OWNER,
        )
        self.parent = Business.objects.create(
            owner=self.business_admin, name='Parent Biz', slug='parent-biz',
            category=self.category, phone='9800000000',
        )

    def test_business_and_branch_codes_assigned_on_create(self):
        self.assertTrue(self.parent.business_code)
        self.assertIsNone(self.parent.branch_code)

    def test_business_admin_can_create_branch_with_new_owner_email(self):
        self.client.force_authenticate(user=self.business_admin)
        resp = self.client.post('/api/businesses/my/', {
            'name': 'Branch One', 'category': self.category.id, 'parent': self.parent.id,
            'phone': '9811111111', 'owner_email': 'branch_admin@example.com',
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.data)
        branch = Business.objects.get(slug=resp.data['slug'] if 'slug' in resp.data else Business.objects.latest('id').slug)
        branch.refresh_from_db()
        self.assertEqual(branch.owner.email, 'branch_admin@example.com')
        self.assertTrue(branch.branch_code)

    def _make_branch(self, owner_email='branch_admin2@example.com'):
        self.client.force_authenticate(user=self.business_admin)
        resp = self.client.post('/api/businesses/my/', {
            'name': 'Branch Two', 'category': self.category.id, 'parent': self.parent.id,
            'phone': '9822222222', 'owner_email': owner_email,
        })
        return Business.objects.get(slug=resp.data.get('slug', Business.objects.latest('id').slug))

    def test_business_admin_retains_management_access_after_reassignment(self):
        branch = self._make_branch()
        self.client.force_authenticate(user=self.business_admin)
        resp = self.client.get(f'/api/businesses/my/{branch.slug}/')
        self.assertEqual(resp.status_code, 200)

    def test_branch_admin_cannot_see_parent_or_sibling(self):
        branch = self._make_branch()
        other_branch = self._make_branch(owner_email='branch_admin3@example.com')
        branch_admin = branch.owner
        self.client.force_authenticate(user=branch_admin)

        resp = self.client.get(f'/api/businesses/my/{self.parent.slug}/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        resp = self.client.get(f'/api/businesses/my/{other_branch.slug}/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        resp = self.client.get(f'/api/businesses/my/{branch.slug}/')
        self.assertEqual(resp.status_code, 200)

    def test_only_parent_owner_can_archive_branch(self):
        branch = self._make_branch()
        branch_admin = branch.owner
        outsider = User.objects.create_user(
            username='outsider', email='outsider@example.com', password='pass12345', role=User.Role.BUSINESS_OWNER,
        )

        self.client.force_authenticate(user=branch_admin)
        resp = self.client.post(f'/api/businesses/my/{branch.slug}/archive/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(user=outsider)
        resp = self.client.post(f'/api/businesses/my/{branch.slug}/archive/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(user=self.business_admin)
        resp = self.client.post(f'/api/businesses/my/{branch.slug}/archive/')
        self.assertEqual(resp.status_code, 200)
        branch.refresh_from_db()
        self.assertEqual(branch.status, Business.Status.ARCHIVED)

    def test_only_parent_owner_can_reset_branch_admin_password(self):
        branch = self._make_branch()
        outsider = User.objects.create_user(
            username='outsider2', email='outsider2@example.com', password='pass12345', role=User.Role.BUSINESS_OWNER,
        )
        self.client.force_authenticate(user=outsider)
        resp = self.client.post(f'/api/businesses/my/{branch.slug}/reset-password/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(user=self.business_admin)
        resp = self.client.post(f'/api/businesses/my/{branch.slug}/reset-password/')
        self.assertEqual(resp.status_code, 200)
        new_password = resp.data['new_password']
        branch.owner.refresh_from_db()
        self.assertTrue(branch.owner.check_password(new_password))
