import unittest

from flask import abort

from pythology import app, db

class PythologyTestCase(unittest.TestCase):

    def setUp(self):
        app.config.update()
        db.create_all()
        # self.client =

if __name__ == '__main__':
    unittest.main()