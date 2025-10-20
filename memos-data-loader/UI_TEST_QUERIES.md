# Dashboard UI Test Queries

## Problem
Data loads successfully via API but not visible in Dashboard UI.

## Likely Cause
**user_id mismatch**: We're using `security_scanner_001` but your Dashboard account has a different user_id.

## Unique Factoids from Loaded Data

### From SSH Scan (loaded successfully):
- **IP Address:** `172.32.0.216`
- **SSH Version:** `OpenSSH 9.2p1 Debian 2+deb12u6`
- **Port:** `22`
- **Failed logins:** root, admin, user, guest, test, ubuntu, debian

### From Port Scan (not loaded yet):
- **IP:** `10.25.0.58`
- **Database:** PostgreSQL on port `5433`
- **Version:** `14.7-14.9`

### From API Discovery (not loaded yet):
- **API Name:** `OffZone API v0.1.0`
- **Endpoints:** `/docs`, `/redoc`, `/openapi.json`

---

## Test in Dashboard UI

### Where to test:
1. Go to https://memos-dashboard.openmem.net/
2. Find **Chat** or **Conversation** interface (not Knowledge Graph)
3. Try these queries:

### Test Queries (try these in chat):
```
What do you know about IP 172.32.0.216?
```

```
Tell me about OpenSSH 9.2p1 Debian
```

```
What SSH information do you have?
```

```
What's on port 22?
```

---

## If Queries Return Nothing

**Problem:** Data is under user_id `security_scanner_001` but Dashboard UI is looking at your account's user_id.

**Solution:** We need to find your actual user_id from the Dashboard.

### How to find your user_id:
1. In Dashboard, go to Profile/Settings
2. Look for User ID or Account ID
3. It might look like: `user_123abc` or a UUID like `550e8400-e29b-41d4-a716-446655440000`

### Once you have it:
Update the `.env` file to use YOUR user_id instead of our test one.

---

## Alternative: Load with Your User ID

If you find your real user_id, we can reload the data:

```bash
# Update .env file with your actual user_id
# Then reload:
python src/simple_loader.py --file test-samples/sample-ssh-scan.txt --user-id YOUR_REAL_USER_ID
```
