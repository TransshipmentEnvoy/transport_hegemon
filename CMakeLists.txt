cmake_minimum_required (VERSION 3.21..3.24)

# ====== sanity check >>>>>>
if (CMAKE_BINARY_DIR STREQUAL CMAKE_SOURCE_DIR)
    message(FATAL_ERROR "Building in-source is not supported! Create a build dir and remove ${CMAKE_SOURCE_DIR}/CMakeCache.txt")
endif()
# <<<<<<

# ====== workspace >>>>>>
cmake_path(SET workspace_DIR NORMALIZE ${CMAKE_CURRENT_LIST_DIR})
message(STATUS "ws dir: ${workspace_DIR}")
# <<<<<<

# ====== import early cmake module >>>>>>
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")

include(opt)
# <<<<<<

# ====== project >>>>>>
project(transport_hegemon)
# <<<<<<

# ====== import cmake module >>>>>>
enable_language(CXX)

include(GNUInstallDirs)

include(lto)
include(cpp_standard)
include(warning)
# <<<<<<

# ====== dependency >>>>>>
find_package(Boost REQUIRED COMPONENTS headers filesystem nowide)
message(STATUS "use boost: ${Boost_DIR}")

find_package(fmt REQUIRED)
message(STATUS "use fmt: ${fmt_DIR}")

find_package(spdlog REQUIRED)
message(STATUS "use spdlog: ${spdlog_DIR}")

find_package(CLI11 REQUIRED)
message(STATUS "use cli11: ${CLI11_DIR}")

find_package(range-v3 REQUIRED)
message(STATUS "use range-v3: ${range-v3_DIR}")

find_package(tsl-robin-map REQUIRED)
message(STATUS "use tsl-robin-map: ${tsl-robin-map_DIR}")

find_package (Eigen3 3.3 REQUIRED NO_MODULE)
message(STATUS "use Eigen3: ${Eigen3_DIR}")

find_package(glfw3 REQUIRED)
message(STATUS "use glfw3: ${glfw3_DIR}")

find_package(Vulkan REQUIRED)
message(STATUS "use vulkan_headers: ${Vulkan_INCLUDE_DIR}")

find_package(shaderc REQUIRED) # provided by conan
message(STATUS "use shaderc: ${shaderc_DIR}")
cmake_path(SET glslc_PATH_HINT NORMALIZE ${shaderc_INCLUDE_DIR}/../bin)
find_program(GLSLC glslc REQUIRED HINTS ${glslc_PATH_HINT})
message(STATUS "use shaderc/glslc: ${GLSLC}")

find_package(vulkan-memory-allocator REQUIRED)
message(STATUS "use vulkan-memory-allocator: ${vulkan-memory-allocator_DIR}")

find_package(flecs REQUIRED)
message(STATUS "use flecs: ${flecs_DIR}")
# <<<<<<

# compile & link property
check_lto_support(LTO_SUPPORTED)

add_executable(transport_hegemon)
target_set_cxx_standard(transport_hegemon)
target_sources(transport_hegemon PRIVATE
    # impl
    src/main.cpp
    # interface
)
target_link_libraries(transport_hegemon
    PRIVATE
        Boost::headers Boost::filesystem Boost::nowide
        fmt::fmt
        spdlog::spdlog
        CLI11::CLI11
        range-v3::range-v3
        tsl::robin_map
        Eigen3::Eigen
        glfw
        Vulkan::Vulkan
        vulkan-memory-allocator::vulkan-memory-allocator
        flecs::flecs
)
target_set_warning(transport_hegemon)
if(LTO_SUPPORTED)
    target_enable_lto(transport_hegemon)
endif()

install(TARGETS transport_hegemon
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
