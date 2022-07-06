from cryptography.fernet import Fernet
import orjson

"""
{
    "people":
        10000000: {
            "id": 10000000,
            "last_use": 10523007,
            "command_use_times":  1,
            "num_stories": 2
            "stories":
                {
                    1: "lorem ipsum",
                    2: "lorem-o ipsum-o"
                }
        }
}
"""


class Person:
    def __init__(self, discord_id: str, last_use: int = 0, command_use_times: int = 1, num_stories: int = 0,
                 stories=None, last_story: str = "", last_input: str = ""):
        if stories is None:
            stories = {}

        discord_id = str(discord_id)

        self.dis_id = discord_id
        self.last_use = last_use
        self.command_use_times = command_use_times
        self.num_stories = num_stories
        self.stories = stories
        self.last_story = last_story
        self.last_input = last_input

    def as_dict(self) -> dict:
        return {
            "id": self.dis_id, "last_use": self.last_use, "command_use_times": self.command_use_times,
            "num_stories": self.num_stories, "stories": self.stories, "last_story": self.last_story,
            "last_input": self.last_input
        }


class Database:
    def __init__(self, file_path: str, password):
        self.data = {}
        self.cryptography = Fernet(password)
        self.file_path = file_path

    def import_content(self):
        self.data.clear()
        with open(self.file_path, "rb") as f:
            content = self.cryptography.decrypt(f.read())
        data = orjson.loads(content)
        for id_ in list(data["people"]):
            person = data["people"][id_]
            self.data[id_] = \
                Person(person["id"], person["last_use"], person["command_use_times"], person["num_stories"],
                       person["stories"], person["last_story"], person["last_input"])

    def new_user(self, user_id: int):
        user_id = str(user_id)
        self.data[user_id] = Person(user_id)
        self.export_content()

    def export_content(self):
        data = {"people": {}}
        for person in self.data.values():
            data["people"][person.dis_id] = person.as_dict()

        with open(self.file_path, "wb") as f:
            f.write(self.cryptography.encrypt(orjson.dumps(data)))

    def reload(self):
        self.export_content()
        self.import_content()

    def has(self, auth_id):
        return True if str(auth_id) in self.data else False

    def get(self, auth_id) -> Person:
        self.reload()
        return self.data[str(auth_id)]


if __name__ == '__main__':
    db = Database("../../dynamic_files/data.txt", b'ETl8CaMqlMOKrFIp1Lzjj5_ZG6KVXRe4PitX8_yBkVo=')
    db.new_user(1)
    db.new_user(2)
    db.import_content()


