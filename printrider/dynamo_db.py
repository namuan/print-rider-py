class DynamoDatabase:
    dt = None

    def init_app(self, db_client, table_name):
        self.dt = db_client.Table(table_name)

    def save(self, item):
        self.dt.put_item(Item=item)

    def load(self, item_id):
        return self.dt.get_item(
            Key={
                'id': item_id
            }
        )
