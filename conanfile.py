from conan import ConanFile
from conan.tools.cmake import cmake_layout
from conan.tools import files

import os


class RepoRecipe(ConanFile):
    name = "transport_hegemon"
    version = "0.0.1"

    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"

    def build_requirements(self):
        self.tool_requires("cmake/3.25.0")

    def requirements(self):
        # util
        self.requires("boost/1.81.0")

        self.requires("fmt/9.1.0")
        self.requires("spdlog/1.11.0")

        self.requires("cli11/2.3.2")

        self.requires("range-v3/0.12.0")
        self.requires("tsl-robin-map/1.2.1")

        # math
        self.requires("eigen/3.4.0")

        # render
        self.requires("glfw/3.3.8")
        self.requires("vulkan-headers/1.3.236.0")
        self.requires("vulkan-loader/1.3.236.0")
        self.requires("vulkan-validationlayers/1.3.236.0")
        self.requires("glslang/1.3.236.0")
        self.requires("shaderc/2022.4@transport_hegemon/dep")
        self.requires("vulkan-memory-allocator/3.0.1")

        # logic
        self.requires("flecs/3.1.3")

    def configure(self):
        self.options["boost"].shared = True

        self.options["flecs"].shared = True

    def layout(self):
        cmake_layout(self)

    def generate(self):
        proc_list = [
            ("boost_filesystem.dll", self.dependencies["boost"].cpp_info.components["filesystem"].bindir),
            ("boost_nowide.dll", self.dependencies["boost"].cpp_info.components["nowide"].bindir),
            ("vulkan-1.dll", self.dependencies["vulkan-loader"].cpp_info.bindir),
        ]

        if self.settings.os == "Windows":
            for proc_lib, proc_bindir in proc_list:
                files.copy(self, proc_lib, proc_bindir, os.path.join(self.build_folder, str(self.settings.build_type)))

    def package_info(self):
        print(self.env_info)