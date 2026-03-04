"""Verify task 17: web-fetch-api.

JSONPlaceholder (https://jsonplaceholder.typicode.com) returns fixed data:
- 10 users
- 100 posts (10 per user, evenly distributed)
- Since all users have exactly 10 posts, userId=1 is typically the 'first' most prolific
  but any user with 10 posts is acceptable.
"""

import json
import sys
from pathlib import Path


def verify(workspace: Path) -> tuple[bool, str]:
    path = workspace / "results.json"
    if not path.exists():
        return False, "results.json not found"

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"Failed to parse results.json: {exc}"

    passed = 0
    checks = []

    # Check 1: total_users = 10
    total_users = data.get("total_users")
    try:
        if int(total_users) == 10:
            passed += 1
            checks.append("total_users: PASS")
        else:
            checks.append(f"total_users: FAIL (got {total_users})")
    except (TypeError, ValueError):
        checks.append(f"total_users: FAIL (got '{total_users}')")

    # Check 2: total_posts = 100
    total_posts = data.get("total_posts")
    try:
        if int(total_posts) == 100:
            passed += 1
            checks.append("total_posts: PASS")
        else:
            checks.append(f"total_posts: FAIL (got {total_posts})")
    except (TypeError, ValueError):
        checks.append(f"total_posts: FAIL (got '{total_posts}')")

    # Check 3: most_prolific_user has required fields
    user = data.get("most_prolific_user", {})
    if isinstance(user, dict) and user.get("name") and user.get("email"):
        passed += 1
        checks.append(f"prolific_user: PASS (name={user.get('name')})")
    else:
        checks.append(f"prolific_user: FAIL (missing fields, got {user})")

    # Check 4: most_prolific_post_count = 10 (all users have exactly 10)
    post_count = data.get("most_prolific_post_count")
    try:
        if int(post_count) == 10:
            passed += 1
            checks.append("post_count: PASS")
        else:
            checks.append(f"post_count: FAIL (got {post_count})")
    except (TypeError, ValueError):
        checks.append(f"post_count: FAIL (got '{post_count}')")

    ok = passed >= 3  # 3 out of 4
    summary = f"{passed}/4 checks passed. {'; '.join(checks)}"
    return ok, summary


if __name__ == "__main__":
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workspace")
    ok, msg = verify(workspace)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)
