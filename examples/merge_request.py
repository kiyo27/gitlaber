from gitlab.client import GitLab
from gitlab.objects.merge_request import ProjectMergeRequest
from gitlab.config import GitLabConfigParser


def run():
    config = GitLabConfigParser("GitLab")
    gl = GitLab.merge_config(config)
    mr = ProjectMergeRequest(gl, project_id=config.project_id, mr_id=1)
    # mr.addLabel(["api label"])
    mr.labels()


if __name__ == "__main__":
    run()
