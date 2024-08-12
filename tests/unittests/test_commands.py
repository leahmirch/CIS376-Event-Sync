import unittest
from unittest.mock import patch
from flask import Flask
from backend.models import db
from backend.commands import register_commands, init_db_command

class TestCommands(unittest.TestCase):
    def setUp(self):
        # Set up a Flask application in testing mode
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(self.app)
        register_commands(self.app)

        self.runner = self.app.test_cli_runner()

    @patch('backend.commands.db.drop_all')
    @patch('backend.commands.db.create_all')
    def test_init_db_command(self, mock_create_all, mock_drop_all):
        """Test the init-db command."""
        result = self.runner.invoke(args=['init-db'])

        mock_drop_all.assert_called_once()
        mock_create_all.assert_called_once()
        self.assertIn('Initialized the database.', result.output)

if __name__ == '__main__':
    unittest.main()
