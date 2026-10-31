"""
Dr. Tanvir Ahmed Chowdhury - Medicine & Diabetes Specialist Portfolio Website
Author: Doctor Portfolio App
Run this script using:
    python run.py
"""

import sys
import os

try:
    from app import app
except ImportError as e:
    print(f"Error importing Flask application: {e}")
    print("Please install requirements using: pip install -r requirements.txt")
    sys.exit(1)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 65)
    print(" Dr. Tanvir Ahmed Chowdhury - Medicine & Diabetes Specialist")
    print(" Sylhet Chamber Portfolio Website")
    print("=" * 65)
    print(f" * Server running on: http://127.0.0.1:{port}")
    print(f" * Reception Admin Panel: http://127.0.0.1:{port}/admin")
    print(f" * Press CTRL+C to quit")
    print("=" * 65)
    app.run(host='127.0.0.1', port=port, debug=True)

