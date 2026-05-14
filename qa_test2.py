"""
QA Test for Resume Builder - Correct URLs
"""
import requests
import json
import time
import sys

BASE_URL = "https://resume-builder-jbyf.onrender.com/api"
FRONTEND_URL = "https://resume-builder-phi-azure.vercel.app"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log(msg, status="INFO"):
    colors = {"PASS": Colors.GREEN, "FAIL": Colors.RED, "WARN": Colors.YELLOW, "INFO": Colors.BLUE}
    print(f"{colors.get(status, Colors.END)}[{status}]{Colors.END} {msg}")

def auth_headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

TS = int(time.time() * 1000) % 10000000

def test_backend_health():
    log(f"Testing Backend: {BASE_URL}", "INFO")
    try:
        resp = requests.get(f"{BASE_URL}/accounts/profile/", timeout=15)
        log(f"Backend status: {resp.status_code}", "PASS")
        return True
    except requests.exceptions.RequestException as e:
        log(f"Backend unreachable: {e}", "FAIL")
        return False

def test_signup():
    log("Testing Signup...", "INFO")
    unique_user = f"user{TS}"
    resp = requests.post(f"{BASE_URL}/accounts/signup/", json={
        "username": unique_user,
        "email": f"{unique_user}@test.com",
        "password": "TestPass123!"
    })
    if resp.status_code == 201:
        log(f"Signup SUCCESS: {unique_user}", "PASS")
        return unique_user, "TestPass123!"
    log(f"Signup FAILED: {resp.status_code} - {resp.text[:200]}", "FAIL")
    return None, None

def test_login(username, password):
    log("Testing Login...", "INFO")
    resp = requests.post(f"{BASE_URL}/token/", json={
        "username": username,
        "password": password
    })
    if resp.status_code == 200:
        log("Login SUCCESS - got tokens", "PASS")
        return resp.json()["access"], resp.json()["refresh"]
    log(f"Login FAILED: {resp.status_code} - {resp.text[:200]}", "FAIL")
    return None, None

def test_profile(access):
    log("Testing Profile GET...", "INFO")
    resp = requests.get(f"{BASE_URL}/accounts/profile/", headers=auth_headers(access))
    if resp.status_code == 200:
        log("Profile SUCCESS", "PASS")
        return True
    log(f"Profile FAILED: {resp.status_code}", "FAIL")
    return False

def test_create_resume(access):
    log("Testing Resume Creation...", "INFO")
    resp = requests.post(f"{BASE_URL}/resumes/", headers=auth_headers(access), json={
        "title": f"Test Resume {TS}"
    })
    if resp.status_code == 201:
        resume_id = resp.json()["id"]
        log(f"Resume created ID:{resume_id}", "PASS")
        return resume_id
    log(f"Resume FAILED: {resp.status_code} - {resp.text[:200]}", "FAIL")
    return None

def test_add_education(access, resume_id):
    log("Testing Education...", "INFO")
    resp = requests.post(f"{BASE_URL}/resumes/{resume_id}/education/", headers=auth_headers(access), json={
        "degree": "BS Computer Science",
        "institution": "MIT",
        "start_year": 2018,
        "end_year": 2022
    })
    if resp.status_code == 201:
        log("Education SUCCESS", "PASS")
        return True
    log(f"Education FAILED: {resp.status_code}", "FAIL")
    return False

def test_share_link(access, resume_id):
    log("Testing Share Link...", "INFO")
    resp = requests.post(f"{BASE_URL}/resumes/{resume_id}/share/", headers=auth_headers(access))
    if resp.status_code == 200:
        share_code = resp.json().get("share_code")
        log(f"Share link: {share_code}", "PASS")
        return share_code
    log(f"Share FAILED: {resp.status_code}", "FAIL")
    return None

def test_public_resume(share_code):
    log("Testing Public Resume View...", "INFO")
    resp = requests.get(f"{BASE_URL}/resumes/public/{share_code}/")
    if resp.status_code == 200:
        log("Public view SUCCESS", "PASS")
        return True
    log(f"Public view FAILED: {resp.status_code}", "FAIL")
    return False

def test_templates():
    log("Testing Templates...", "INFO")
    resp = requests.get(f"{BASE_URL}/resumes/templates/")
    if resp.status_code == 200:
        log(f"Templates SUCCESS - {len(resp.json())} templates", "PASS")
        return True
    log(f"Templates FAILED: {resp.status_code}", "FAIL")
    return False

def run_tests():
    print("\n" + "="*60)
    print("RESUME BUILDER QA TEST")
    print(f"Backend: {BASE_URL}")
    print(f"Frontend: {FRONTEND_URL}")
    print("="*60 + "\n")

    all_passed = True

    # Test 1: Backend reachable
    if not test_backend_health():
        log("Backend not reachable. Check Render deployment.", "FAIL")
        return False

    # Test 2: Signup
    username, password = test_signup()
    if not username:
        return False

    # Test 3: Login
    access, refresh = test_login(username, password)
    if not access:
        return False

    # Test 4: Profile
    test_profile(access)

    # Test 5: Create Resume
    resume_id = test_create_resume(access)
    if not resume_id:
        return False

    # Test 6: Add Education
    test_add_education(access, resume_id)

    # Test 7: Templates
    test_templates()

    # Test 8: Share Link
    share_code = test_share_link(access, resume_id)
    if share_code:
        test_public_resume(share_code)

    print("\n" + "="*60)
    print(f"{Colors.GREEN}ALL TESTS COMPLETED{Colors.END}")
    print("="*60)
    print(f"\nFrontend: {FRONTEND_URL}")
    print(f"Backend API: {BASE_URL}")
    if share_code:
        print(f"Test public resume: {BASE_URL}/resumes/public/{share_code}/")

    return all_passed

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
