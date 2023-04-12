
class Permissions:
    def __init__(self, user):
        self.user = user
    
    def has_read_permission(self, model_name):
        # Check if user has read permission for the specified model
        # Return True if user has permission, False otherwise
        ...

    def has_write_permission(self, model_name):
        # Check if user has write permission for the specified model
        # Return True if user has permission, False otherwise
        ...

    def has_delete_permission(self, model_name):
        # Check if user has delete permission for the specified model
        # Return True if user has permission, False otherwise
        ...