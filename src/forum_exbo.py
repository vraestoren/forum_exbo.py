from requests import Session
from datetime import datetime

class ForumExbo:
    def __init__(self) -> None:
        self.api = "https://forum.exbo.ru"
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
            "Content-Type": "application/json"
        }
        self.token = None
        self.user_id = None
        self.get_cookies()
        
    def get_cookies(self) -> None:
        response =  self.session.get(self.api)
        self.csrf_token = response.headers["X-CSRF-Token"]
        self.flarum_session = response.cookies["flarum_session"]
        self.self.session.headers["x-csrf-token"] = self.csrf_token
        self.session.headers["cookie"] = f"flarum_session={self.flarum_session}"
    
    def login_with_flarum(
            self,
            flarum_session: str,
            flarum_remember: str) -> str:
        self.flarum_session = flarum_session
        self.flarum_remember = self.flarum_remember
        self.session.headers["cookie"] = f"flarum_remember={self.flarum_remember}; flarum_session={self.flarum_session}"
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
        }
        return self.session.post(
            f"{self.api}/api/posts/{comment_id}", json=data).json()

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
        return self.session.post(
            f"{self.api}/api/posts/{comment_id}", json=data).json()

    def react_comment(self, comment_id: int, reaction_id: int = 5) -> dict:
        data = {
            "data": {
                "type": "posts",
                "id": comment_id,
                "attributes": {
                    "reaction": reaction_id
                }
            }
        }
        return self.session.post(
            f"{self.api}/api/posts/{comment_id}",
            json=data).json()

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
        return self.session.post(
            f"{self.api}/api/posts", json=data).json()

    def edit_comment(
            self,
            comment_id: int,
            content: str = None,
            is_hidden: bool = False) -> dict:
        data = {
            "data": {
                "type": "posts",
                "id": comment_id
            }
        }
        if content:
            data["attributes"] = {"content": content}
        if is_hidden:
            data["attributes"] = {"isHidden": is_hidden}
        return self.session.post(
            f"{self.api}/api/posts/{comment_id}",
            json=data).json()

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
            data["attributes"] = {"reasonDetail": detail}
        return self.session.post(
            f"{self.api}/api/flags", json=data).json()

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
        return self.session.post(
            f"{self.api}/api/discussions/{discussion_id}",
            json=data).json()

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
        return self.session.post(
            f"{self.api}/api/discussions/{discussion_id}",
            json=data).json()

    def get_user_discussions(
            self,
            username: str,
            include: str = "user,lastPostedUser,mostRelevantPost,mostRelevantPost.user,tags,tags.parent,firstPost,lastPost", 
            sort: str = "-createdAt", 
            offset: int = 0) -> dict:
        return self.session.get(
            f"{self.api}/api/discussions?include={include}&filter[q]=author:{username}&sort={sort}&page[offset]={offset}").json()

    def get_user_mentioned(
            self,
            user_id: int,
            offset: int = 0,
            limit: int = 20,
            sort: str = "-createdAt") -> dict:
        return self.session.get(
            f"{self.api}/api/posts?filter[type]=comment&filter[mentioned]={user_id}&page[offset]={offset}&page[limit]={limit}&sort={sort}").json()
    
    def get_user_comments(
            self,
            username: str,
            offset: int = 0,
            limit: int = 20,
            sort: str = "-createdAt") -> dict:
        return self.session.get(
            f"{self.api}/api/posts?filter[author]={username}&filter[type]=comment&page[offset]={offset}&page[limit]={limit}&sort={sort}").json()

    def get_user_info(self, user_id: int) -> dict:
        return self.session.get(
            f"{self.api}/api/users/{user_id}").json()

    def get_notifications(self, offset: int = 0) -> dict:
        return self.session.get(
            f"{self.api}/api/notifications?page[offset]={offset}").json()

    def get_discussions(
            self,
            include: str = "user,lastPostedUser,tags,tags.parent,firstPost,firstPost,lastPost",
            sort: str = "-createdAt",
            offset: int = 20) -> dict:
        return self.session.get(
            f"{self.api}/api/discussions?include={include}&sort={sort}&page[offset]={offset}").json()

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
        return self.session.post(
            f"{self.api}/api/users/{self.user_id}", 
            json=data).json()

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
        return self.session.post(
            f"{self.api}/api/users/{user_id}",
            json=data).json()


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
        return self.session.post(
            f"{self.api}/api/users/{user_id}",
            json=data).json()

    def reset_password(self, email: str) -> dict:
        data = {
            "email": email
        }
        return self.session.post(
            f"{self.api}/forgot", json=data).json()
