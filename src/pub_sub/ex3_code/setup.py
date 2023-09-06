from setuptools import setup

package_name = 'ex3_code'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mat',
    maintainer_email='mat@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ex3_NodeA = ex3_code.NodeA:main',
            'ex3_NodeB = ex3_code.NodeB:main'
        ],
    },
)
