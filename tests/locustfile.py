# """
# _summary
# """
# from locust import HttpUser, task, between

# class User(HttpUser):
#     """
#     _summary
#     """
#     wait_time = between(2, 5)

#     @task
#     def get_double(self):
#         """
#         _summary
#         """
#         self.client.get("/5")
