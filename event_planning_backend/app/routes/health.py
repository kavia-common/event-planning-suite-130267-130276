from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint("Health", "health", url_prefix="/", description="Health check route")

@blp.route("/")
class HealthCheck(MethodView):
    """Basic liveness probe endpoint."""
    def get(self):
        """
        Returns a simple JSON indicating service health.
        """
        return {"message": "Healthy"}
