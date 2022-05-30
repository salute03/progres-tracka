from project import User, Topic
import json


def create_users():
    users = []
    with open("users.txt", "r") as f:
        for line in f:
            users.append(User(*line.split(",")))
    return users


def create_topics():
    topics = []
    with open("media.txt", "r") as f:
        for line in f:
            topics.append(Topic(*line.split(",")))
    return topics


def create_lists():
    f = open("lists.json")
    return json.load(f)