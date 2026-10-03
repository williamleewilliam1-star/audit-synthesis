import json, pathlib, sys, unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from audit_synthesis import run_workflow, sha, normalize_work

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=json.loads((pathlib.Path(__file__).parent/'fixture.json').read_text())
        cls.r=run_workflow('trusted research agents',cls.raw)
    def test_retracted_excluded(self):
        self.assertEqual(len(self.r['excluded']),1); self.assertTrue(self.r['excluded'][0]['is_retracted'])
    def test_missing_doi_flag_visible(self):
        self.assertTrue(any(x['flag']=='MISSING_DOI' for x in self.r['validation']['flags']))
    def test_no_scientific_conclusion(self):
        self.assertEqual(self.r['summary']['scientific_conclusion'],'WITHHELD')
    def test_human_gate(self):
        self.assertTrue(self.r['summary']['human_approval_required']); self.assertFalse(self.r['decision']['approved'])
    def test_audit_chain_complete(self):
        self.assertEqual([x['step'] for x in self.r['audit']],['PLAN','DISCOVER','NORMALIZE','VALIDATE','SYNTHESIZE','REVIEW_GATE'])
        self.assertTrue(all(len(x['input_sha256'])==64 and len(x['output_sha256'])==64 for x in self.r['audit']))
    def test_hash_deterministic(self):
        self.assertEqual(sha({'b':2,'a':1}),sha({'a':1,'b':2}))

if __name__=='__main__': unittest.main()
