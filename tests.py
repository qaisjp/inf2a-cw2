import unittest
import semantics
from semantics import *


class Part1Test(unittest.TestCase):
	def testLexicon(self):
		lx = Lexicon()
		lx.add("John", "P")
		lx.add("Mary", "P")
		lx.add("like", "T")
		self.assertItemsEqual(lx.getAll("P"), ["John", "Mary"])

	def testFactBase(self):
		fb = FactBase()
		fb.addUnary("duck", "John")
		fb.addBinary("love", "John", "Mary")
		self.assertTrue(fb.queryUnary("duck", "John"))
		self.assertTrue(fb.queryBinary("love", "John", "Mary"))
		self.assertFalse(fb.queryBinary("love", "Mary", "John"))

	def testVerbStem1(self):
		self.assertEqual('eat', verb_stem('eats'))
		self.assertEqual('tell', verb_stem('tells'))
		self.assertEqual('show', verb_stem('shows'))

	def testVerbStem2(self):
		self.assertEqual('pay', verb_stem('pays'))
		self.assertEqual('buy', verb_stem('buys'))

	def testVerbStem3(self):
		self.assertEqual('fly', verb_stem('flies'))
		self.assertEqual('try', verb_stem('tries'))
		self.assertEqual('unify', verb_stem('unifies'))

	def testVerbStem4(self):
		self.assertEqual('die', verb_stem('dies'))
		self.assertEqual('lie', verb_stem('lies'))
		self.assertEqual('tie', verb_stem('ties'))

	def testVerbStem5(self):
		self.assertEqual('go', verb_stem('goes'))
		self.assertEqual('box', verb_stem('boxes'))
		self.assertEqual('attach', verb_stem('attaches'))
		self.assertEqual('wash', verb_stem('washes'))
		self.assertEqual('dress', verb_stem('dresses'))
		# self.assertEqual('fizz', verb_stem('fizzes'))
		self.assertEqual('buzz', verb_stem('buzzes'))

	def testVerbStem6(self):
		self.assertEqual('lose', verb_stem('loses'))
		# self.assertEqual('daze', verb_stem('dazes'))
		self.assertEqual('laze', verb_stem('lazes'))
		self.assertEqual('lapse', verb_stem('lapses'))
		# self.assertEqual('analyse', verb_stem('analyses'))
		self.assertEqual('rise', verb_stem('rises'))

	def testVerbStem7(self):
		self.assertEqual('have', verb_stem('has'))

	def testVerbStem8(self):
		self.assertEqual('like', verb_stem('likes'))
		self.assertEqual('hate', verb_stem('hates'))
		self.assertEqual('bathe', verb_stem('bathes'))


class Part2Test(unittest.TestCase):
	def testNounStem1(self):
		self.assertEqual('sheep', noun_stem('sheep'))
		self.assertEqual('buffalo', noun_stem('buffalo'))

	def testNounStem2(self):
		# self.assertEqual('leaf', noun_stem('leaves'))
		# self.assertEqual('knife', noun_stem('knives'))
		pass

	def testNounStem3(self):
		self.assertEqual('cat', noun_stem('cats'))
		self.assertEqual('bay', noun_stem('bays'))
		self.assertEqual('fly', noun_stem('flies'))
		self.assertEqual('tie', noun_stem('ties'))
		self.assertEqual('box', noun_stem('boxes'))
		self.assertEqual('rose', noun_stem('roses'))
		self.assertEqual('lake', noun_stem('lakes'))

	def testTagWord(self):
		lx = Lexicon()
		lx.add('John', 'P')
		lx.add('orange', 'N')
		lx.add('orange', 'A')
		lx.add('fish', 'N')
		lx.add('fish', 'I')
		lx.add('fish', 'T')
		self.assertItemsEqual(["P"], tag_word(lx, "John"))
		self.assertItemsEqual(["Ns", "A"], tag_word(lx, "orange"))
		self.assertItemsEqual(["Ns", "Np", "Ip", "Tp"], tag_word(lx, "fish"))
		self.assertItemsEqual(["AR"], tag_word(lx, "a"))
		self.assertItemsEqual([], tag_word(lx, "zxghqw"))


class Part3Test(unittest.TestCase):
	def testParseAgreement(self):
		lx = Lexicon()
		lx.add('John', 'P')
		lx.add('orange', 'N')
		lx.add('orange', 'A')
		lx.add('like', 'T')
		lx.add('a', 'AR')
		tr0 = all_valid_parses(lx, ['Who', 'likes', 'John', '?'])
		self.assertGreater(len(tr0), 0)
		tr = restore_words(tr0[0], ['Who', 'likes', 'John', '?'])
		self.assertTrue(tr[0])


class Part4Test(unittest.TestCase):
	def setUp(self):
		self.lx = Lexicon()
		self.lx.add('John', 'P')
		self.lx.add('orange', 'N')
		self.lx.add('orange', 'A')
		self.lx.add('duck', 'N')
		self.lx.add('frog', 'N')
		self.lx.add('like', 'T')
		self.lx.add('a', 'AR')

	def testSemantics1(self):
		phrase = 'Who is a duck ?'
		model = r'(\x. N_duck(x))'
		tr0 = all_valid_parses(self.lx, phrase.split())[0]
		tr = restore_words(tr0, phrase.split())
		self.assertTrue(lp.parse(sem(tr)).simplify(), lp.parse(model).simplify())

	def testSemantics2(self):
		phrase = 'Which orange duck likes a frog ?'
		model = r'(\x. ((A_orange(x) & N_duck(x)) & (exists y. (N_frog(y) & T_like(x,y)))))'
		tr0 = all_valid_parses(self.lx, phrase.split())[0]
		tr = restore_words(tr0, phrase.split())
		self.assertTrue(lp.parse(sem(tr)).simplify(), lp.parse(model).simplify())

	def testSemantics3(self):
		phrase = 'Who does John like ?'
		model = r'(\x. (exists y.((y=John) & T_like(y,x))))'
		tr0 = all_valid_parses(self.lx, phrase.split())[0]
		tr = restore_words(tr0, phrase.split())
		self.assertTrue(lp.parse(sem(tr)).simplify(), lp.parse(model).simplify())

	if __name__ == '__main__':
		unittest.main()
