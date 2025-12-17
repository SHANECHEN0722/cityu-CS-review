import re

print("--- Task 1: Alphabetic Characters Only ---")
REpattern1 = r'^[a-zA-Z]+$'
test_cases1 = ['Python', 'DataScience', 'Hello123']
for text in test_cases1:
    if re.fullmatch(REpattern1, text):
        print(f"'{text}' -- Contains only alphabetic characters")
    else:
        print(f"'{text}' -- No Match")
print("-" * 30)

print("--- Task 2: Words Beginning with a Consonant ---")
REpattern2 = r'\b[b-df-hj-np-tv-z]\w*'
test_cases2 = ["cat", "elephant", "dog", "owl"]
for text in test_cases2:
    if re.match(REpattern2, text, re.IGNORECASE):
        print(f"'{text}' -- A word beginning with a consonant")
    else:
        print(f"'{text}' -- No Match")
print("-" * 30)

print("--- Task 3: Validate Domain Name ---")
REpattern3 = r'^([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
test_cases3  = ['openai.org', 'invalid@site', 'my-site.net']
for text in test_cases3:
    if re.fullmatch(REpattern3, text):
        print(f"'{text}' -- Validate Domain Name")
    else:
        print(f"'{text}' -- No Match")
print("-" * 30)

print("--- Task 4: Extract All Integers ---")
REpattern4 = r'\d+'
test_case4 = 'He scored 45 goals in 2022 and 10 goals in 2023.'
numbers = re.findall(REpattern4, test_case4)
print(f"Extracted numbers: {numbers}")
print("-" * 30)

print("--- Task 5: Identify Valid File Paths ---")
REpattern5 = r'^(?:[a-zA-Z]:\\|/)?(?:[\w.-]*[a-zA-Z0-9]+/)*[\w.-]+\.(txt|csv|jpg|doc)$'
test_cases5 = ['/home/user/file.txt', 'report.doc', '/tmp/image.jpg']   
for text in test_cases5:
    if re.search(REpattern5, text):
        print(f"'{text}' -- Valid File Path")
    else:
        print(f"'{text}' -- No Match")
print("-" * 30)

print("--- Task 6: Validate Canadian Postal Code ---")
REpattern6 = r'^[A-Z]\d[A-Z]\s\d[A-Z]\d$'
test_cases6 = ['K1A 0B1', '123 456']
for test in test_cases6:
    if re.fullmatch(REpattern6, test):
        print(f"'{test}' -- Valid Canadian Postal Code")
    else:
        print(f"'{test}' -- No Match")
print("-" * 30)

print("--- Task 7: Same First and Last Character ---")
REpattern7 = r'^(\w).*\1$'
test_cases7 = ['level', 'stats', 'world']
for text in test_cases7:
    if re.fullmatch(REpattern7, text):
        print(f"'{text}' -- Match")
    else:
        print(f"'{text}' -- No Match")
print("-" * 30)

print("--- Task 8: Strong Password Validation ---")
REpattern8 = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{10,}$'
test_cases8 = ['Secure123!', 'weakpass', 'ValidPass#2023']
for text in test_cases8:
    if re.fullmatch(REpattern8, text):
        print(f"'{text}' -- Match Strong Password Validation")
    else:
        print(f"'{text}' -- No Match")
print("-" * 30)

print("--- Task 9: Match Date Formats (mm/dd/yyyy or yyyy-mm-dd) ---")
REpattern9 = r'(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})'
test_cases9 = ['07/04/2021', '2022-12-31', '01/01/2024', '2022/12/31', '13-2020', '07-04-21']
for text in test_cases9:
    match = re.fullmatch(REpattern9, text)
    if match:
        print(f"'{text}' -- Match Date Formats")
    else:
        print(f"'{text}' -- No Match")
print("-" * 30)

print("--- Task 10: Validate IPv6 Address (Simplified) ---")
REpattern10 = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
test_cases10 = ['2001:0db8:85a3:0000:0000:8a2e:0370:7334', '1234:5678:90ab:cdefghij:0000:0000:0001']
for text in test_cases10:
    if re.fullmatch(REpattern10, text):
        print(f"'{text}' -- Valid IPv6 Address (Simplified)")
    else:
        print(f"'{text}' -- No Match")
print("-" * 30)