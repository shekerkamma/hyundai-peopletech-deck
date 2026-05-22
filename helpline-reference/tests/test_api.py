"""Integration test — build the API app and exercise it end to end."""

from api.routes import build_app


def test_create_and_list_ticket() -> None:
    app = build_app()
    created = app.dispatch(
        "POST /tickets",
        {"org_id": "org_apitest", "subject": "Need help", "body": "details"},
    )
    assert created["status"] == 200
    ticket_id = created["data"]["id"]
    assert ticket_id.startswith("tkt_")

    listed = app.dispatch("GET /tickets", {"org_id": "org_apitest"})
    assert listed["status"] == 200
    assert ticket_id in listed["data"]["tickets"]


def test_validation_error_maps_to_422() -> None:
    app = build_app()
    resp = app.dispatch("POST /tickets", {"org_id": "org_apitest"})  # no subject
    assert resp["status"] == 422


def test_unknown_route_is_404() -> None:
    app = build_app()
    assert app.dispatch("DELETE /nope", {})["status"] == 404
