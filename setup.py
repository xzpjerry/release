from setuptools import find_packages, setup

import versioneer

reqrs = []
try:
    # pip >=20
    from pip._internal.network.session import PipSession
    from pip._internal.req import parse_requirements
except ImportError:
    try:
        # 10.0.0 <= pip <= 19.3.1
        from pip._internal.download import PipSession
        from pip._internal.req import parse_requirements
    except ImportError:
        # pip <= 9.0.3
        from pip.download import PipSession
        from pip.req import parse_requirements
install_reqs = parse_requirements("requirements.txt", session=PipSession())
try:
    reqrs = [str(ir.req) for ir in install_reqs]
except Exception:
    reqrs = [str(ir.requirement) for ir in install_reqs]

with open("README.md", encoding="utf8") as f:
    readme = f.read()

with open("HISTORY.md", encoding="utf8") as f:
    history = f.read()

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Project Short Description",
    long_description=readme + "\n\n" + history,
    long_description_content_type='text/markdown',
    author="xzpjerry",
    author_email="xzpjerry@gmail.com",
    keywords="track_changes",
    url="https://github.com/xzpjerry/tracks_changes",
    include_package_data=True,
    packages=find_packages(include=["track_changes", "track_changes.*"]),
    install_requires=reqrs,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    zip_safe=False,
    entry_points={"console_scripts": [
        "track_changes=track_changes:entrypoint",
        "track-changes=track_changes:entrypoint"
    ]},
)
