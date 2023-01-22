from conan import ConanFile
from conan.tools.cmake import cmake_layout


class RepoRecipe(ConanFile):
    name = "transport_hegemon"
    version = "0.0.1"

    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"

    def requirements(self):
        # util
        self.requires("fmt/9.1.0")
        self.requires("spdlog/1.11.0")

        self.requires("cli11/2.3.2")
        
        self.requires("range-v3/0.12.0")
        self.requires("tsl-robin-map/1.2.1")

        # math
        self.requires("eigen/3.4.0")

        # render
        self.requires("glfw/3.3.8")
        self.requires("vulkan-loader/1.3.236.0")
        # self.tool_requires("cmake/3.25.0")

    def layout(self):
        cmake_layout(self)
