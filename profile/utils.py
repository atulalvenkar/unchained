class ProfileUtils:

    @staticmethod
    def records_exist(query_set):
        if (query_set.count() == 0):
            return None
        else:
            return query_set[0]

