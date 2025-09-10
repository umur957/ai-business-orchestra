#!/usr/bin/env python3
"""
AI Business Orchestra Test Suite
Complete testing of all workflows and scenarios
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from orchestra import BusinessOrchestra
        print("✅ Orchestra import successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_orchestra_initialization():
    """Test BusinessOrchestra initialization"""
    print("\n🧪 Testing Orchestra initialization...")
    
    try:
        from orchestra import BusinessOrchestra
        orchestra = BusinessOrchestra()
        print("✅ Orchestra initialized successfully")
        return orchestra
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return None

def test_recruitment_scenario(orchestra):
    """Test recruitment workflow"""
    print("\n🧪 Testing Recruitment Scenario...")
    
    try:
        result = orchestra.run_scenario(
            scenario_type="recruitment",
            context="Senior Python Developer position for AI company - remote work, 5+ years experience required"
        )
        
        print("✅ Recruitment scenario completed")
        print("📋 Result preview:", str(result)[:200] + "..." if len(str(result)) > 200 else str(result))
        return True
        
    except Exception as e:
        print(f"❌ Recruitment scenario failed: {e}")
        return False

def test_admin_scenario(orchestra):
    """Test administrative workflow"""
    print("\n🧪 Testing Administrative Scenario...")
    
    try:
        result = orchestra.run_scenario(
            scenario_type="admin_task",
            context="Organize company-wide quarterly meeting for 100 employees with catering and AV equipment"
        )
        
        print("✅ Admin scenario completed")
        print("📋 Result preview:", str(result)[:200] + "..." if len(str(result)) > 200 else str(result))
        return True
        
    except Exception as e:
        print(f"❌ Admin scenario failed: {e}")
        return False

def test_crisis_management_scenario(orchestra):
    """Test crisis management workflow"""
    print("\n🧪 Testing Crisis Management Scenario...")
    
    try:
        result = orchestra.run_scenario(
            scenario_type="crisis_management",
            context="Critical system outage affecting customer transactions - need immediate response plan"
        )
        
        print("✅ Crisis management scenario completed")
        print("📋 Result preview:", str(result)[:200] + "..." if len(str(result)) > 200 else str(result))
        return True
        
    except Exception as e:
        print(f"❌ Crisis management scenario failed: {e}")
        return False

def test_daily_operations_scenario(orchestra):
    """Test daily operations workflow"""
    print("\n🧪 Testing Daily Operations Scenario...")
    
    try:
        result = orchestra.run_scenario(
            scenario_type="daily_operations",
            context="Coordinate today's schedule: 3 client meetings, team standup, project review, and deadline tracking"
        )
        
        print("✅ Daily operations scenario completed")
        print("📋 Result preview:", str(result)[:200] + "..." if len(str(result)) > 200 else str(result))
        return True
        
    except Exception as e:
        print(f"❌ Daily operations scenario failed: {e}")
        return False

def test_invalid_scenario(orchestra):
    """Test error handling with invalid scenario"""
    print("\n🧪 Testing Error Handling...")
    
    try:
        result = orchestra.run_scenario(
            scenario_type="invalid_scenario",
            context="This should trigger error handling"
        )
        
        print("⚠️ Invalid scenario didn't raise error (unexpected)")
        return False
        
    except Exception as e:
        print(f"✅ Error handling works correctly: {e}")
        return True

def run_comprehensive_test():
    """Run all tests comprehensively"""
    print("="*60)
    print("🎼 AI BUSINESS ORCHESTRA - COMPREHENSIVE TEST SUITE")
    print("="*60)
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Imports
    if test_imports():
        tests_passed += 1
    
    # Test 2: Initialization
    orchestra = test_orchestra_initialization()
    if orchestra:
        tests_passed += 1
        
        # Test 3: Recruitment
        if test_recruitment_scenario(orchestra):
            tests_passed += 1
        
        # Test 4: Admin tasks
        if test_admin_scenario(orchestra):
            tests_passed += 1
        
        # Test 5: Crisis management
        if test_crisis_management_scenario(orchestra):
            tests_passed += 1
        
        # Test 6: Daily operations
        if test_daily_operations_scenario(orchestra):
            tests_passed += 1
    
    # Additional error handling test
    if orchestra:
        test_invalid_scenario(orchestra)
    
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    print(f"✅ Tests passed: {tests_passed}/{total_tests}")
    print(f"❌ Tests failed: {total_tests - tests_passed}/{total_tests}")
    print(f"📈 Success rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED! System is working correctly.")
    else:
        print(f"\n⚠️ {total_tests - tests_passed} tests failed. Check the errors above.")
    
    print(f"\n📅 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

if __name__ == "__main__":
    run_comprehensive_test()
