
import unittest
import re

from pbcommand.pb_io.common import load_pipeline_chunks_from_json
from pbcore.io import ContigSet, FastaReader
import pbcommand.testkit.core

from base import get_temp_file


def _write_fasta_or_contigset(file_name):
    fasta_file = re.sub(".contigset.xml", ".fasta", file_name)
    rec = [">chr%d\nacgtacgtacgt" % x for x in range(251)]
    with open(fasta_file, "w") as f:
        f.write("\n".join(rec))
    if file_name.endswith(".xml"):
        cs = ContigSet(fasta_file)
        cs.write(file_name)


class ScatterSequenceBase(object):
    READER_CLASS = None

    @classmethod
    def setUpClass(cls):
        super(ScatterSequenceBase, cls).setUpClass()
        _write_fasta_or_contigset(cls.INPUT_FILES[0])

    def run_after(self, rtc, output_dir):
        json_file = rtc.task.output_files[0]
        chunks = load_pipeline_chunks_from_json(json_file)
        n_rec = 0
        with self.READER_CLASS(self.INPUT_FILES[0]) as f:
            n_rec = len([r for r in f])
        n_rec_chunked = 0
        for chunk in chunks:
            d = chunk.chunk_d
            with self.READER_CLASS(d[self.CHUNK_KEYS[0]]) as cs:
                n_rec_chunked += len([r for r in cs])
        self.assertEqual(n_rec_chunked, n_rec)


class TestScatterFilterFasta(ScatterSequenceBase,
                             pbcommand.testkit.core.PbTestScatterApp):
    READER_CLASS = FastaReader
    DRIVER_BASE = "python -m pbsmrtpipe.tools_dev.scatter_filter_fasta"
    INPUT_FILES = [
        get_temp_file(suffix=".fasta")
    ]
    MAX_NCHUNKS = 12
    RESOLVED_MAX_NCHUNKS = 12
    CHUNK_KEYS = ("$chunk.fasta_id",)


class TestScatterContigSet(ScatterSequenceBase,
                           pbcommand.testkit.core.PbTestScatterApp):
    READER_CLASS = ContigSet
    DRIVER_BASE = "python -m pbsmrtpipe.tools_dev.scatter_contigset"
    INPUT_FILES = [
        get_temp_file(suffix=".contigset.xml")
    ]
    MAX_NCHUNKS = 12
    RESOLVED_MAX_NCHUNKS = 12
    CHUNK_KEYS = ("$chunk.contigset_id",)
