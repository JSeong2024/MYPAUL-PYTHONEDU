"""Documentation links and source-code compilation."""
from pathlib import Path
import ast
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]
class DocumentationChecks(unittest.TestCase):
 def test_markdown_relative_links_exist(self):
  for file in ROOT.rglob('*.md'):
   txt=file.read_text(encoding='utf-8')
   # markdown inline links; skip HTTP links and pure anchors
   for target in re.findall(r'!?(?:\[[^\]]*\])\(([^()]+)\)',txt):
    path=target.split('#',1)[0]
    if not path or path.startswith(('http://','https://','mailto:')):continue
    with self.subTest(file=file.relative_to(ROOT),target=target):self.assertTrue((file.parent/path).exists(),f'{file}: {target}')
 def test_all_python_files_parse(self):
  for file in ROOT.rglob('*.py'):
   with self.subTest(file=file.name):ast.parse(file.read_text(encoding='utf-8'))
 def test_readme_contains_ten_linked_projects(self):
  readme=(ROOT/'README.md').read_text(encoding='utf-8')
  ids=sorted(p.name for p in (ROOT/'projects').iterdir() if p.is_dir())
  self.assertEqual(len(ids),10)
  for pid in ids:self.assertIn(f'./projects/{pid}/README.md',readme)
 def test_no_reused_project_solution_implementation(self):
  files=list((ROOT/'solutions').glob('*/reference_solution.py'))
  self.assertEqual(len(files),10)
  allsrc=[f.read_text(encoding='utf-8') for f in files]
  self.assertEqual(len(set(allsrc)),10)
 def test_all_project_readmes_include_required_sections(self):
  for path in (ROOT/'projects').glob('*/README.md'):
   content=path.read_text(encoding='utf-8')
   with self.subTest(project=path.parent.name):
    for s in ('문제 상황','제공 데이터','데이터 검증 및 계산 기준','구현 요구사항','구현 가이드','테스트 시나리오','완료 기준'):
     self.assertIn(s,content)
    self.assertNotIn('[ ]',content)
    self.assertNotIn('실무',content)

if __name__=='__main__':unittest.main()
