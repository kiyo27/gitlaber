from gitlab.client import GitLab

class RESTManager:

    gl: GitLab

    def __init__(self, gl: GitLab):
        self.gl = gl