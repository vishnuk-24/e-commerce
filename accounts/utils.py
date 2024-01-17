"""Accounts utils.py"""

def get_pic_path(instance, filename):
    return "profile_pic/{}/{}.{}".format((instance.user.username), (instance.user.username), filename.split(".")[-1])
