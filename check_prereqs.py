#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

class PrerequisiteChecker:
    def __init__(self):
        self.results = []
        self.critical_failed = False
    
    def check_python_version(self):
        version_info = sys.version_info
        version_str = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
        
        if version_info.major >= 3 and version_info.minor >= 9:
            self.results.append({
                'name': f'Python {version_str}',
                'status': 'OK',
                'critical': True,
                'details': 'FREE - Open Source'
            })
            return True
        else:
            self.results.append({
                'name': f'Python {version_str}',
                'status': 'FAIL',
                'critical': True,
                'details': 'Need 3.9+ (Download FREE python.org)'
            })
            self.critical_failed = True
            return False
    
    def check_pip(self):
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                pip_version = result.stdout.strip().split()[1]
                self.results.append({
                    'name': f'pip {pip_version}',
                    'status': 'OK',
                    'critical': True,
                    'details': 'Comes with Python - FREE'
                })
                return True
            else:
                self.results.append({
                    'name': 'pip',
                    'status': 'FAIL',
                    'critical': True,
                    'details': 'Run: python -m ensurepip'
                })
                self.critical_failed = True
                return False
        except Exception as e:
            self.critical_failed = True
            return False
    
    def check_disk_space(self):
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            free_gb = free / (1024**3)
            
            if free_gb >= 2:
                self.results.append({
                    'name': f'Disk Space ({free_gb:.1f}GB)',
                    'status': 'OK',
                    'critical': False,
                    'details': '2GB minimum needed'
                })
                return True
            else:
                self.results.append({
                    'name': f'Disk Space ({free_gb:.1f}GB)',
                    'status': 'WARN',
                    'critical': False,
                    'details': 'Low - need 2GB'
                })
                return False
        except:
            return False
    
    def check_internet(self):
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            self.results.append({
                'name': 'Internet',
                'status': 'OK',
                'critical': True,
                'details': 'Required for downloads'
            })
            return True
        except:
            self.results.append({
                'name': 'Internet',
                'status': 'FAIL',
                'critical': True,
                'details': 'Cannot reach internet'
            })
            self.critical_failed = True
            return False
    
    def check_requirements(self):
        if Path('requirements.txt').exists():
            self.results.append({
                'name': 'requirements.txt',
                'status': 'OK',
                'critical': True,
                'details': 'All packages are FREE open source'
            })
            return True
        else:
            self.results.append({
                'name': 'requirements.txt',
                'status': 'FAIL',
                'critical': True,
                'details': 'Clone repo first'
            })
            self.critical_failed = True
            return False
    
    def print_results(self):
        print("\n" + "="*70)
        print("PREREQUISITE CHECK")
        print("="*70)
        
        for result in self.results:
            symbol = "✓" if result['status'] == 'OK' else "✗"
            print(f"{symbol} {result['name']:30} [{result['status']}]")
            print(f"  → {result['details']}")
        
        print("\n" + "="*70)
    
    def run_all(self):
        self.check_python_version()
        self.check_pip()
        self.check_disk_space()
        self.check_internet()
        self.check_requirements()
        self.print_results()
        
        if self.critical_failed:
            print("\n⚠️  CRITICAL ISSUES - Fix before proceeding\n")
            for result in self.results:
                if result['critical'] and result['status'] != 'OK':
                    print(f"  • {result['name']}: {result['details']}")
            return False
        else:
            print("\n✓ ALL CHECKS PASSED\n")
            return True

if __name__ == "__main__":
    checker = PrerequisiteChecker()
    success = checker.run_all()
    sys.exit(0 if success else 1)