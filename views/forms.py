import json
from typing import Dict

import flask as flask
from data_source import DataSource
from flask import abort, request
from views.base_blueprint import BaseBlueprint


class FormsBlueprint(BaseBlueprint):

    def __init__(self, data_source: DataSource, config: Dict[str, str]):
        super().__init__(data_source, "forms")
        self.config = config

    def register(self):
        self.blueprint.route("/")(self.list_forms)
        self.blueprint.route(
            "/raw/<stat_name>/<view_date:view_date>/", methods=['GET']
        )(self.raw_form)
        self.blueprint.route(
            "/raw/<stat_name>/<view_date:view_date>/", methods=['POST']
        )(self.raw_form_post)
        self.blueprint.route(
            "/import_google_maps"
        )(self.google_maps_import)

    def list_forms(self):
        forms = ["raw", "import_google_maps"]
        return flask.render_template("list_forms.html", forms=forms)

    def raw_form(self, stat_name, view_date):
        raw_entries = self.data_source.get_entries_for_stat_on_date(stat_name, view_date)
        data = raw_entries[0]["data"]
        raw_data = json.dumps(data, indent=2, sort_keys=True)
        return flask.render_template(
            "form_raw.html",
            stat_name=stat_name, view_date=view_date, raw_data=raw_data
        )

    def raw_form_post(self, stat_name, view_date):
        auth_key = request.form['auth_key']
        new_data = json.loads(request.form['new_data'])
        if auth_key != self.config['edit_auth_key']:
            abort(401)
        self.data_source.update_entry_for_stat_on_date(
            stat_name,
            view_date,
            new_data,
            "Updated via dailys form"
        )
        # Get data and return the form
        return self.raw_form(stat_name, view_date)

    def google_maps_import(self):
        latest_date = None  # TODO: get latest date with google maps data
        timeline_url = f"https://www.google.com/maps/timeline?hl=en&authuser=0" \
                       f"&ei=Bs9bXer4Cv6W1fAPgvOLgAQ%3A45&ved=1t%3A17706" \
                       f"&pb=!1m2!1m1!1s{latest_date.isoformat()}"
        return flask.render_template(
            "import_google_maps.html",
            latest_date=latest_date
        )