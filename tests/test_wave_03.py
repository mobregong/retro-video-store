from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from datetime import datetime, timedelta

VIDEO_TITLE = "A Brand New Video"
VIDEO_ID = 1
VIDEO_INVENTORY = 1
VIDEO_RELEASE_DATE = "01-01-2001"

CUSTOMER_NAME = "A Brand New Customer"
CUSTOMER_ID = 1
CUSTOMER_POSTAL_CODE = "12345"
CUSTOMER_PHONE = "123-123-1234"

DATE_TODAY = datetime.utcnow() + timedelta(days=16)


# def test_get_video_history_by_customer(client, one_checked_in_video ):
#     response =  client.get("/rentals/1/history")

def test_get_videos_overdue_is_true(client, one_checked_out_video) :
    # Act
    response = client.get("/rentals/overdue")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["due_date"] < DATE_TODAY
    assert response_body["customer_id"]==1
    assert response_body["videos_checked_out_count"] == 1
    assert response_body["available_inventory"] == 0