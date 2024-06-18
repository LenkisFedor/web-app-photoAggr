from db import db
    
def get_next_sequence_value(collection_name):
    max_id = db[collection_name].find_one({}, sort=[('_id', -1)])['_id']
    return max_id + 1 if max_id is not None else 1