from requests import Session
from datetime import datetime

class ForumExbo:
	def __init__(self) -> None:
		self.api = "https://forum.exbo.ru"
		self.session = Session()
		self.session.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
			"Content-Type": "application/json"}
		self.token = None
		self.user_id = None
		self.csrf_token = None
		self.flarum_session = None
		self.get_cookies()

	def _post(self, endpoint: str, data: dict) -> dict:
		return self.session.post(
			f"{self.api}{endpoint}", json=data).json()

	def _patch(self, endpoint: str, data: dict) -> dict:
		return self.session.patch(
			f"{self.api}{endpoint}", json=data).json()

	def _get(self, endpoint: str, params: dict = None) -> dict:
		return self.session.get(
			f"{self.api}{endpoint}", params=params or {}).json()

	def get_cookies(self) -> None:
		response = self.session.get(self.api)
		self.csrf_token = response.headers["X-CSRF-Token"]
		self.flarum_session = response.cookies["flarum_session"]
		self.session.headers["x-csrf-token"] = self.csrf_token
		self.session.headers["cookie"] = f"flarum_session={
			self.flarum_session}"

	def login_with_flarum(
			self,
			flarum_session: str,
			flarum_remember: str) -> tuple:
		self.flarum_session = flarum_session
		self.flarum_remember = flarum_remember
		self.session.headers["cookie"] = f"flarum_remember={
			self.flarum_remember}; flarum_session={
			self.flarum_session}"
		return self.flarum_session, self.flarum_remember

	def like_comment(self, comment_id: int) -> dict:
		data = {
			"data": {
				"type": "posts",
				"id": comment_id,
						"attributes": {
							"isLiked": True
						}
			}
		}
		return self._patch(f"/api/posts/{comment_id}", data)

	def unlike_comment(self, comment_id: int) -> dict:
		data = {
			"data": {
				"type": "posts",
				"id": comment_id,
						"attributes": {
							"isLiked": False
						}
			}
		}
		return self._patch(f"/api/posts/{comment_id}", data)

	def react_comment(
			self, comment_id: int, reaction_id: int = 5) -> dict:
		data = {
			"data": {
				"type": "posts",
				"id": comment_id,
						"attributes": {
							"reaction": reaction_id
						}
			}
		}
		return self._patch(f"/api/posts/{comment_id}", data)

	def comment(self, discussion_id: int, content: str) -> dict:
		data = {
			"data": {
				"type": "posts",
				"attributes": {"content": content},
						"relationships": {
							"discussion": {
								"data": {
									"type": "discussions",
									"id": discussion_id
								}
							}
				}
			}
		}
		return self._post("/api/posts", data)

	def edit_comment(
			self,
			comment_id: int,
			content: str = None,
			is_hidden: bool = False) -> dict:
		data = {
			"data": {
				"type": "posts",
				"id": comment_id,
						"attributes": {}
			}
		}
		if content:
			data["data"]["attributes"]["content"] = content
		if is_hidden:
			data["data"]["attributes"]["isHidden"] = is_hidden
		return self._patch(f"/api/posts/{comment_id}", data)

	def report_comment(
			self,
			comment_id: int,
			reason: str,
			detail: str = None) -> dict:
		data = {
			"data": {
				"type": "flags",
				"attributes": {
					"reason": reason
				},
				"relationships": {
					"user": {
						"data": {
							"type": "users",
									"id": self.user_id
						}
					},
					"post": {
						"data": {
							"type": "posts",
									"id": comment_id
						}
					}
				}
			}
		}
		if detail:
			data["data"]["attributes"]["reasonDetail"] = detail
		return self._post("/api/flags", data)

	def follow_discussion(self, discussion_id: int) -> dict:
		data = {
			"data": {
				"type": "discussions",
				"id": discussion_id,
						"attributes": {
							"subscription": "follow"
						}
			}
		}
		return self._patch(f"/api/discussions/{discussion_id}", data)

	def unfollow_discussion(self, discussion_id: int) -> dict:
		data = {
			"data": {
				"type": "discussions",
				"id": discussion_id,
						"attributes": {
							"subscription": None
						}
			}
		}
		return self._patch(f"/api/discussions/{discussion_id}", data)

	def get_user_discussions(
			self,
			username: str,
			include: str = "user,lastPostedUser,mostRelevantPost,mostRelevantPost.user,tags,tags.parent,firstPost,lastPost",
			sort: str = "-createdAt",
			offset: int = 0) -> dict:
		params = {
			"include": include,
			"filter[q]": f"author:{username}",
			"sort": sort,
			"page[offset]": offset
		}
		return self._get("/api/discussions", params)

	def get_user_mentioned(
			self,
			user_id: int,
			offset: int = 0,
			limit: int = 20,
			sort: str = "-createdAt") -> dict:
		params = {
			"filter[type]": "comment",
			"filter[mentioned]": user_id,
			"sort": sort,
			"page[offset]": offset,
			"page[limit]": limit
		}
		return self._get("/api/posts", params)

	def get_user_comments(
			self,
			username: str,
			offset: int = 0,
			limit: int = 20,
			sort: str = "-createdAt") -> dict:
		params = {
			"filter[type]": "comment",
			"filter[author]": username,
			"sort": sort,
			"page[offset]": offset,
			"page[limit]": limit
		}
		return self._get("/api/posts", params)

	def get_user_info(self, user_id: int) -> dict:
		return self._get(f"/api/users/{user_id}")

	def get_notifications(self, offset: int = 0) -> dict:
		params = {"page[offset]": offset}
		return self._get("/api/notifications", params)

	def get_discussions(
			self,
			include: str = "user,lastPostedUser,tags,tags.parent,firstPost,lastPost",
			sort: str = "-createdAt",
			offset: int = 20) -> dict:
		params = {
			"include": include,
			"sort": sort,
			"page[offset]": offset
		}
		return self._get("/api/discussions", params)

	def mark_discussions_read(self) -> dict:
		data = {
			"data": {
				"type": "users",
				"id": self.user_id,
						"attributes": {
							"markedAllAsReadAt": f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"
						}
			}
		}
		return self._patch(f"/api/users/{self.user_id}", data)

	def ignore_user(self, user_id: int) -> dict:
		data = {
			"data": {
				"type": "users",
				"id": user_id,
						"attributes": {
							"ignored": True
						}
			}
		}
		return self._patch(f"/api/users/{user_id}", data)

	def unignore_user(self, user_id: int) -> dict:
		data = {
			"data": {
				"type": "users",
				"id": user_id,
						"attributes": {
							"ignored": False
						}
			}
		}
		return self._patch(f"/api/users/{user_id}", data)

	def reset_password(self, email: str) -> dict:
		data = {
			"email": email
		}
		return self._post("/forgot", data)
