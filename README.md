<h1>
  <img src="https://forum.exbo.ru/assets/logo-mc7qzhak.png" width="100" style="vertical-align:middle;" />
  forum_exbo.py
</h1>

> Web-API for [forum.exbo.ru](https://forum.exbo.ru) website which is the official [stalcraft](https://store.steampowered.com/app/1818450/STALCRAFT) forum

## Usage

```python
from forum_exbo import ForumExbo

exbo = ForumExbo()
```

On initialization, the client automatically fetches the CSRF token and session cookie required for all requests.

### Authentication

**Option 1 — Cookie-based login** (recommended):

```python
exbo.login_with_flarum(
    flarum_session="your_flarum_session",
    flarum_remember="your_flarum_remember"
)
```

You can obtain these values from your browser's cookies after logging in manually.

---

## Methods

### Comments

| Method | Description |
|---|---|
| `comment(discussion_id, content)` | Post a comment in a discussion |
| `edit_comment(comment_id, content, is_hidden)` | Edit or hide a comment |
| `like_comment(comment_id)` | Like a comment |
| `unlike_comment(comment_id)` | Remove like from a comment |
| `react_comment(comment_id, reaction_id)` | React to a comment (default reaction: `5`) |
| `report_comment(comment_id, reason, detail)` | Report a comment with an optional detail |

### Discussions

| Method | Description |
|---|---|
| `get_discussions(include, sort, offset)` | Fetch a list of discussions |
| `get_user_discussions(username, include, sort, offset)` | Fetch discussions created by a user |
| `follow_discussion(discussion_id)` | Follow a discussion |
| `unfollow_discussion(discussion_id)` | Unfollow a discussion |
| `mark_discussions_read()` | Mark all discussions as read |

### Posts / Comments Search

| Method | Description |
|---|---|
| `get_user_comments(username, offset, limit, sort)` | Fetch comments made by a user |
| `get_user_mentioned(user_id, offset, limit, sort)` | Fetch posts where a user was mentioned |

### Users

| Method | Description |
|---|---|
| `get_user_info(user_id)` | Get public info about a user |
| `ignore_user(user_id)` | Ignore a user |
| `unignore_user(user_id)` | Unignore a user |
| `reset_password(email)` | Send a password reset email |

### Notifications

| Method | Description |
|---|---|
| `get_notifications(offset)` | Fetch notifications |

---

## Examples

```python
# Post a comment
exbo.comment(discussion_id=123, content="Hello!")

# Like a comment
exbo.like_comment(comment_id=456)

# React to a comment
exbo.react_comment(comment_id=456, reaction_id=3)

# Report a comment
exbo.report_comment(
    comment_id=456,
    reason="spam",
    detail="This user is posting ads"
)

# Get discussions by a user
exbo.get_user_discussions(username="john_doe")

# Follow a discussion
exbo.follow_discussion(discussion_id=123)

# Mark all discussions as read
exbo.mark_discussions_read()

# Ignore a user
exbo.ignore_user(user_id=789)

# Fetch notifications
exbo.get_notifications(offset=0)
```

---

## Notes

- Authentication relies on session cookies. Keep your `flarum_session` and `flarum_remember` values private.
- `self.user_id` is not set automatically — methods like `mark_discussions_read` and `report_comment` require it to be set manually after login.
