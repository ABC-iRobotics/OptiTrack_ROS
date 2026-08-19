import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'g1_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
  data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')), #ezt add hozzá
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')), #ez kell a g1_servo.launch.py
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gabo',
    maintainer_email='gabo@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'vector_teleop = g1_teleop.g1_vector_teleop:main',
            'direct_teleop = g1_teleop.g1_direct_teleop:main',
            'servo_teleop = g1_teleop.g1_servo_teleop:main',
            'fake_body = g1_teleop.fake_body:main',
        ],
    },
)
