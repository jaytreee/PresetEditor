from unittest import TestCase
from schemamanager import iXMLSchemaManager
import os

class Test_SchemaManager(TestCase):

    def test_main(self):
        # after that we should have all files on our local computer
        m= iXMLSchemaManager()
        m.main()
        for key in m.md5sums:
            self.assertTrue(os.path.isfile(m.folder+'/'+key))
