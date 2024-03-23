from faker import Faker

from ..config.settings import Config
from ..models.schemas.schema import AdverseIncident, BoundingBox
from ..utils import faker_utils
from ..utils.geo_utils import generate_random_points

boundaries = [[-76.8635495958, 3.1194990575], [-76.8642836451, 3.8006769776], [-76.0888693083, 3.8015092147], [
    -76.088135259, 3.1203318932], [-76.8635495958, 3.1194990575]]

fake = Faker()
fake.add_provider(faker_utils.AdverseIncidentFakerProvider)


def randomize_adverse_incidents():
    number_of_incidents = fake.random_int(1, 5)
    points = generate_random_points(number_of_incidents, boundaries)
    incidents = []
    for i in range(number_of_incidents):
        point = points[i]
        point_latitude = point.y
        point_longitude = point.x
        affected_range = float(Config.ADVERSE_INCIDENTS_AFFECTED_RANGE)
        incidents.append(AdverseIncident(
            description=fake.adverse_incident(),
            bounding_box=BoundingBox(
                latitude_from=point_latitude - affected_range,
                longitude_from=point_longitude - affected_range,
                latitude_to=point_latitude + affected_range,
                longitude_to=point_longitude + affected_range
            )
        ))

    return incidents
