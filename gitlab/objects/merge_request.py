from gitlab.base import RESTManager
from gitlab.client import GitLab


class ProjectMergeRequest(RESTManager):

    project_id: int
    mr_id: int

    def __init__(self, gl: GitLab, project_id: int, mr_id: int):
        super().__init__(gl)
        self.project_id = project_id
        self.mr_id = mr_id

    def addLabel(self, labels: list):
        data = {"add_labels": ",".join(labels)}
        self.gl.http_put(
            f"/projects/{self.project_id}/merge_requests/{self.mr_id}", post_data=data
        )

    def labels(self):
        result = self.gl.http_get(
            f"/projects/{self.project_id}/merge_requests/{self.mr_id}"
        )
        print(result)
