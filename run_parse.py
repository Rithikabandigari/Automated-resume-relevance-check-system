import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from parse_resume import parse_resume

result = parse_resume("../../sample.txt")  
print("==== PARSED RESUME ====")
print(result)