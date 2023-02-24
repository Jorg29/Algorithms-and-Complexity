import unittest
import MaxSub


class MyTestCase(unittest.TestCase):
    def test_Prefix(self):
        sequence = [2, 17, 20, -27, -29]
        sums = MaxSub.prefix(sequence)
        self.assertEqual(sums, [2, 19, 39, 12, -17])

    def test_SimpleAlgorithm(self):
        sequence = [2, 17, 20, -27, 29]
        sa = MaxSub.SimpleAlgorithm(sequence)
        self.assertEqual(sa, (41, 0, 4))

    def test_AdvanceAlgorithm(self):
        sequence = [2, 17, 20, -27, 29]
        aa = MaxSub.AdvanceAlgorithm(MaxSub.prefix(sequence))
        self.assertEqual(aa, (41, 0, 4))

    def test_Kadane(self):
        sequence = [2, 17, 20, -27 , 29]
        k = MaxSub.Kadane(sequence)
        self.assertEqual(k, (41, 0, 4))


if __name__ == "__main__":
    unittest.main()
