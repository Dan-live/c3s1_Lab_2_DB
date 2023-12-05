# ControllerBooking
############################################################################
class ControllerAnalytics:
    def __init__(self, model_analytics, view_analytics):
        self.model_analytics = model_analytics
        self.view_analytics = view_analytics

    def room_occupancy(self):
        # Get analytical data
        room_occupancy_data = self.model_analytics.room_occupancy()

        # Show results
        if room_occupancy_data:
            self.view_analytics.display_room_occupancy(room_occupancy_data)
        else:
            print("Error when performing analytics")

    def number_of_orders(self):
        # Do analytics
        number_of_orders_data = self.model_analytics.number_of_orders()

        # Show results
        if number_of_orders_data:
            self.view_analytics.display_number_of_orders(number_of_orders_data)
        else:
            print("Error when performing room occupancy analytics")

    def client_analytics(self):
        # Do analytics
        client_analytics_data = self.model_analytics.client_analytics()

        # Show results
        if client_analytics_data is not None:
            self.view_analytics.display_client_analytics(client_analytics_data)
        else:
            print("Error when performing analytics")