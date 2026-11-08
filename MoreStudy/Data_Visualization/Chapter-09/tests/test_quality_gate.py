"""End-to-end checks for the full mutation-driven Challenge 03 gate."""
from pathlib import Path
import subprocess,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
GATE=ROOT/'projects'/'challenge_03_transit_reliability'/'quality_gate.py'
REF=ROOT/'solutions'/'challenge_03_transit_reliability'/'reference_solution.py'
class GateChecks(unittest.TestCase):
 def test_reference_passes_full_quality_gate(self):
  result=subprocess.run([sys.executable,str(GATE),'--script',str(REF)],capture_output=True,text=True,timeout=150)
  self.assertEqual(result.returncode,0,result.stdout+'\n'+result.stderr)
  self.assertIn('PASS: 8/8 checks passed',result.stdout)
 def test_unimplemented_starter_fails_gate(self):
  result=subprocess.run([sys.executable,str(GATE)],capture_output=True,text=True,timeout=30)
  self.assertEqual(result.returncode,1)
  self.assertIn('FAIL',result.stdout)
if __name__=='__main__':unittest.main()
