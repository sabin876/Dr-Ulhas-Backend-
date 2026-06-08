import json

print("Reading data_dump_utf8.json...")
with open("data_dump_utf8.json", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Verify the lines at the start of corruption
print("Line 796 (0-indexed 795):", repr(lines[795]))
print("Line 797 (0-indexed 796):", repr(lines[796]))
print("Line 798 (0-indexed 797):", repr(lines[797]))
print("Line 799 (0-indexed 798):", repr(lines[798]))

# Verify the lines at the end of corruption
print("Line 887 (0-indexed 886):", repr(lines[886]))
print("Line 888 (0-indexed 887):", repr(lines[887]))
print("Line 889 (0-indexed 888):", repr(lines[888]))
print("Line 890 (0-indexed 889):", repr(lines[889]))

# The replacement block (lines 797 to 888, indices 796 to 887)
# We replace index 796 to 887 inclusive.
# That is, lines[796:888] in python slice notation.

replacement_content = """          {
            "question": "à¤°à¤¿à¤\u0095à¤µà¤°à¥\u0080 à¤\u0095à¥\u0080 à¤\u0085à¤µà¤§à¤¿ à¤\u0095à¤¿à¤¤à¤¨à¥\u0080 à¤²à¤‚à¤¬à¥\u0080 à¤¹à¥ˆ?",
            "answer": "à¤°à¤¿à¤\u0095à¤µà¤°à¥\u0080 à¤ªà¥\u008dà¤°à¤\u0095à¥\u008dà¤°à¤¿à¤¯à¤¾ à¤\u0095à¥\u0087 à¤\u0086à¤§à¤¾à¤° à¤ªà¤° à¤à¤¿à¤¨à¥\u008dà¤¨ à¤¹à¥\u008bà¤¤à¥\u0080 à¤¹à¥\u0085, à¤²à¥\u0087à¤\u0095à¤¿à¤¨ à¤\u0085à¤§à¤¿à¤\u0095à¤¾à¤‚à¤¶ à¤®à¤°à¥\u0080à¤\u009c à¤\u0089à¤\u009aà¤¿à¤¤ à¤«à¤¿à¤\u009cà¤¿à¤¯à¥\u008bà¤¥à¥\u0087à¤°à¥\u0087à¤ªà¥\u0080 à¤\u0095à¥\u0087 à¤¸à¤¾à¤¥ 6 à¤¸à¥\u0087 12 à¤¸à¤ªà¥\u008dà¤¤à¤¾à¤¹ à¤\u0095à¥\u0087 à¤à¥\u0080à¤¤à¤° à¤¸à¤¾à¤®à¤¾à¤¨à¥\u008dà¤¯ à¤—à¤¤à¤¿à¤µà¤¿à¤§à¤¿à¤¯à¥\u008bà¤‚ à¤®à¥\u0087à¤‚ à¤²à¥\u008cà¤\u009f à¤\u0086à¤¤à¥\u0087 à¤¹à¥\u0085à¤\u0094à¥\u008b"
          },
          {
            "question": "à¤\u0095à¥\u008dà¤¯à¤¾ à¤à¤¾à¤ª à¤\u0096à¥\u0087à¤² à¤à¥\u0080 à¤\u009aà¥\u008bà¤\u009fà¥\u008bà¤‚ à¤à¥\u0085 à¤\u0089à¤ªà¤\u009aà¤¾à¤° à¤\u0095à¤°à¤¤à¥\u0087 à¤¹à¥\u0088à¤\u0082?",
            "answer": "à¤¹à¤¾à¤‚, à¤¹à¤® à¤\u008fà¤¸à¥\u0080à¤\u008fà¤² à¤®à¤°à¤®à¥\u008dà¤®à¤¤, à¤®à¥\u0087à¤¨à¤¿à¤¸à¥\u008dà¤\u0095à¤¸ à¤\u0089à¤ªà¤\u009aà¤¾à¤° à¤\u0094à¥\u008bà¤° à¤à¥\u0086à¤² à¤\u0095à¥\u0080 à¤¸à¤à¥\u0080 à¤à¥\u0082 à¤\u009aà¥\u008bà¤\u009fà¥\u008bà¤‚ à¤\u0095à¥\u0087 à¤\u0089à¤ªà¤\u009aà¤¾à¤° à¤®à¥\u0087à¤‚ à¤µà¤¿à¤¶à¥\u0087à¤§à¤\u009cà¥\u008dà¤ñ à¤¹à¥\u0088à¤\u0082à¥\u008b"
          },
          {
            "question": "à¤\u0095à¥\u008dà¤²à¤¿à¤¨à¤¿à¤\u0095 à¤\u0095à¤¹à¤¾à¤‚ à¤¸à¥\u008dà¤¥à¤¿à¤¤ à¤¹à¥ˆ?",
            "answer": "à¤¹à¤®à¤¾à¤°à¥\u0087 à¤®à¥\u008dà¤\u009aà¥\u008dà¤¯ à¤ªà¤°à¤¾à¤®à¤°à¥\u008dà¤¶ à¤\u0095à¤\u0095à¥\u008dà¤· à¤¦à¥\u0081à¤¬à¤8 à¤®à¥\u0087à¤‚, à¤ªà¥\u008dà¤°à¥\u0080à¤®à¤¿à¤¯à¤® à¤\u009aà¤¿à¤\u0095à¤¿à¤¤à¥\u008dà¤¸à¤¾ à¤¸à¥\u008dà¤µà¤¿à¤§à¤¾à0093à¤‚ à¤\u0095à¥\u0087 à¤à¥\u0080à¤¤à¤° à¤¸à¥\u008dà¤¥à¤¿à¤¤ à¤¹à¥\u0088à¤\u0082à¥\u008b"
          },
          {
            "question": "à¤\u0095à¥\u008dà¤¯à¤¾ à¤¦à¥\u0082à¤¸à¤°à¥\u0080 à¤°à¤¾à¤¯ à¤\u0089à¤ªà¤²à¤¬à¥\u008dà¤ध à¤¹à¥ˆ?",
            "answer": "à¤¹à¤¾à¤‚, à¤¹à¤® à¤®à¤°à¥\u0080à¤\u009cà¥\u008bà¤‚ à¤\u0095à¥\u008b à¤\u0089à¤ªà¤\u009aà¤¾à¤° à¤®à¥\u0087à¤‚ à¤µà¤¿à¤शà¥\u008dà¤µà¤¾à¤¸ à¤¸à¥\u008dà¤¨à¤¿à¤¶à¥\u008dà¤\u009aà¤¿à¤¤ à¤à¤°à¤¨à¥\u0087 à¤\u0095à¥\u0087 à¤²à¤¿à¤\u008f à¤\u009cà¤\u009fà¤¿à¤² à¤\u0086à¤°à¥\u008dà¤¥à¥\u008bà¤ªà¥\u0080à¤¡à¤¿à¤\u0095 à¤®à¤¾à¤®à¤²à¥\u008bà¤‚ à¤®à¥\u0087à¤‚ à¤¦à¥\u0082à¤¸à¤°à¥\u0080 à¤°à¤¾à¤¯ à¤²à¥\u0087à¤¨à¥\u0087 à¤\u0095à¥\u0087 à¤²à¤¿à¤\u008f  à¤ªà¥\u008dà¤°à¥\u008bà¤¤à¥\u008dà¤¸à¤¾à¤¹à¤¿à¤¤ à¤\u0095à¤°à¤¤à¥\u0087 à¤¹à¥\u0088à¤\u0082à¥\u008b"
          }
        ]
      },
      "contact": {
        "badge": "à¤¸à¤‚à¤ªà¤°à¥\u008dà¤\u0095 à¤\u0095à¤°à¥\u0087à¤‚",
        "title": "à¤\u0085à¤ªà¤¨à¥\u0080 à¤¬à¥\u0081à¤\u0095 à¤\u0095à¤°à¥\u0087à¤‚",
        "titleHighlight": "à¤ªà¤°à¤¾à¤®à¤°à¥\u008dà¤¶",
        "description": "à¤°à¤¿à¤\u0095à¤µà¤°à¥\u0080 à¤\u0095à¥\u0080 à¤\u009bà¥\u008bà¤° à¤ªà¤¹à¤²à¤¾ à¤\u0095à¤¦à¤® à¤\u0089à¤ à¤¾à¤\u0082à¥\u008b à¤\u0086à¤\u009c à¤¹à¥\u0080 à¤¹à¤®à¤¾à¤°à¥\u0080 à¤µà¤¿à¤¶à¥\u0087à¤§à¤\u009cà¥\u008dà¤ñ à¤à¥\u0080à¤® à¤¸à¥\u0087 à¤¸à¤‚à¤ªà¤°à¥\u008dà¤\u0095 à¤\u0095à¤°à¥\u0087à¤‚à¥\u008b",
        "form": {
          "title": "à¤¸à¤‚à¤¦à¥\u0087à¤¶ à¤à¥\u0087à¤\u009cà¥\u0087à¤‚",
          "name": "à¤à¤¾à¤ªà¤\u0095à¤¾ à¤¨à¤¾à¤®",
          "namePlaceholder": "à¤\u0085à¤ªà¤¨à¤¾ à¤ªà¥\u0082à¤°à¤¾ à¤¨à¤¾à¤® à¤¦à¤°à¥\u008dà¤\u009c à¤\u0095à¤°à¥\u0087à¤‚\",\n"""

# Let's perform the line replacement
# Lines 797 to 888 (indices 796 to 887 inclusive)
# Note: lines[796] is 797th line. lines[888] is 889th line.
# So lines[796:888] is the range to replace.
lines[796:888] = [replacement_content]

new_content = "".join(lines)

with open("data_dump_utf8.json", "w", encoding="utf-8") as f:
    f.write(new_content)

print("\nRepair completed. Validating JSON...")
try:
    data = json.loads(new_content)
    print("SUCCESS! data_dump_utf8.json is now 100% valid JSON!")
    print("Languages in translations:", list(data['translations'].keys()))
except Exception as e:
    print("JSON PARSE ERROR:", e)
