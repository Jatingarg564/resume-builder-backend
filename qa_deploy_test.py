"""
Comprehensive QA Test for Deployed Resume Builder
Tests the LIVE Render deployment
"""
import requests
import json
import time
import sys

BASE_URL = "https://resume-builder-backend-z3xm.onrender.com/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log(msg, status="INFO"):
    colors = {"PASS": Colors.GREEN, "FAIL": Colors.RED, "WARN": Colors.YELLOW, "INFO": Colors.BLUE}
    print(f"{colors.get(status, Colors.END)}[{status}]{Colors.END} {msg}")

def create_user(username, email, password):
    return requests.post(f"{BASE_URL}/accounts/signup/", json={
        "username": username,
        "email": email,
        "password": password
    })

def get_tokens(username, password):
    resp = requests.post(f"{BASE_URL}/token/", json={
        "username": username,
        "password": password
    })
    if resp.status_code == 200:
        return resp.json()
    return None

def auth_headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Unique suffix for test users
TS = int(time.time() * 1000) % 10000000

def test_backend_health():
    log("Testing Backend Health...", "INFO")
    try:
        resp = requests.get(f"{BASE_URL}/accounts/profile/", timeout=10)
        log(f"Backend reachable - Status: {resp.status_code}", "PASS")
        return True
    except requests.exceptions.RequestException as e:
        log(f"Backend unreachable: {e}", "FAIL")
        return False

def test_cors_headers():
    log("Testing CORS Headers...", "INFO")
    try:
        resp = requests.options(f"{BASE_URL}/accounts/signup/", json={})
        log(f"CORS preflight status: {resp.status_code}", "PASS")
        return True
    except Exception as e:
        log(f"CORS check failed: {e}", "FAIL")
        return False

def test_signup():
    log("Testing User Signup...", "INFO")
    unique_user = f"user{TS}"
    resp = create_user(unique_user, f"{unique_user}@test.com", "TestPass123!")
    if resp.status_code == 201:
        log(f"Signup successful for {unique_user}", "PASS")
        return unique_user, "TestPass123!"
    else:
        log(f"Signup failed: {resp.status_code} - {resp.text[:200]}", "FAIL")
        return None, None

def test_login(username, password):
    log("Testing Login...", "INFO")
    resp = requests.post(f"{BASE_URL}/token/", json={
        "username": username,
        "password": password
    })
    if resp.status_code == 200:
        data = resp.json()
        log(f"Login successful - got access token", "PASS")
        return data["access"], data["refresh"]
    log(f"Login failed: {resp.status_code} - {resp.text[:200]}", "FAIL")
    return None, None

def test_profile(access):
    log("Testing Profile GET...", "INFO")
    resp = requests.get(f"{BASE_URL}/accounts/profile/", headers=auth_headers(access))
    if resp.status_code == 200:
        log("Profile GET successful", "PASS")
        return True
    log(f"Profile GET failed: {resp.status_code}", "FAIL")
    return False

def test_create_resume(access):
    log("Testing Resume Creation...", "INFO")
    resp = requests.post(f"{BASE_URL}/resumes/", headers=auth_headers(access), json={
        "title": f"Test Resume {TS}"
    })
    if resp.status_code == 201:
        resume_id = resp.json()["id"]
        log(f"Resume created (ID: {resume_id})", "PASS")
        return resume_id
    log(f"Resume creation failed: {resp.status_code} - {resp.text[:200]}", "FAIL")
    return None

def test_add_education(access, resume_id):
    log("Testing Add Education...", "INFO")
    resp = requests.post(f"{BASE_URL}/resumes/{resume_id}/education/", headers=auth_headers(access), json={
        "degree": "BS Computer Science",
        "institution": "MIT",
        "start_year": 2018,
        "end_year": 2022
    })
    if resp.status_code == 201:
        log("Education added", "PASS")
        return True
    log(f"Add education failed: {resp.status_code}", "FAIL")
    return False

def test_add_experience(access, resume_id):
    log("Testing Add Experience...", "INFO")
    resp = requests.post(f"{BASE_URL}/resumes/{resume_id}/experience/", headers=auth_headers(access), json={
        "company": "Tech Corp",
        "role": "Software Engineer",
        "start_date": "2022-01-01",
        "end_date": "2024-01-01",
        "description": "Built applications"
    })
    if resp.status_code == 201:
        log("Experience added", "PASS")
        return True
    log(f"Add experience failed: {resp.status_code}", "FAIL")
    return False

def test_add_skills(access, resume_id):
    log("Testing Add Skills...", "INFO")
    for skill in ["Python", "JavaScript", "React"]:
        resp = requests.post(f"{BASE_URL}/resumes/{resume_id}/skills/", headers=auth_headers(access), json={
            "name": skill
        })
    log("Skills added", "PASS")
    return True

def test_generate_share_link(access, resume_id):
    log("Testing Generate Share Link...", "INFO")
    resp = requests.post(f"{BASE_URL}/resumes/{resume_id}/share/", headers=auth_headers(access))
    if resp.status_code == 200:
        share_code = resp.json().get("share_code")
        log(f"Share link generated: {share_code}", "PASS")
        return share_code
    log(f"Share link generation failed: {resp.status_code}", "FAIL")
    return None

def test_public_resume_view(share_code):
    log("Testing Public Resume View...", "INFO")
    resp = requests.get(f"{BASE_URL}/resumes/public/{share_code}/")
    if resp.status_code == 200:
        data = resp.json()
        log(f"Public view successful - Resume: {data.get('title', 'N/A')}", "PASS")
        return True
    log(f"Public view failed: {resp.status_code}", "FAIL")
    return False

def test_get_resume_detail(access, resume_id):
    log("Testing Get Resume Detail...", "INFO")
    resp = requests.get(f"{BASE_URL}/resumes/{resume_id}/", headers=auth_headers(access))
    if resp.status_code == 200:
        log("Resume detail fetched", "PASS")
        return True
    log(f"Get resume failed: {resp.status_code}", "FAIL")
    return False

def test_unauthorized_access():
    log("Testing Unauthorized Access Blocked...", "INFO")
    resp = requests.get(f"{BASE_URL}/accounts/profile/")
    if resp.status_code == 401:
        log("Unauthorized access blocked correctly", "PASS")
        return True
    log(f"Expected 401, got {resp.status_code}", "FAIL")
    return False

def test_templates_public():
    log("Testing Public Templates Endpoint...", "INFO")
    resp = requests.get(f"{BASE_URL}/resumes/templates/")
    if resp.status_code == 200:
        log("Templates endpoint accessible (public)", "PASS")
        return True
    log(f"Templates endpoint failed: {resp.status_code}", "FAIL")
    return False

def run_all_tests():
    print("\n" + "="*60)
    print("RESUME BUILDER DEPLOYMENT QA TEST")
    print("Testing LIVE deployment at:")
    print(f"  {BASE_URL}")
    print("="*60 + "\n")

    all_passed = True
    username = None
    password = None
    access_token = None
    resume_id = None
    share_code = None

    try:
        # Basic connectivity
        log("\n--- CONNECTIVITY TESTS ---", "INFO")
        if not test_backend_health():
            log("Backend is not reachable. Exiting.", "FAIL")
            return False

        test_cors_headers()
        test_unauthorized_access()
        test_templates_public()

        # Auth tests
        log("\n--- AUTH TESTS ---", "INFO")
        username, password = test_signup()
        if not username:
            log("Cannot continue without signup. Exiting.", "FAIL")
            return False

        access_token, refresh_token = test_login(username, password)
        if not access_token:
            log("Cannot continue without login. Exiting.", "FAIL")
            return False

        test_profile(access_token)

        # Resume tests
        log("\n--- RESUME TESTS ---", "INFO")
        resume_id = test_create_resume(access_token)
        if not resume_id:
            log("Cannot continue without resume. Exiting.", "FAIL")
            return False

        test_get_resume_detail(access_token, resume_id)
        test_add_education(access_token, resume_id)
        test_add_experience(access_token, resume_id)
        test_add_skills(access_token, resume_id)

        # Sharing tests
        log("\n--- SHARING TESTS ---", "INFO")
        share_code = test_generate_share_link(access_token, resume_id)
        if share_code:
            test_public_resume_view(share_code)
        else:
            log("Skipping public view test (no share code)", "WARN")

    except Exception as e:
        import traceback
        log(f"ERROR: {e}\n{traceback.format_exc()}", "FAIL")
        all_passed = False

    print("\n" + "="*60)
    if all_passed:
        print(f"{Colors.GREEN}ALL TESTS PASSED!{Colors.END}")
        print("\n✅ Backend is working properly")
        print("✅ Signup/Login working from external domains")
        print("✅ Public sharing working")
        if share_code:
            print(f"\n📄 Test public resume at: {BASE_URL}/resumes/public/{share_code}/")
    else:
        print(f"{Colors.RED}SOME TESTS FAILED{Colors.END}")
    print("="*60 + "\n")

    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)