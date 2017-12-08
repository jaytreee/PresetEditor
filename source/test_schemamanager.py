from unittest import TestCase
from schemamanager import iXMLSchemaManager
import os
from urllib import error

class Test_SchemaManager(TestCase):

    def test_main(self):
        # after that we should have all files on our local computer
        m= iXMLSchemaManager()
        m.main()
        for key in m.md5sums:
            self.assertTrue(os.path.isfile(m.folder+'/'+key))

    def test_noconnection(self):
        # wrong url
        m= iXMLSchemaManager()
        m.md5sumurl = 'https://dist.ithera-medsafsdaical.com/pydist/schemata/'
        self.assertRaises(error.URLError, m.getmd5sums)
