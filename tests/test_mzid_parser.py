import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
import spectra_cluster.ui.mgf_search_result_annotator as mgf_search_result_annotator


class MzIdParserTest(unittest.TestCase):
    """
    Test mzid parser functions
    """
    def setUp(self):
        self.testfile = os.path.join(os.path.dirname(__file__), "testfiles", "test.mzid")


    def testParseMzIdentMl(self):
        # score_field =mgf_search_result_annotator.get_scorefield(filename=self.testfile)

        # self.assertEqual("Scaffold:Peptide Probability", score_field)
        # print(score_field)
        resutls = mgf_search_result_annotator.parse_mzid_by_score_field(filename=self.testfile,
                                                             fdr=2, decoy_string="REVERSED")

        self.assertEqual(6573, len(resutls))



    # def testGetScfield(self):
    #     score_field = mgf_search_result_annotator.get_scorefield(filename=self.testfile)
    #     self.assertEqual("Scaffold:Peptide Probability", score_field)


if __name__ == "__main__":
    unittest.main()
