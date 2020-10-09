import cloudscraper

class TellonymTell():
    def __init__(self, tellJSON):
        #print(tellJSON)
        self.question = tellJSON["tell"]
        self.answer = tellJSON["answer"]
        self.createdAt = tellJSON["createdAt"]
        self.likeCount = tellJSON["likesCount"]
    
    def GetQuestion(self):
        return self.question
    
    def GetAnswer(self):
        return self.answer
    
    def GetCreatedAt(self):
        return self.createdAt
    
    def GetLikeCount(self):
        return self.likeCount

class TellonymFollowing():
    def __init__(self, followerJSON):
        self.displayName = followerJSON["displayName"]
        self.username= followerJSON["username"]
        if followerJSON["aboutMe"] == None:
            self.bio = ""
        else:
            self.bio = followerJSON["aboutMe"]
        
        self.anonymousFollower = followerJSON["isFollowingAnonymous"]
        self.isActive = followerJSON["isActive"]

    def GetUsername(self):
        return self.username
    
    def GetDisplayName(self):
        return self.displayName
    
    def GetBIO(self):
        return self.bio
    
    def IsAnonymousFollower(self):
        return self.anonymousFollower
    
    def IsActive(self):
        return self.isActive
    
class TellonymFollower():
    def __init__(self, followerJSON):
        self.displayName = followerJSON["displayName"]
        self.username= followerJSON["username"]
        if followerJSON["aboutMe"] == None:
            self.bio = ""
        else:
            self.bio = followerJSON["aboutMe"]
        
        self.isActive = followerJSON["isActive"]

    def GetUsername(self):
        return self.username
    
    def GetDisplayName(self):
        return self.displayName
    
    def GetBIO(self):
        return self.bio
    
    def IsActive(self):
        return self.isActive

class TellonymUser():
    def __init__(self, profileJson, found_):
        self.profielPropeties = profileJson
        self.found = found_
        if found_ == True:
            self.cSession = cloudscraper.create_scraper()
            self.display_name = profileJson["displayName"]
            self.username = profileJson["username"]
            self.bio = profileJson["aboutMe"]
            self.avatar_url = profileJson["avatarFileName"]
            self.userid = profileJson["id"]
            self.followersCount = profileJson["followerCount"]
            self.anonymousFollowerCount = profileJson["anonymousFollowerCount"]
            self.isFollowingcount = profileJson["followingCount"]
            self.active = profileJson["isActive"]
            self.tellsCount = profileJson["tellCount"]
            self.tells = []
            self.followers = []
            self.followings = []
        else:
            return
    
    def IsProfileFound(self):
        return self.found
    
    def GetDisplayName(self):
        return self.display_name
    
    def GetUserName(self):
        return self.username
    
    def GetUserId(self):
        return self.userid
    
    def GetUserBIO(self):
        return self.bio
    
    def IsActive(self):
        return self.IsActive
    
    def GetUserFollowersCount(self):
        return self.followersCount
    
    def GetUserAnonymousFollowers(self):
        return self.anonymousFollowerCount
    
    def GetUserFollowersWithOutAnonymousFollowers(self):
        return self.followersCount - self.anonymousFollowerCount

    def GetAvatarUrlXS(self):
        return "https://userimg.tellonym.me/xs/{}".format(self.avatar_url)
    
    def GetAvatarUrlThumb(self):
        return "https://userimg.tellonym.me/thumb/{}".format(self.avatar_url)
    
    def GetTells(self):
        return self.tells
    
    def GetFollowings(self):
        return self.followings
    
    def GetFollowers(self):
        return self.followers
    
    def FetchTells(self):
        self.tells = []
        tellsUrl = "https://api.tellonym.me/answers/{}?&userId={}&limit=25&pos={}"
        posX = 0
        while True:
            tellReq = self.cSession.get(tellsUrl.format(str(self.userid), str(self.userid), str(posX)))
            respJs = tellReq.json()
            if len(respJs["answers"]) == 0:
                break
            
            for xT in respJs["answers"]:
                if xT["type"] == "AD":
                    continue
                else:
                    self.tells.append(TellonymTell(xT))

            self.tells.reverse()
            posX += 25

    
    def FetchFollowings(self):
        self.followings = []
        followersUrl = "https://api.tellonym.me/followings/id/{}?userId={}&limit=25&pos={}"
        posX = 0
        while True:
            followersReq = self.cSession.get(followersUrl.format(str(self.userid), str(self.userid), str(posX)))
            followersJs = followersReq.json()
            if len(followersJs["followings"]) == 0:
                break
            
            for xT in followersJs["followings"]:
                self.followings.append(TellonymFollowing(xT))

            self.followings.reverse()
            posX += 25
    
    def FetchFollowers(self):
        self.followers = []
        followersUrl = "https://api.tellonym.me/followers/id/{}?userId={}&limit=25&pos={}"
        posX = 0
        while True:
            followersReq = self.cSession.get(followersUrl.format(str(self.userid), str(self.userid), str(posX)))
            followersJs = followersReq.json()
            if len(followersJs["followers"]) == 0:
                break
            
            for xT in followersJs["followers"]:
                self.followers.append(TellonymFollower(xT))

            self.followers.reverse()
            posX += 25


class TellonymApi():
    def __init__(self, logging):
        self.logging = logging
        self.api_url = "https://api.tellonym.me"
        self.cSession = cloudscraper.create_scraper()
    
    def GetUser(self, username):
        request = self.cSession.get("{}/profiles/name/{}".format(self.api_url, username))
        if request.status_code == 200:
            return TellonymUser(request.json(), True)
        else:
            return TellonymUser(None, False)