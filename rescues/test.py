"""
rescue_tests.py

Tests for rescue.py -- just the RNG for now.
"""

import unittest

from rescue import DotNetRNG, OtherRNG, RescueCode, Symbol


class TestRNG(unittest.TestCase):
    """
    Test cases for the DotNetRNG class. Assert that we produce the right
    values for some seeds for which we were able to find examples online:

    https://docs.microsoft.com/en-us/dotnet/api/system.random.-ctor?view=netframework-4.8#System_Random__ctor_System_Int32_

    I also installed the .NET Core from

    https://docs.microsoft.com/en-us/dotnet/core/install/   linux-package-manager-ubuntu-1910

    and created test programs to validate results another way.
    """

    def test_seed_123(self):
        """Test that the RNG produces the right values for seed 123"""

        rng = DotNetRNG(123)
        other = OtherRNG(123)
        assert rng.next() == 2114319875
        assert rng.next() == 1949518561
        assert rng.next() == 1596751841
        assert rng.next() == 1742987178
        assert rng.next() == 1586516133
        assert rng.next() == 103755708

        assert other.next() == 2114319875
        assert other.next() == 1949518561
        assert other.next() == 1596751841
        assert other.next() == 1742987178
        assert other.next() == 1586516133
        assert other.next() == 103755708

    # def test_seed_456(self):
    #     """Test that the RNG produces the right values for seed 456"""

    #     rng = DotNetRNG(456)
    #     assert rng.next() == 2044805024
    #     assert rng.next() == 1323311594
    #     assert rng.next() == 1087799997
    #     assert rng.next() == 1907260840
    #     assert rng.next() == 179380355
    #     assert rng.next() == 120870348

    # def test_seed_12(self):
    #     """Test that the RNG produces the right values for seed 12"""

    #     rng = DotNetRNG(12)
    #     assert rng.next() == 2137491492
    #     assert rng.next() == 726598452
    #     assert rng.next() == 334746691
    #     assert rng.next() == 256573526
    #     assert rng.next() == 1339733510
    #     assert rng.next() == 98050828
    #     assert rng.next() == 607109598
    #     assert rng.next() == 992976482
    #     assert rng.next() == 992459907
    #     assert rng.next() == 1500484683


class TestSymbol(unittest.TestCase):
    """Test methods of Symbol"""

    def test_alphabet(self):
        assert len(Symbol.ALPHABET) == 64

    def test_text(self):
        assert Symbol("1f").text == "1f"
        assert Symbol("6h").text == "6h"
        assert Symbol("Xe").text == "Xe"
        assert Symbol("4w").text == "4w"
        assert Symbol("Pf").text == "Pf"

    def test_pos(self):
        assert Symbol("1f").pos == 0
        assert Symbol("5w").pos == 30
        assert Symbol("Ds").pos == 63

    def test_comparisons(self):
        """Test that symbols are in the right order"""

        # Symbols go fire - heart - water - emerald - star
        assert Symbol("1f").pos < Symbol("2f").pos
        assert Symbol("1f").pos < Symbol("1h").pos
        assert Symbol("1f").pos < Symbol("1w").pos
        assert Symbol("1f").pos < Symbol("1e").pos
        assert Symbol("1f").pos < Symbol("1s").pos
        assert Symbol("Pf").pos < Symbol("Mf").pos
        assert Symbol("Mf").pos < Symbol("Df").pos
        assert Symbol("Df").pos < Symbol("Xf").pos
        assert Symbol("Xf").pos < Symbol("1h").pos
        assert Symbol("8e").pos < Symbol("4s").pos
        assert Symbol("3h").pos < Symbol("5w").pos
        assert Symbol("9w").pos < Symbol("Pe").pos

    def test_prev(self):
        assert Symbol("1f").prev == Symbol("Ds")  # wrapping
        assert Symbol("2w").prev == Symbol("1w")
        assert Symbol("Ph").prev == Symbol("9h")
        assert Symbol("1h").prev == Symbol("Xf")
        assert Symbol("Me").prev == Symbol("Pe")
        assert Symbol("8h").prev == Symbol("7h")

    def test_next(self):
        assert Symbol("1f").next == Symbol("2f")
        assert Symbol("2w").next == Symbol("3w")
        assert Symbol("9h").next == Symbol("Ph")
        assert Symbol("Ph").next == Symbol("Mh")
        assert Symbol("De").next == Symbol("Xe")
        assert Symbol("Xe").next == Symbol("1s")
        assert Symbol("Ds").next == Symbol("1f")  # wrapping


class TestRescueCode(unittest.TestCase):
    """Test methods of RescueCode"""

    basic_code = "Pf8sPs4fPhXe3f7h1h2h5s8w3h9s3fXh4wMw4s6w8w9w6e2f8h9f1h2s1w8h"

    def test_inc_symbol(self):
        """Test that the inc_symbol method does the right thing"""

        code = RescueCode.from_text(TestRescueCode.basic_code)

        code = code.inc_symbol(0)
        assert code.symbols[0] == Symbol("Mf")

        code = code.inc_symbol(1)
        assert code.symbols[1] == Symbol("9s")

        code = code.inc_symbol(2)
        assert code.symbols[2] == Symbol("Ms")

        code = code.inc_symbol(3)
        assert code.symbols[3] == Symbol("5f")

        code = code.inc_symbol(4)
        assert code.symbols[4] == Symbol("Mh")

    def test_dec_symbol(self):
        """Test that the dec_symbol method does the right thing"""

        code = RescueCode.from_text(TestRescueCode.basic_code)

        code = code.dec_symbol(15)
        assert code.symbols[15] == Symbol("Dh")

        code = code.dec_symbol(16)
        assert code.symbols[16] == Symbol("3w")

        code = code.dec_symbol(17)
        assert code.symbols[17] == Symbol("Pw")

        code = code.dec_symbol(18)
        assert code.symbols[18] == Symbol("3s")

        code = code.dec_symbol(19)
        assert code.symbols[19] == Symbol("5w")

    def test_shuffle(self):
        """Test that the shuffle method puts symbols in the right spot"""

        code = RescueCode.from_text(TestRescueCode.basic_code)
        new_code = code.shuffle()

        assert code.symbols[0] == new_code.symbols[3]
        assert code.symbols[1] == new_code.symbols[0x1B]
        assert code.symbols[2] == new_code.symbols[0xD]
        assert code.symbols[3] == new_code.symbols[0x15]
        assert code.symbols[4] == new_code.symbols[0xC]
        assert code.symbols[5] == new_code.symbols[9]
        assert code.symbols[6] == new_code.symbols[7]
        assert code.symbols[7] == new_code.symbols[4]
        assert code.symbols[8] == new_code.symbols[6]
        assert code.symbols[9] == new_code.symbols[0x11]
        assert code.symbols[10] == new_code.symbols[0x13]
        assert code.symbols[0xB] == new_code.symbols[0x10]
        assert code.symbols[0xC] == new_code.symbols[0x1C]
        assert code.symbols[0xD] == new_code.symbols[0x1D]
        assert code.symbols[0xE] == new_code.symbols[0x17]
        assert code.symbols[0xF] == new_code.symbols[0x14]
        assert code.symbols[0x10] == new_code.symbols[0xB]
        assert code.symbols[0x11] == new_code.symbols[0]
        assert code.symbols[0x12] == new_code.symbols[1]
        assert code.symbols[0x13] == new_code.symbols[0x16]
        assert code.symbols[0x14] == new_code.symbols[0x18]
        assert code.symbols[0x15] == new_code.symbols[0xE]
        assert code.symbols[0x16] == new_code.symbols[8]
        assert code.symbols[0x17] == new_code.symbols[2]
        assert code.symbols[0x18] == new_code.symbols[0xF]
        assert code.symbols[0x19] == new_code.symbols[0x19]
        assert code.symbols[0x1A] == new_code.symbols[10]
        assert code.symbols[0x1B] == new_code.symbols[5]
        assert code.symbols[0x1C] == new_code.symbols[0x12]
        assert code.symbols[0x1D] == new_code.symbols[0x1A]

    def test_unshuffle(self):
        """Test that the unshuffle method puts symbols in the right spot"""

        code = RescueCode.from_text(TestRescueCode.basic_code)
        new_code = code.unshuffle()

        assert new_code.symbols[0] == code.symbols[3]
        assert new_code.symbols[1] == code.symbols[0x1B]
        assert new_code.symbols[2] == code.symbols[0xD]
        assert new_code.symbols[3] == code.symbols[0x15]
        assert new_code.symbols[4] == code.symbols[0xC]
        assert new_code.symbols[5] == code.symbols[9]
        assert new_code.symbols[6] == code.symbols[7]
        assert new_code.symbols[7] == code.symbols[4]
        assert new_code.symbols[8] == code.symbols[6]
        assert new_code.symbols[9] == code.symbols[0x11]
        assert new_code.symbols[10] == code.symbols[0x13]
        assert new_code.symbols[0xB] == code.symbols[0x10]
        assert new_code.symbols[0xC] == code.symbols[0x1C]
        assert new_code.symbols[0xD] == code.symbols[0x1D]
        assert new_code.symbols[0xE] == code.symbols[0x17]
        assert new_code.symbols[0xF] == code.symbols[0x14]
        assert new_code.symbols[0x10] == code.symbols[0xB]
        assert new_code.symbols[0x11] == code.symbols[0]
        assert new_code.symbols[0x12] == code.symbols[1]
        assert new_code.symbols[0x13] == code.symbols[0x16]
        assert new_code.symbols[0x14] == code.symbols[0x18]
        assert new_code.symbols[0x15] == code.symbols[0xE]
        assert new_code.symbols[0x16] == code.symbols[8]
        assert new_code.symbols[0x17] == code.symbols[2]
        assert new_code.symbols[0x18] == code.symbols[0xF]
        assert new_code.symbols[0x19] == code.symbols[0x19]
        assert new_code.symbols[0x1A] == code.symbols[10]
        assert new_code.symbols[0x1B] == code.symbols[5]
        assert new_code.symbols[0x1C] == code.symbols[0x12]
        assert new_code.symbols[0x1D] == code.symbols[0x1A]


if __name__ == "__main__":
    unittest.main()

