from setuptools import find_packages, setup

package_name = "puzzle_solver"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", ["solution.launch"]),
    ],
    install_requires=[
        "setuptools",
    ],
    zip_safe=True,
    maintainer="solution-team",
    maintainer_email="solution@gitlab.lrz.de",
    description="Solution node",
    license="MIT",
    tests_require=[""],
    entry_points={
        "console_scripts": [
            "main = puzzle_solver.ros.ros_main:main",
        ],
    },
)
