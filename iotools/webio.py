import requests

class WebIO:
    def get_response(url: str) -> str:
        resp = requests.get(url)

        if resp.status_code == 200:
            return resp.text
        else:
            raise ConnectionRefusedError(
                f'Unable to reach website. Response status code was {resp.status_code}.'
            )