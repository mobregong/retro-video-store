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

def test_get_no_videos_overdue(client, one_checked_out_video) :
    # Act
    response = client.get("/rentals/overdue")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_video_history(client, one_checked_in_video):
    # Act
    response = client.get("/videos/1/history")
    response_body = response.get_json()

    # Assert

    assert response.status_code == 200
    len(response_body) == 1
    assert response_body[0]["video"] == VIDEO_TITLE
    assert response_body[0]["check-in date"] != None
    assert response_body[0]["video_id"] == VIDEO_ID
    assert  response_body[0]["checkout date"] != None
    assert response_body[0]["customer_id"] == CUSTOMER_ID
    assert response_body[0]["Customer name"] == CUSTOMER_NAME
    # assert response_body['available_inventory'] == 1
    # assert response_body['videos_checked_out_count'] == 0



#  Customer name": customer.name,
#                             "video": video.title,
#                             "check-in date": rental.checked_in,
#                             "video_id": rental.video_id,
#                             "customer_id": rental.customer_id, 
#                             "checkout date": rental.checkout_date})


# VIDEO_TITLE = "A Brand New Video"
# VIDEO_INVENTORY = 1
# VIDEO_RELEASE_DATE = "01-01-2001"

# CUSTOMER_NAME = "A Brand New Customer"
# CUSTOMER_POSTAL_CODE = "12345"
# CUSTOMER_PHONE = "123-123-1234"

def test_get_video_history_video_not_found(client):
    response = client.get("/videos/1/history")

    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body["message"] == "Video 1 was not found"

