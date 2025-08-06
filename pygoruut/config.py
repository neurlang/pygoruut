import json
import random

class Config:
    def __init__(self):
        # Generate a random TCP port number from the range 1024-65535 (upper range)
        self.port = random.randint(1024, 65535)
    
    def serialize(self, filename, models):
        # Create the data to serialize
        data = {
            "Port": str(self.port),  # Convert port to string
            "AdminPort": str(self.port-1), # we don't use admin port
            "PolicyMaxWords": 9999999 # Policy of how many words can be processed in HTTP request
        }
        if len(models) > 0:
            data["LoadModels"] = [{"Lang": k, "File": v} for k, v in models.items()]

        # Write the data to the specified file in JSON format
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)

    def url(self, subpath):
        path = "http://127.0.0.1:" + str(self.port) + "/" + subpath
        #print(path)
        return path

class ConfigApi:
    def __init__(self, url):
        self._url = url

    def serialize(self, filename, models):
        return

    def url(self, subpath):
        path = self._url + "/" + subpath
        #print(path)
        return path
