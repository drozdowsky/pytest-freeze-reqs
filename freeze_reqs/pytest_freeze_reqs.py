import pytest


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption(
        "--freeze_reqs",
        action="store_true",
        help="run check if requirements (req*.txt|pip) are frozen",
    )
    parser.addini(
        "freeze-reqs-ignore-paths",
        type="linelist",
        help="each line specifies a part of path to ignore "
        "by pytest-freeze-reqs, example: "
        "requirement_dev.txt matches /a/b/c/requirement_dev.txt",
    )
    parser.addini(
        "freeze-reqs-include-paths",
        type="linelist",
        help="each line specifies a part of path to include "
        "by pytest-freeze-reqs, example: "
        "/base_requirements.txt matches /a/b/c/base_requirements.txt",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "freeze_reqs: mark as freeze requirements test")


def pytest_sessionstart(session):
    config = session.config
    if config.option.freeze_reqs:
        config._freeze_reqs_ignore = config.getini("freeze-reqs-ignore-paths")
        config._freeze_reqs_include = config.getini("freeze-reqs-include-paths")


def pytest_collect_file(parent, path):
    config = parent.config
    if not config.option.freeze_reqs:
        return None

    if path.ext in (".txt", ".pip") and path.basename.startswith("req"):
        for ignore_path in config._freeze_reqs_ignore:
            if ignore_path in str(path):
                return None
        return RequirementFile.from_parent(parent, fspath=path)
    else:
        for include_path in config._freeze_reqs_include:
            if include_path in str(path):
                return RequirementFile.from_parent(parent, fspath=path)


class RequirementFile(pytest.File):
    def collect(self):
        import requirements
        with open(str(self.fspath), "r") as fd:
            for req in requirements.parse(fd):
                yield RequirementItem.from_parent(self, name=req.name, req=req)


class RequirementItem(pytest.Item):
    def __init__(self, name, parent, req):
        super(RequirementItem, self).__init__(name, parent)
        self.add_marker("freeze_reqs")
        self.req = req

    def runtest(self):
        # local files
        if self.req.local_file:
            return

        # revision
        if self.req.vcs:
            if not self.req.revision:
                raise RequirementNotFrozenException(self, self.name, "[no revision]")
            else:
                return

        # pip packages
        if not self.req.specs:
            raise RequirementNotFrozenException(self, self.name, self.req.specs)

        for spec in self.req.specs:
            operator, _ = spec
            if operator in ("<", "<=", "=="):
                return

        raise RequirementNotFrozenException(self, self.name, self.req.specs)

    def repr_failure(self, excinfo):
        """ called when self.runtest() raises an exception. """
        if isinstance(excinfo.value, RequirementNotFrozenException):
            args = excinfo.value.args
            return "\n".join(
                [
                    "requirement freeze test failed",
                    "   improperly frozen requirement: {1!r}: {2!r}".format(*args),
                    "   try adding pkg==version, or git@revision",
                ]
            )

    def reportinfo(self):
        return (
            self.fspath,
            0,
            "requirement: {name} is not frozen properly.".format(name=self.name),
        )


class RequirementNotFrozenException(Exception):
    """ custom exception for error reporting. """
