import requests
from typing import Optional, Dict, Any

class ARDProgram:
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://programm-tools-origin.ard.de/nucleus-rest"
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def _get(self, endpoint: str, path_params: Dict[str, str] = {}, query_params: Dict[str, Any] = {}):
        url = self.base_url + endpoint.format(**path_params)
        response = self.session.get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, data: Dict[str, Any]):
        url = self.base_url + endpoint
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    # --- TV Endpunkte ---
    def get_tv_broadcasts(self, date: str, station: str):
        return self._get("/feeds/tv/broadcasts/{date}/{station}", {"date": date, "station": station})

    def get_tv_broadcasts_videos(self, date: str, station: str):
        return self._get("/feeds/tv/broadcasts_videos/{date}/{station}", {"date": date, "station": station})

    def get_tv_broadcasts_livestreams(self):
        return self._get("/api/tv/broadcasts_livestreams")

    def get_tv_realbroadcasts(self, date: str, station: str):
        return self._get("/feeds/tv/realbroadcasts/{date}/{station}", {"date": date, "station": station})

    def get_tv_stations_ardmt(self, web_only: Optional[str] = None):
        return self._get("/api/tv/stations_ardmt", query_params={"web_only": web_only} if web_only else {})

    def get_tv_stations_afps(self):
        return self._get("/api/tv/stations_afps")

    def get_tv_medias_station_logos(self):
        return self._get("/api/tv/medias/station_logos")

    def get_tv_productions_search(self, query: str, **kwargs):
        params = {"query": query}
        params.update(kwargs)
        return self._get("/api/tv/productions/search", query_params=params)

    def get_tv_mediathek_histories(self, **kwargs):
        return self._get("/api/tv/mediathek_histories", query_params=kwargs)

    # --- Radio Endpunkte ---
    def get_radio_broadcasts_clips(self, date: str, station: str):
        return self._get("/feeds/radio/broadcasts_clips/{date}/{station}", {"date": date, "station": station})

    def get_radio_broadcasts_by_ids(self, ids: str, station: Optional[str] = None):
        params = {"ids": ids}
        if station:
            params["station"] = station
        return self._get("/api/radio/broadcasts_by_ids", query_params=params)

    def get_radio_stations_afps(self):
        return self._get("/api/radio/stations_afps")

    def get_radio_stations_ardat(self):
        return self._get("/api/radio/stations_ardat")

    # --- Subscription ---
    def post_subscriptions(self, data: Dict[str, Any]):
        return self._post("/api/subscriptions", data)
