#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test FA data structure"""

import sys
import json
from fa_calculator import calculate_fa_ratios
from stock_classifier import StockClassifier

print("="*60)
print("1. Test calculate_fa_ratios() directly:")
print("="*60)

fa_data = calculate_fa_ratios('TCB')
print(f"Type: {type(fa_data)}")
print(f"Keys: {list(fa_data.keys())}")
print(f"Has 'ratios' key: {'ratios' in fa_data}")
print(f"Has 'data' key: {'data' in fa_data}")
print(f"Has 'success' key: {'success' in fa_data}")
print(f"\nFull structure:")
print(json.dumps(fa_data, indent=2, ensure_ascii=False, default=str))

print("\n" + "="*60)
print("2. Test Stock Classifier:")
print("="*60)

classifier = StockClassifier()
result = classifier.classify_stock('TCB')

print(f"\nGrowth classification:")
growth = result['classifications']['growth']
print(f"  ROE: {growth['roe']}")
print(f"  PE: {growth['pe']}")
print(f"  NPM: {growth['npm']}")
print(f"  Category: {growth['category']}")
print(f"  Score: {growth['score']}")

print(f"\nOverall Rating: {result['overall_rating']['rating']}")

