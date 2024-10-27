import platform,distro

def getSysType():
    sys_type = platform.system()
    match sys_type:
        case "Windows":
            pass
        case "Linux":
            release_type = distro.id()
        case _:
            return "Unknown System Type"


print(getSysType())