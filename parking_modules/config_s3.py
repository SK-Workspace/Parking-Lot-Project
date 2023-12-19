from configparser import ConfigParser as cfg

def config(configFilename="",configSection=""):
    config_dic={}
    if not(configFilename and configSection):
        print("Please pass valid params when calling config()")
        return None
    else:
        try:
            config_obj= cfg()
            config_obj.read(configFilename)
            for i in config_obj.items(configSection):
                config_dic[i[0]]=i[1]
            return config_dic
        except Exception as err:
            print(err)
