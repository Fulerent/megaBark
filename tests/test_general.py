import unittest
from datetime import datetime
from bark.persistence import BookmarkDatabase
from unittest.mock import patch


class TestGeneralBark:
    def test_create_db(self, create_test_db):
        db = create_test_db

        assert isinstance(db, BookmarkDatabase)

    def test_create_notion(self, create_test_db):
        current_date = str(datetime.now())
        data_notion: dict = {
            'title': 'Test Notion',
            'url': 'http://test.company.com',
            'notes': 'Test Description',
            'date_added': current_date,
        }

        create_test_db.create(data_notion)
        test_notion: list = create_test_db.list()[0]

        assert len(create_test_db.list()) == 1
        assert test_notion[0] == 1
        assert test_notion[1] == 'Test Notion'
        assert test_notion[2] == 'http://test.company.com'
        assert test_notion[3] == 'Test Description'
        assert test_notion[4] == current_date

    def test_edit_notion(self, create_test_db):
        id_notion = 1  # after last the test
        new_data_notion: dict = {
            'title': 'Test Notion after edit',
            'url': 'None',
        }

        create_test_db.edit(id_notion, new_data_notion)
        test_notion: list = create_test_db.list()[0]

        assert test_notion[0] == 1
        assert test_notion[1] == 'Test Notion after edit'
        assert test_notion[2] == 'None'
        assert test_notion[3] == 'Test Description'
        assert test_notion[4] != f'{datetime.now()}'

    def test_deleted_notion(self, create_test_db):
        id_notion = 1  # after the creation test

        create_test_db.delete(id_notion)

        assert len(create_test_db.list()) == 0


class TestGithubFunctional(unittest.TestCase):
    @patch('bark.basic_commands.ImportGitHubStarsCommand')
    def test_get_stars_from_github(self, GithubMock):
        mock = GithubMock()
        mock.execute.return_value = True, {
            'title': 'Mock name',
            'url': 'http://mock.url.ru',
            'notes': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. '
                     'Lorem Ipsum has been '
                     'the industry\'s standard dummy text ever since the 1500s, '
                     'when an unknown printer took a galley '
                     'of type and scrambled it to make a type specimen book. '
                     'It has survived not only five centuries, '
                     'but also the leap into electronic typesetting, '
                     'remaining essentially unchanged. ',
        }
        status, notes = mock.execute()

        assert GithubMock.called
        assert status
        assert notes['title'] == 'Mock name'
        assert notes['url'] == 'http://mock.url.ru'
        assert 'remaining essentially unchanged' in notes['notes']
