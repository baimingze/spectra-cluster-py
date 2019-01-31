import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
import spectra_cluster.ui.mgf_search_result_annotator as mgf_search_result_annotator


class XTandemImportTest(unittest.TestCase):
    def setUp(self):
        self.testfile = os.path.join(os.path.dirname(__file__), "testfiles", "test_xtandem.mzid")

    def testXtandemImport(self):
        # results = mgf_ijjsearch_result_annotator.parser_mzident(filename=self.testfile,
        #                                                      score_field="X\\!Tandem:expect",
        #                                                      title_field="spectrumID", fdr=0.01,
        #                                                      decoy_string="REVERSED")
        #
        # self.assertEqual(len(results), 3579)

        results = mgf_search_result_annotator.parse_mzid_by_score_field(filename=self.testfile,
                                                                        fdr=0.01, decoy_string="REVERSED")
        self.assertEqual(len(results), 3579)

        for psm in results:
            self.assertNotEqual(psm.index, mgf_search_result_annotator.Psm.MISSING_INDEX)

if __name__ == "__main__":
    unittest.main()
