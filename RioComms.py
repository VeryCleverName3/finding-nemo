from networktables import NetworkTables

class RioComms:


    def __init__(self, url):
        self.url = url

        NetworkTables.initialize(server=url)

    
    def send(self, tableName, key, value):
        table = NetworkTables.getTable(tableName)

        table.putNumber(key, value)

    def receive(self, tableName, key, defaultValue):
        table = NetworkTables.getTable(tableName)
        return table.getNumber(key, defaultValue)
