pytest_plugins = ["pytester"]


def test_simple_frozen_req(testdir):
    testdir.makefile(
        ext=".txt",
        requirements="""free_requirement
equal_requirement==1.0
less_requirement<=0.1""",
    )
    result = testdir.runpytest("--freeze_reqs")
    assert "free_requirement is not frozen properly" in result.stdout.str()
    assert "equal_requirement is not frozen properly" not in result.stdout.str()
    assert "less_requirement is not frozen properly" not in result.stdout.str()


def test_complex_frozen_req(testdir):
    """ complex requirement is properly frozen using two lines. """
    testdir.makefile(ext=".txt", requirements="""complex_requirement>=1.0,<=1.1""")
    result = testdir.runpytest("--freeze_reqs")
    assert "complex_requirement is not frozen properly" not in result.stdout.str()


def test_ignore_paths(testdir):
    testdir.makefile(ext=".txt", requirements_local="""free_requirement""")
    testdir.makeini(
        """[pytest]
freeze-reqs-ignore-paths=requirements_local.txt"""
    )
    result = testdir.runpytest("--freeze_reqs")
    assert "free_requirement is not frozen properly" not in result.stdout.str()


def test_include_paths(testdir):
    """ local_requirements is not matched by req*.txt """
    testdir.makefile(ext=".txt", local_requirements="""free_requirement""")
    testdir.makeini(
        """[pytest]
freeze-reqs-include-paths=local_requirements.txt"""
    )
    result = testdir.runpytest("--freeze_reqs")
    assert "free_requirement is not frozen properly" in result.stdout.str()


def test_ifs_in_req_file(testdir):
    testdir.makefile(
        ext=".txt",
        requirements="equal_requirement==1.0; python_version < '2.7'",
        requirements2="free_requirement; python_version < '2.7'",
    )
    result = testdir.runpytest("--freeze_reqs")
    assert "equal_requirement is not frozen properly" not in result.stdout.str()
    assert "free_requirement is not frozen properly" in result.stdout.str()


def test_github_revision(testdir):
    testdir.makefile(
        ext=".txt",
        requirements="".join(
            [
                "-e git://github.com/",
                "mozilla/elasticutils.git",
                "@000b14389171a9f0d7d713466b32bc649b0bed8e#egg=elasticutils",
            ]
        ),
    )
    result = testdir.runpytest("--freeze_reqs")
    assert "elasticutils is not frozen properly" not in result.stdout.str()


def test_github_no_revision(testdir):
    testdir.makefile(
        ext=".txt",
        requirements="".join(
            ["-e git://github.com/", "mozilla/elasticutils.git", "#egg=elasticutils"]
        ),
    )
    result = testdir.runpytest("--freeze_reqs")
    assert "elasticutils is not frozen properly" in result.stdout.str()


def test_local_file(testdir):
    testdir.makefile(ext=".txt", requirements="-e /test/file")
    result = testdir.runpytest("--freeze_reqs")
    assert "is not frozen properly" not in result.stdout.str()


def test_marker(testdir):
    testdir.makefile(ext=".txt", requirements="Django==2.2")
    result = testdir.runpytest("-m freeze_reqs --freeze_reqs")
    assert "PytestUnknownMarkWarning" not in result.stdout.str()
