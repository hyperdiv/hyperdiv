import os


def get_frontend_public_path():
    frontend_path = os.path.realpath(
        os.path.join(
            os.path.split(__file__)[0],
            "..",
            "frontend",
            "public",
        )
    )

    if os.path.isdir(frontend_path):
        return frontend_path

    frontend_path = os.path.realpath(
        os.path.join(
            os.path.split(__file__)[0],
            "public",
        )
    )

    if os.path.isdir(frontend_path):
        return frontend_path

    raise Exception("Could not find the frontend.")
