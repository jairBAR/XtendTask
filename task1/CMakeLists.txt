cmake_minimum_required(VERSION 3.5)
project(task1)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

install(DIRECTORY config launch assignment
        DESTINATION share/${PROJECT_NAME})

# Install Python modules
ament_python_install_package(${PROJECT_NAME})
install(PROGRAMS scripts/create_bag.py 
        DESTINATION lib/${PROJECT_NAME}
)

ament_package()

