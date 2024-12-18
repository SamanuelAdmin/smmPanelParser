from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent

uarSoftwareNames = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value, SoftwareName.ANDROID.value]
uarOperatingSystems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
userAgentRandomizer = UserAgent(software_names=uarSoftwareNames, operating_systems=uarOperatingSystems)


def getRandomUserAgent():
    return userAgentRandomizer.get_random_user_agent()