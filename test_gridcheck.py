import unittest
from gridcheck import analyze
class Checks(unittest.TestCase):
 def row(self,**kw):
  r=dict(plant_id='1',plant_name='Example',state='NY',generator_id='A',capacity_mw='10',energy_source='SUN');r.update(kw);return r
 def test_distinct_generators(self):
  self.assertEqual(analyze([(2,self.row()),(3,self.row(generator_id='B'))])[1],[])
 def test_duplicate_retained(self):
  c,i=analyze([(2,self.row()),(3,self.row())]);self.assertEqual(len(c),2);self.assertEqual(i[0]['rule'],'duplicate')
 def test_nan(self):
  self.assertEqual(analyze([(2,self.row(capacity_mw='nan'))])[1][0]['rule'],'invalid_capacity')
 def test_missing_schema(self):
  with self.assertRaises(ValueError):analyze([(2,{'plant_id':'1'})])
 def test_source_row(self):
  self.assertEqual(analyze([(42,self.row(state='ZZ'))])[1][0]['source_row'],42)
if __name__=='__main__':unittest.main()
