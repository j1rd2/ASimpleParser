from Lexer import *
from Parser import *
import sys

if __name__ == '__main__':
    print("---------------------------------------")
    print("Testing good case 1 (should compile)")
    print("---------------------------------------")
    try:
        parser = Parser("test_cases/good/input01.txt")
        parser.analize()
        print("-> Successfully parsed\n")
    except Exception as e:
        print(f"-> Error: {e}\n")

    print("---------------------------------------")
    print("Testing good case 2 (should compile)")
    print("---------------------------------------")
    try:
        parser = Parser("test_cases/good/input02.txt")
        parser.analize()
        print("-> Successfully parsed\n")
    except Exception as e:
        print(f"-> Error: {e}\n")

    print("---------------------------------------")
    print("Testing bad case 1 (should not compile)")
    print("---------------------------------------")
    try:
        parser = Parser("test_cases/bad/input03.txt")
        parser.analize()
        print("-> This should have failed!\n")
    except Exception as e:
        print(f"-> Expected Error caught: {e}\n")

    print("---------------------------------------")
    print("Testing bad case 2 (should not compile)")
    print("---------------------------------------")
    try:
        parser = Parser("test_cases/bad/input04.txt")
        parser.analize()
        print("-> This should have failed!\n")
    except Exception as e:
        print(f"-> Expected Error caught: {e}\n")