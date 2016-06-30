#! /usr/bin/env python
# -*-coding:utf-8 -*

import sys
import os

class TestCounter(unittest.TestCase):
    """teste le compteur: pour essayer le test unitaire"""
    
    def testCursor1(self):
        """teste si le curseur avance correctement"""
        s, e = 1, 100
        c = Counter(start=s, end=e)
        for i in xrange(s, e + 1):
            self.assertEqual(c.cursor, i)
            c.next()
        c.finish()
            
    def testCursorN(self):
        """teste si le curseur avance correctement"""
        s, e = 1, 100
        st = 20
        c = Counter(start=s, end=e, step=st)
        for i in xrange(s, e + 1, st):
            self.assertEqual(c.cursor, i)
            c.next()
        c.finish()

    def testStatus(self):
        """teste si le compteur s'active et se désactive correctement'"""
        c = Counter(isEnabled=True)
        self.assertEqual(c.isEnabled, True)
        c.toggle()
        self.assertEqual(c.isEnabled, False)

def main():
    unittest.main()

if __name__ == '__main__':
    sys.exit(main())


