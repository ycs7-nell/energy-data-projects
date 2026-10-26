import unittest
from model import dispatch
class ModelTests(unittest.TestCase):
 def test_flat_positive(self):self.assertAlmostEqual(dispatch([50]*24)['net'],0,places=5)
 def test_known_trade(self):self.assertAlmostEqual(dispatch([10,100],capacity=1,rte=1)['net'],90,places=5)
 def test_losses(self):self.assertAlmostEqual(dispatch([10,100],capacity=1,rte=.81)['net'],71,places=5)
 def test_no_cycles(self):self.assertAlmostEqual(dispatch([-30,100],cycles=0)['net'],0,places=5)
 def test_negative_prices_no_simultaneous(self):
  r=dispatch([-100,-100],capacity=1);self.assertTrue(all(c*d<1e-7 for c,d in zip(r['charge'],r['discharge'])))
 def test_invalid(self):
  with self.assertRaises(ValueError):dispatch([float('nan')])
if __name__=='__main__':unittest.main()
