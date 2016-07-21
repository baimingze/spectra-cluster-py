import unittest
import os
from .context import clustering_parser


class ClusteringParserTest(unittest.TestCase):
    """
    Test case for the ClusteringParser class
    """
    def setUp(self):
        self.testfile = os.path.abspath('.') + os.path.sep + "test.clustering"
        self.ptm_string = "1-MOD:1234,2-MOD:00043"
        self.spec_line = "SPEC\t#file=/home/jg/Projects/ebi-pride/pride-cluster-2/chimeric-spectra-generator/src/test/" \
                         "resources/PRD000001.st.id.mgf#id=index=1464#title=id=PRD000001;PRIDE_Exp_Complete_Ac_1644.xml;" \
                         "spectrum=5071,splib_sequence=MEGIGLK,score=0.362,peptideR2=,scoreR2=\ttrue\tMEGIGLK\t382.149\t2" \
                         "\t\t\t0.0"

    def test_parse_ptms(self):
        ptms = clustering_parser.ClusteringParser._parse_ptms(self.ptm_string)

        self.assertEqual(2, len(ptms))
        self.assertEqual(1, ptms[0].position)
        self.assertEqual("MOD:1234", ptms[0].accession)
        self.assertEqual(2, ptms[1].position)
        self.assertEqual("MOD:00043", ptms[1].accession)

        self.assertEqual("1-MOD:1234", str(ptms[0]))

    def test_parse_spec_line(self):
        spectrum = clustering_parser.ClusteringParser._parse_spec_line(self.spec_line)

        self.assertEqual("MEGIGLK", list(spectrum.psms)[0].sequence)
        self.assertEqual(2, spectrum.charge)
        self.assertEqual(382.149, spectrum.precursor_mz)

        self.assertEqual("/home/jg/Projects/ebi-pride/pride-cluster-2/chimeric-spectra-generator/src/test/resources/"
                         "PRD000001.st.id.mgf", spectrum.get_filename())
        self.assertEqual("index=1464", spectrum.get_id())
        self.assertEqual("id=PRD000001;PRIDE_Exp_Complete_Ac_1644.xml;spectrum=5071,splib_sequence=MEGIGLK,"
                         "score=0.362,peptideR2=,scoreR2=", spectrum.get_title())

        self.assertEqual("MEGIGLK", list(spectrum.get_clean_sequences())[0])

        spectrum_copy = clustering_parser.ClusteringParser._parse_spec_line(self.spec_line)
        self.assertEqual(spectrum, spectrum_copy)

        self.assertEqual("<Spectrum @ 382.149 m/z 2.0+ with 1 PSMs>", str(spectrum))

    def test_parse_clustering_file(self):
        parser = clustering_parser.ClusteringParser(self.testfile)

        n_clusters = 0

        for cluster in parser:
            n_clusters += 1

            if n_clusters == 1:
                self.assertEqual("1cc813a1-4e75-4c1d-99aa-752312fbe554", cluster.id)
                self.assertEqual(359.155, cluster.precursor_mz)
                self.assertEqual(2, len(cluster.get_spectra()))
                self.assertEqual(1, len(cluster.get_spectra()[0].psms))
                self.assertEqual("RPHFFFPK", cluster.get_spectra()[0].psms.__iter__().__next__().sequence)
                self.assertEqual(1, len(cluster.max_sequences))
                self.assertEqual("RPHFFFPK", cluster.max_sequences[0])
                self.assertEqual(1, cluster.max_ratio)
                self.assertEqual(1, cluster.max_il_ratio)

                for spectrum in cluster.get_spectra():
                    for psm in spectrum.psms:
                        if len(psm.ptms) > 0:
                            self.assertEqual("R[MOD:1234]PHFFFPK", str(psm))

            if n_clusters == 2:
                self.assertEqual("9a582e74-e8b1-451d-a007-cadc362aa2ce", cluster.id)
                self.assertEqual(2/3, cluster.max_ratio)
                self.assertEqual(2/3, cluster.max_il_ratio)
                self.assertEqual(1, len(cluster.max_sequences))
                self.assertEqual("MEGIGLK", cluster.max_sequences[0])

        self.assertEqual(838, n_clusters)
