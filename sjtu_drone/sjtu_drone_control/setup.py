from setuptools import setup, find_packages
import os
from glob import glob

package_name = "sjtu_drone_control"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(),  # Automatically finds all submodules
    install_requires=["setuptools"],
    zip_safe=True,
    include_package_data=True,  # Ensure all package data is included
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
    ],
    entry_points={
        "console_scripts": [
            "teleop = sjtu_drone_control.teleop:main",
            "teleop_joystick = sjtu_drone_control.teleop_joystick:main",
            "open_loop_control = sjtu_drone_control.open_loop_control:main",
            "drone_position_control = sjtu_drone_control.drone_position_control:main",
        ],
    }
)
